import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.1

import UM 1.0 as UM

UM.MainWindow 
{
    id: base
    visible: true

    width: 1024
    height: 768

    Item 
    {
        id: background_item;
        anchors.fill: parent;

        UM.ApplicationMenu 
        {
            id: menu
            window: base

            Menu 
            {
                title: '&File';

                MenuItem { action: load_file_action; }
                MenuItem { action: save_file_action; }

                MenuSeparator { }

                MenuItem { action: quit_action; }
            }

            Menu 
            {
                title: '&Edit';

                MenuItem { action: undo_action; }
                MenuItem { action: redo_action; }
                MenuSeparator { }
                MenuItem { action: delete_action; }
            }

            Menu 
            {
                title: "&Machine";

                MenuSeparator { }
                MenuItem{text: "UltiScanTastic"; enabled: false;}
            }

            Menu 
            {
                title: '&Settings';

                MenuItem { action: preferences_action; }
                MenuItem { action: plugin_action; }
                MenuItem { action: settings_action; }
            }

            Menu 
            {
                title: '&Help';

                MenuItem { action: helpAction; enabled: false; }
                MenuItem { action: aboutAction; enabled: false; }
            }
        }

        Item 
        {
            id: contentItem;

            y: menu.height
            width: parent.width;
            height: parent.height - menu.height;

            Keys.forwardTo: menu

            DropArea 
            {
                anchors.fill: parent

                onDropped: {
                    if(drop.urls.length > 0) 
                    {
                        for(var i in drop.urls) 
                        {
                            UM.Controller.addMesh(drop.urls[i]);
                        }
                    }
                }
            }

            UM.MeshListPanel 
            {
                id: mesh_list_panel;
 
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
            }

            UM.Panel 
            {
                anchors.top: parent.top
                anchors.left: parent.left

                contents: RowLayout 
                {
                    ToolButton { action: undo_action }
                    ToolButton { action: redo_action }

                    Item { width: 10; }

                    ToolButton { text: "3D"; onClicked: UM.Scene.setActiveCamera('3d'); }
                    ToolButton { text: "Left"; onClicked: UM.Scene.setActiveCamera('left'); }
                    ToolButton { text: "Top"; onClicked: UM.Scene.setActiveCamera('top'); }
                    ToolButton { text: "Front"; onClicked: UM.Scene.setActiveCamera('front'); }
                }
            }

            UM.ToolPanel 
            {
                anchors.top: parent.top;
                anchors.horizontalCenter: parent.horizontalCenter
            }

            UM.Panel {
                anchors.top: parent.top
                anchors.right: parent.right

                contents: RowLayout 
                {
                    ComboBox 
                    {
                        model: UM.Models.viewModel

                        onCurrentIndexChanged: UM.Controller.setActiveView(model.items[currentIndex].text)
                    }

                    ToolButton { text: "Settings"; onClicked: preferences.visible = true; }
                    ToolButton { text: "Help"; }
                }
            }

            UM.SettingsPanel 
            {
                anchors.right: parent.right;
                anchors.verticalCenter: parent.verticalCenter

                onSettingConfigurationRequested: 
                {
                    preferences.visible = true;
                    preferences.setPage(1);
                }
            }

            UM.JobList { anchors.left: parent.left; anchors.bottom: parent.bottom; width: parent.width / 10; height: parent.height / 5; }
        }
    }

    UM.PreferencesDialog { id: preferences }

    Action 
    {
        id: undo_action;
        text: "Undo";
        iconName: "edit-undo";
        shortcut: StandardKey.Undo;
        onTriggered: UM.OperationStack.undo();
        enabled: UM.OperationStack.canUndo;
    }

    Action 
    {
        id: redo_action;
        text: "Redo";
        iconName: "edit-redo";
        shortcut: StandardKey.Redo;
        onTriggered: UM.OperationStack.redo();
        enabled: UM.OperationStack.canRedo;
    }

    Action 
    {
        id: quit_action;
        text: "Quit";
        iconName: "application-exit";
        shortcut: StandardKey.Quit;
        onTriggered: Qt.quit();
    }

    Action 
    {
        id: preferences_action;
        text: "Preferences";
        iconName: "configure";
        onTriggered: preferences.visible = true;
    }
    
    Action
    {   
        id: plugin_action;
        text: "Plugins";
        onTriggered: 
        {
            preferences.visible = true;
            preferences.setPage(2);  
        }
    }
    
    Action
    {   
        id: settings_action;
        text: "Settings";
        onTriggered: 
        {
            preferences.visible = true;
            preferences.setPage(1);  
        }
    }

    Action 
    {
        id: helpAction;
        text: "Show Manual";
        iconName: "help-contents";
        shortcut: StandardKey.Help;
    }

    Action 
    {
        id: aboutAction;
        text: "About...";
        iconName: "help-about";
    }

    Action 
    {
        id: delete_action;
        text: "Delete Selection";
        iconName: "edit-delete";
        shortcut: StandardKey.Delete;
        onTriggered: UM.Controller.removeSelection();
    }

    Action 
    {
        id: load_file_action;
        text: "Open...";
        iconName: "document-open";
        shortcut: StandardKey.Open;
        onTriggered: open_file_dialog.open()
    }

    Action 
    {
        id: save_file_action;
        text: "Save...";
        iconName: "document-save";
        shortcut: StandardKey.Save;
        onTriggered: UM.Controller.saveWorkspace();
    }

    Menu {
        id: contextMenu;

        MenuItem { action: delete_action; }
    }
   
   FileDialog {
        id: open_file_dialog

        title: "Choose files"
        modality: Qt.NonModal
        //TODO: Support multiple file selection, workaround bug in KDE file dialog
        //selectMultiple: true

        onAccepted: 
        {
            UM.Controller.addMesh(fileUrl)
        }
    }
}
