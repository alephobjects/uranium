# Copyright (c) 2016 Ultimaker B.V.
# Uranium is released under the terms of the AGPLv3 or higher.
from UM.Qt.ListModel import ListModel

from PyQt5.QtCore import pyqtProperty, Qt, pyqtSignal, pyqtSlot, QUrl

from UM.PluginRegistry import PluginRegistry #For getting the possible profile writers to write with.
from UM.Settings.ContainerRegistry import ContainerRegistry
from UM.Settings.InstanceContainer import InstanceContainer

import os

from UM.i18n import i18nCatalog
catalog = i18nCatalog("uranium")

##  Model that holds instance containers. By setting the filter property the instances held by this model can be
#   changed.
class InstanceContainersModel(ListModel):
    NameRole = Qt.UserRole + 1  # Human readable name (string)
    IdRole = Qt.UserRole + 2    # Unique ID of Definition
    MetaDataRole = Qt.UserRole + 3
    ReadOnlyRole = Qt.UserRole + 4
    SectionRole = Qt.UserRole + 5

    def __init__(self, parent = None):
        super().__init__(parent)
        self.addRoleName(self.NameRole, "name")
        self.addRoleName(self.IdRole, "id")
        self.addRoleName(self.MetaDataRole, "metadata")
        self.addRoleName(self.ReadOnlyRole, "readOnly")
        self.addRoleName(self.SectionRole, "section")

        self._instance_containers = []

        self._section_property = ""

        # Listen to changes
        ContainerRegistry.getInstance().containerAdded.connect(self._onContainerChanged)
        ContainerRegistry.getInstance().containerRemoved.connect(self._onContainerChanged)

        self._filter_dict = {}
        self._update()

    ##  Handler for container added / removed events from registry
    def _onContainerChanged(self, container):
        # We only need to update when the changed container is a instanceContainer
        if isinstance(container, InstanceContainer):
            self._update()

    ##  Private convenience function to reset & repopulate the model.
    def _update(self):
        for container in self._instance_containers:
            container.nameChanged.disconnect(self._update)
            container.metaDataChanged.disconnect(self._updateMetaData)

        items = []
        self._instance_containers = ContainerRegistry.getInstance().findInstanceContainers(**self._filter_dict)
        self._instance_containers.sort(key = self._sortKey)

        for container in self._instance_containers:
            container.nameChanged.connect(self._update)
            container.metaDataChanged.connect(self._updateMetaData)

            metadata = container.getMetaData().copy()
            metadata["has_settings"] = len(container.getAllKeys()) > 0

            items.append({
                "name": container.getName(),
                "id": container.getId(),
                "metadata": metadata,
                "readOnly": container.isReadOnly(),
                "section": container.getMetaDataEntry(self._section_property, ""),
            })
        items.sort(key = lambda k: (k["section"], k["id"]))
        self.setItems(items)


    def setSectionProperty(self, property_name):
        if self._section_property != property_name:
            self._section_property = property_name
            self.sectionPropertyChanged.emit()
            self._update()

    sectionPropertyChanged = pyqtSignal()
    @pyqtProperty(str, fset = setSectionProperty, notify = sectionPropertyChanged)
    def sectionProperty(self):
        return self._section_property

    ##  Set the filter of this model based on a string.
    #   \param filter_dict Dictionary to do the filtering by.
    def setFilter(self, filter_dict):
        if filter_dict != self._filter_dict:
            self._filter_dict = filter_dict
            self.filterChanged.emit()
            self._update()

    filterChanged = pyqtSignal()
    @pyqtProperty("QVariantMap", fset = setFilter, notify = filterChanged)
    def filter(self):
        return self._filter_dict

    @pyqtSlot(str, str)
    def rename(self, instance_id, new_name):
        if new_name != self.getName():
            containers = ContainerRegistry.getInstance().findInstanceContainers(id = instance_id)
            if containers:
                containers[0].setName(new_name)
                self._update()

    ##  Gets a list of the possible file filters that the plugins have
    #   registered they can write.
    #
    #   \param io_type \type{str} name of the needed IO type
    #   \return A list of strings indicating file name filters for a file
    #   dialog.
    @pyqtSlot(str, result="QVariantList")
    def getFileNameFilters(self, io_type):
        filters = []
        for plugin_id, meta_data in self._getIOPlugins(io_type):
            for writer in meta_data[io_type]:
                filters.append(writer["description"] + " (*." + writer["extension"] + ")")

        filters.append(
            catalog.i18nc("@item:inlistbox", "All Files (*)"))  # Also allow arbitrary files, if the user so prefers.
        return filters

    @pyqtSlot(result=QUrl)
    def getDefaultPath(self):
        return QUrl.fromLocalFile(os.path.expanduser("~/"))

    ##  Gets a list of profile writer plugins
    #   \return List of tuples of (plugin_id, meta_data).
    def _getIOPlugins(self, io_type):
        pr = PluginRegistry.getInstance()
        active_plugin_ids = pr.getActivePlugins()

        result = []
        for plugin_id in active_plugin_ids:
            meta_data = pr.getMetaData(plugin_id)
            if io_type in meta_data:
                result.append( (plugin_id, meta_data) )
        return result

    @pyqtSlot("QVariantList", QUrl, str)
    def exportProfile(self, instance_id, file_url, file_type):
        if not file_url.isValid():
            return
        path = file_url.toLocalFile()
        if not path:
            return
        ContainerRegistry.getInstance().exportProfile(instance_id, path, file_type)

    @pyqtSlot(QUrl, result="QVariantMap")
    def importProfile(self, file_url):
        if not file_url.isValid():
            return
        path = file_url.toLocalFile()
        if not path:
            return
        return ContainerRegistry.getInstance().importProfile(path)

    def _sortKey(self, item):
        result = []
        if self._section_property:
            result.append(item.getMetaDataEntry(self._section_property, ""))

        result.append(not item.isReadOnly())
        result.append(item.getMetaDataEntry("weight", ""))
        result.append(item.getName())

        return result

    def _updateMetaData(self, container):
        index = self.find("id", container.id)

        if self._section_property:
            self.setProperty(index, "section", container.getMetaDataEntry(self._section_property, ""))

        self.setProperty(index, "metadata", container.getMetaData())
