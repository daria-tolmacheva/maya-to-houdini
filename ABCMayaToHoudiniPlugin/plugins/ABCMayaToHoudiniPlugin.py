################################################################################################
# This file is a modified version of Jon Macey's plugin template file
################################################################################################


import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI1
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from exporterGui import MayaAlembicExporter

'''
def maya_useNewAPI():
    """
    Can either use this function (which works on earlier versions)
    or we can set maya_useNewAPI = True
    """
    pass
'''

maya_useNewAPI = True

alembic_exporter_dialog = None

def MayaAlembicExporterScript(restore = False) :
    global alembic_exporter_dialog
    if restore == True :
        restored_control = OpenMayaUI1.MQtUtil.getCurrentParent()
    if alembic_exporter_dialog == None :
        print("Creating new UI")
        alembic_exporter_dialog = MayaAlembicExporter()
        alembic_exporter_dialog.setObjectName('MayaAlembicExporter')
    if restore == True :
        mixin_ptr = OpenMayaUI1.MQtUtil.findControl(alembic_exporter_dialog.objectName())
        OpenMayaUI1.MQtUtil.addWidgetToMayaLayout(int(mixin.ptr), int(restored_control))
    else :
        alembic_exporter_dialog.show(dockable=True, width=600, height=400,
                                 uiScript='MayaAlembicExporterScript(restore=True)')

class ABCMayaExporter(om.MPxCommand) :

    CMD_NAME = "ABCMayaExporter"

    def __init__(self):
        super(ABCMayaExporter, self).__init__()

    def doIt(self, args):
        ui = MayaAlembicExporterScript()
        if ui is not None :
            try :
                cmds.workspaceControl('MayaAlembicExporterWorkspaceControl', e=True, restore=True)
            except :
                pass
        return ui

    @classmethod
    def creator(cls):
        """
        Think of this as a factory
        """
        return ABCMayaExporter()


def initializePlugin(plugin):
    """
    Load our plugin
    """
    vendor = "NCCA"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(ABCMayaExporter.CMD_NAME, ABCMayaExporter.creator)
    except:
        om.MGlobal.displayError(
            "Failed to register command: {0}".format(ABCMayaExporter.CMD_NAME)
        )


def uninitializePlugin(plugin):
    """
    Exit point for a plugin
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(ABCMayaExporter.CMD_NAME)
    except:
        om.MGlobal.displayError(
            "Failed to deregister command: {0}".format(ABCMayaExporter.CMD_NAME)
        )


if __name__ == "__main__":
    """
    So if we execute this in the script editor it will be a __main__ so we can put testing code etc here
    Loading the plugin will not run this
    As we are loading the plugin it needs to be in the plugin path.
    """

    plugin_name = "exporterGUI.py"

    cmds.evalDeferred(
        'if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(
            plugin_name
        )
    )
    cmds.evalDeferred(
        'if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(
            plugin_name
        )
    )
