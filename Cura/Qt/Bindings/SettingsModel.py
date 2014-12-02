from PyQt5.QtCore import Qt, QCoreApplication, pyqtSlot

from Cura.Qt.ListModel import ListModel

class SettingsModel(ListModel):
    
    NameRole = Qt.UserRole + 1 #Label 
    CategoryRole =Qt.UserRole + 2 #Key of category
    CollapsedRole = Qt.UserRole + 3 #Is it collapsed
    TypeRole = Qt.UserRole + 4 # Type of setting (int, float, string, etc)
    ValueRole = Qt.UserRole + 5 # Value of setting
    ValidRole = Qt.UserRole + 6 # Is value valid (5 = correct, 0-4 is error/warning)
    KeyRole = Qt.UserRole + 7 #Unique identifier of setting
    DepthRole = Qt.UserRole + 8
    VisibilityRole = Qt.UserRole + 9
    def __init__(self, parent = None):
        super().__init__(parent)
        self._machine_settings = QCoreApplication.instance().getMachineSettings()
        self._updateSettings()
        
    def roleNames(self):
        return {self.NameRole:'name', self.CategoryRole:"category", self.CollapsedRole:"collapsed",self.TypeRole:"type",self.ValueRole:"value",self.ValidRole:"valid",self.KeyRole:"key", self.DepthRole:"depth", self.VisibilityRole:"visible"}
        
    def _updateSettings(self):
        self.clear()
        settings = self._machine_settings.getAllSettings()
        for setting in settings:
            self.appendItem({"name":setting.getLabel(),"category":setting.getCategory().getLabel(),"collapsed":True,"type":setting.getType(),"value":setting.getValue(),"valid":setting.validate(),"key":setting.getKey(), "depth":setting.getDepth(),"visible":setting.isVisible()})
            
    @pyqtSlot(str)
    def toggleCollapsedByCategory(self, category_key):
        for index in range(0, len(self.items)):
            item = self.items[index]
            if item["category"] == category_key:
                self.setProperty(index, 'collapsed', not item['collapsed'])
    
    @pyqtSlot(int, str, str)
    def settingChanged(self, index, key, value):
        #index = self.items.index(key)
        if self._machine_settings.getSettingByKey(key) is not None:
            self._machine_settings.getSettingByKey(key).setValue(value)
        self.setProperty(index,'valid', self.isValid(key))
    
    @pyqtSlot(str,result=int)
    def isValid(self,key):
        if self._machine_settings.getSettingByKey(key) is not None:
            return self._machine_settings.getSettingByKey(key).validate()
        return 5
    
    @pyqtSlot()
    def saveSettingValues(self):
        self._machine_settings.saveValuesToFile("settings.ini")
        
        
        