import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import os

import subprocess
import sys

from PySide2.QtGui import QCloseEvent

import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI1
import pymel.core as pm
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from pathlib import Path
from shiboken2 import wrapInstance
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import pymel.core as pm
import pathlib

from src.sceneSetUpExec import sceneSetUpExec
from src.importerExec import importerExec


def get_main_window():
  """this returns the maya main window for parenting"""
  window = OpenMayaUI1.MQtUtil.mainWindow()
  return wrapInstance(int(window), QDialog)

class MayaAlembicExporter(MayaQWidgetDockableMixin, QDialog) :

  def __init__(self, parent=get_main_window()):
    """init the class and setup dialog"""
    super().__init__(parent)

    # Set the GUI components and layout
    self.setWindowTitle("Maya Alembic Exporter")
    self.resize(500, 100)
    grid_layout = QGridLayout(self)

    row = 0
    # set export options
    export_row = 0
    export_gb = QGroupBox("Export Settings")
    export_gb_layout = QGridLayout()
    export_gb.setLayout(export_gb_layout)
    grid_layout.addWidget(export_gb, row, 0)

    assets_folder_button = QPushButton("Find Assets Folder", export_gb)
    assets_folder_button.clicked.connect(self.assets_folder_button_clicked)
    export_gb_layout.addWidget(assets_folder_button, row, 0)
    self.assets_dir_line_edit = QLineEdit()
    try :
      self.assets_dir_line_edit.setPlaceholderText(self.tex_dir)
    except :
      pass
    self.assets_dir_line_edit.setReadOnly(True)
    export_gb_layout.addWidget(self.assets_dir_line_edit, export_row, 1, 1, 3)

    export_row+=1
    label = QLabel("Alembic export frame range (by default the slider range is chosen):", export_gb)
    export_gb_layout.addWidget(label, export_row, 0, 1, 4)
    export_row+=1
    self.start_time = QSpinBox(export_gb)
    self.start_time.setRange(1, 10000)
    self.start_time.setValue(cmds.playbackOptions(minTime =True, q=True))
    label = QLabel("Start Frame", export_gb)
    export_gb_layout.addWidget(label, export_row, 0, 1, 1)
    export_gb_layout.addWidget(self.start_time, export_row, 1, 1, 1)
    self.end_time = QSpinBox(export_gb)
    self.end_time.setRange(1, 10000)
    self.end_time.setValue(cmds.playbackOptions(maxTime =True, q=True))
    label = QLabel("End Frame", export_gb)
    export_gb_layout.addWidget(label, export_row, 2, 1, 1)
    export_gb_layout.addWidget(self.end_time, export_row, 3, 1, 1)

    export_row+=1
    self.export_button = QPushButton("Export Alembics", export_gb)
    self.export_button.clicked.connect(self.exportSelected)
    export_gb_layout.addWidget(self.export_button, export_row, 3, 1, 1)

  def assets_folder_button_clicked(self) :
    """Pop up for asset folder search"""
    try :
      self.assets_dir=QFileDialog.getExistingDirectory(self,"Select your assets folder for geometry export", self.assets_dir)
    except :
      project_directory = cmds.workspace(q=True, rd=True)
      self.assets_dir=QFileDialog.getExistingDirectory(self,"Select your assets folder for geometry export", project_directory)
    self.assets_dir_line_edit.setPlaceholderText(self.assets_dir)

  def exportSelected(self) :
    """
    Callback function for Ecport button pressed.
    Kickstarts the export process.
    """
    # Get the selected Objects
    current_view = cmds.getPanel(withFocus=True)
    objects = cmds.ls(sl=True)
    if len(objects) == 0 :
      cmds.warning("No objects selected")
      return
    current_dir = os.path.join(self.assets_dir, "Geometry")
    os.makedirs(current_dir, exist_ok=True)
    print(f"current_dir = {current_dir}")
    self.exportNodes(objects, current_dir)

  def exportNodes(self, nodes, current_dir) :
    """
    Depth-first iteration over node tree
    to create corresponding directory structure
    and export files accordingly
    """
    for node in nodes :
      children = cmds.listRelatives(node, children=True, type="transform")
      if children is None :
        file_name = self.splitName(node)
        file_name = os.path.join(current_dir, file_name)
        # export selection as alembic
        abc_export_args = f"-frameRange {self.start_time.value()} {self.end_time.value()} -root {node} -uvWrite -worldSpace -file {file_name}.abc"
        cmds.AbcExport(j = abc_export_args)
        print(f"Exported {file_name} as alembic")
      else :
        folder_name = self.splitName(node)
        folder_name = os.path.join(current_dir, folder_name)
        os.makedirs(folder_name, exist_ok=True)
        print(f"Created folder named {folder_name}")
        self.exportNodes(children, folder_name)

  def splitName(self, name_to_split) :
    """
    This function splits names on : and only take right-hand side
    to avoid long names for referenced-in objects
    """
    split_name = name_to_split.split(":")
    if len(split_name) > 1 :
      file_name = split_name[1]
    else :
      file_name = name_to_split
    return file_name


if __name__ == "__main__":

    # If we have a dialog open already close
    try:
        maya_exporter_dialog.close()
        maya_exporter_dialog.deleteLater()
    except:
        pass

    maya_exporter_dialog = MayaAlembicExporter()
    maya_exporter_dialog.show()