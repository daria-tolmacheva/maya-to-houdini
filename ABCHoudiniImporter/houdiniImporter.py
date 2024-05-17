from hutil.Qt import QtWidgets
import hou

import os
import subprocess
import sys

from PySide2.QtGui import QCloseEvent

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from pathlib import Path
from shiboken2 import wrapInstance
import pathlib


class HoudiniAlembicImporter(QDialog) :
  """
    A tool for inporting Alembic Cache files to Houdini.

    This class includes a Qt GUI interface and import backend for
    the importer tool.

  """

  def __init__(self, parent=None):
    """init the class and setup dialog"""
    super().__init__(parent)

    # Set the GUI components and layout
    self.setWindowTitle("Maya Alembic Exporter")
    self.resize(500, 300)
    grid_layout = QGridLayout(self)

    # Add import settings
    row = 0
    import_gb = QGroupBox("Import Settings")
    import_gb_layout = QGridLayout()
    import_gb.setLayout(import_gb_layout)
    grid_layout.addWidget(import_gb,row,0) 

    import_row = 0

    assets_folder_button = QPushButton("Find Assets Folder", import_gb)
    assets_folder_button.clicked.connect(self.assets_folder_button_clicked)
    import_gb_layout.addWidget(assets_folder_button, row, 0)
    self.assets_dir_line_edit = QLineEdit()
    try :
      self.assets_dir_line_edit.setPlaceholderText(self.tex_dir)
    except :
      pass
    self.assets_dir_line_edit.setReadOnly(True)
    import_gb_layout.addWidget(self.assets_dir_line_edit, row, 1, 1, 3)
    
    import_row += 1
    tex_folder_button = QPushButton("Find Textures Folder", import_gb)
    tex_folder_button.clicked.connect(self.tex_folder_button_clicked)
    import_gb_layout.addWidget(tex_folder_button,import_row,0)
    self.tex_dir_line_edit = QLineEdit()
    try :
      self.tex_dir_line_edit.setPlaceholderText(self.assets_dir)
    except :
      pass
    self.tex_dir_line_edit.setReadOnly(True)
    import_gb_layout.addWidget(self.tex_dir_line_edit, import_row, 1, 1, 3)

    import_row+=1
    label = QLabel("Import Destination", import_gb)
    import_gb_layout.addWidget(label, import_row, 0, 1, 1)
    self.destination_option = QComboBox(import_gb)
    self.destination_option.addItem("Create new .hip file")
    self.destination_option.addItem("Use existing .hip file")
    import_gb_layout.addWidget(self.destination_option, import_row, 1, 1, 1)

    import_row+=1
    self.hip_folder_button = QPushButton("Destination folder", import_gb)
    self.hip_folder_button.clicked.connect(self.hip_folder_button_clicked)
    import_gb_layout.addWidget(self.hip_folder_button,import_row,0)
    self.hip_folder_line_edit = QLineEdit()
    try :
      self.hip_folder_line_edit.setPlaceholderText(self.hip_folder)
    except :
      pass
    self.hip_folder_line_edit.setReadOnly(True)
    import_gb_layout.addWidget(self.hip_folder_line_edit, import_row, 1, 1, 3)

    import_row+=1
    self.hip_file_button = QPushButton("Destination file", import_gb)
    self.hip_file_button.clicked.connect(self.hip_file_button_clicked)
    import_gb_layout.addWidget(self.hip_file_button, import_row, 0)
    self.hip_file_line_edit = QLineEdit()
    try :
      self.hip_file_line_edit.setPlaceholderText(self.hip_filename_existing)
    except :
      pass
    self.hip_file_line_edit.setReadOnly(True)
    import_gb_layout.addWidget(self.hip_file_line_edit, import_row, 1, 1, 3)
    self.hip_file_line_edit.setVisible(False)
    self.hip_file_button.setVisible(False)

    import_row+=1
    self.hip_filename_label = QLabel("Houdini Scene Filename", import_gb)
    import_gb_layout.addWidget(self.hip_filename_label, import_row, 0, 1, 1)
    self.hip_filename = QLineEdit()
    import_gb_layout.addWidget(self.hip_filename, import_row, 1, 1, 3)

    # needs to happen after objects affected by import_dest_option_changed are created
    self.destination_option.currentIndexChanged.connect(self.import_dest_option_changed)

    import_row+=1

    self.export_button = QPushButton("Import Alembics", import_gb)
    self.export_button.clicked.connect(self.importSelected)
    import_gb_layout.addWidget(self.export_button, import_row, 3, 1, 1)
  
  def assets_folder_button_clicked(self) :
    """Pop up for asset folder search"""
    try :
      self.assets_dir=QFileDialog.getExistingDirectory(self,"Select your assets folder for geometry export", self.assets_dir)
    except :
      hip_dir = hou.text.expandString("$HIP")
      self.assets_dir=QFileDialog.getExistingDirectory(self,"Select your assets folder for geometry export", hip_dir)
    self.assets_dir_line_edit.setPlaceholderText(self.assets_dir)

  def hip_file_button_clicked(self) :
    """Pop up for houdini scene file search"""
    try :
      self.hip_filename_existing=QFileDialog.getOpenFileName(self,"Select a .hip file for geometry import", "./", "Houdini Scene Files (*.hip)")
    except :
      hip_dir = hou.text.expandString("$HIP")
      self.hip_filename_existing=QFileDialog.getExistingDirectory(self,"Select a .hip file for geometry import", hip_dir)
    self.hip_file_line_edit.setPlaceholderText(self.hip_filename_existing)

  def import_dest_option_changed(self, index) :
    """Visibility toggle for different file source options"""
    index = self.destination_option.currentIndex()
    if index == 0 :
      self.hip_folder_button.setVisible(True)
      self.hip_filename_label.setVisible(True)
      self.hip_filename.setVisible(True)
      self.hip_folder_line_edit.setVisible(True)
      self.hip_file_button.setVisible(False)
      self.hip_file_line_edit.setVisible(False)
    elif index == 1 :
      self.hip_folder_button.setVisible(False)
      self.hip_filename_label.setVisible(False)
      self.hip_filename.setVisible(False)
      self.hip_folder_line_edit.setVisible(False)
      self.hip_file_button.setVisible(True)
      self.hip_file_line_edit.setVisible(True)

  def hip_folder_button_clicked(self) :
    """Pop up for .hip file parent folder search"""
    try :
      self.hip_folder=QFileDialog.getExistingDirectory(self,"Select your project folder for .hip file import", self.hip_folder)
    except :
      hip_dir = hou.text.expandString("$HIP")
      self.hip_folder=QFileDialog.getExistingDirectory(self,"Select your project folder for .hip file import", hip_dir)
    self.hip_folder_line_edit.setPlaceholderText(self.hip_folder)

  def tex_folder_button_clicked(self) :
    """Pop up for textures folder search"""
    try :
      self.tex_dir=QFileDialog.getExistingDirectory(self,"Select your textures folder to assign at import", self.tex_dir)
    except :
      hip_dir = hou.text.expandString("$HIP")
      self.tex_dir=QFileDialog.getExistingDirectory(self,"Select your textures folder to assign at import", hip_dir)
    self.tex_dir_line_edit.setPlaceholderText(self.tex_dir)

  def importSelected(self) :
    """
    This function manages and calls  functions that create and initialise
    the new .hip file if needed, followed by scene reconstruction based on
    the imported alembics and corresponding textures.
    """

    print(f"Importing to Houdini")
    currentDir = pathlib.Path.cwd()
    if self.destination_option.currentIndex() == 0 :
      # create new file
      print(f"Creating new file {self.hip_filename.text()}")
      self.sceneSetUpExec(self.hip_filename.text(), currentDir)
      scene_filename = f"{self.hip_folder_line_edit.text()}/{self.hip_filename.text()}"
    else :
      print(f"Importing to file {scene_filename}")
      scene_filename = self.hip_filename_existing.text()
    # importer code
    self.importerExec(scene_filename, self.assets_dir, currentDir)

  def stageSetUp(self) :
    """
    This function sets up the stage level network to organise the scene
    including /obj geometry, lighting and render nodes.
    """
    # Import scene from /obj
    scene_import = hou.node("/stage").createNode("sceneimport::2.0", node_name="import_scene")
    # Add basic Karma light
    sky_dome_light = hou.node("/stage").createNode("karmaskydomelight", node_name="skydome_light")
    # Merge light into imported scene
    merge_light = hou.node("/stage").createNode("merge", node_name="merge_skydome")
    merge_light.setInput(0, scene_import)
    merge_light.setInput(1, sky_dome_light)
    # Add lightlinker for extra user control
    light_linker = hou.node("/stage").createNode("lightlinker", node_name="light_linker")
    light_linker.setInput(0, merge_light)
    # Finish with Karma rendering setup - settings and final rop nodes
    karma_render_setting = hou.node("/stage").createNode("karmarenderproperties", node_name="karma_render_settings")
    karma_render_setting.setInput(0, light_linker)
  
    usd_render_rop = hou.node("/stage").createNode("usdrender_rop", node_name="usd_render_rop")
    usd_render_rop.setInput(0, karma_render_setting)
  
    # Same as "L" shortcut (Layout All)
    # Makes the network readable
    hou.node("/stage").layoutChildren()
  
  def createNewFile(self, filename : str) :
    """
    This function creates, initialises and saves the new .hip file.
    """
    hou.hipFile.clear()
    self.stageSetUp()
    hou.hipFile.setSaveMode(hou.saveMode.Text)
    hou.hipFile.save(filename)

  def sceneSetUpExec(self, scene_filename : str, currentDir :str) :
    self.createNewFile(f"{currentDir}/{scene_filename}")

  def setupObjScene(self, assets_dir : str) :
    """
    This function creates the obj level node tree from .abc files.
    """
    # check if geometry dir exists, if yes - assign geometry_dir
    assets_path = Path(assets_dir)
    if Path(assets_path / 'Geometry').is_dir() == False :
      print(f"{assets_path}/Geometry not found")
      return
    geometry_dir = Path(assets_path / 'Geometry')
    # check if textures dir exists, if yes - assign textures_dir
    if Path(assets_path / 'Textures').is_dir() == False :
      print(f"Textures folder not found, proceeding without assigning materials.")
      return
    self.current_textures_dir = Path(assets_path / 'Textures')

    for dir_object in geometry_dir.iterdir() :
      if dir_object.is_dir() :
        # create geo node
        geo_node = hou.node("/obj").createNode("geo", node_name=dir_object.name+"_Geo")
        # crete merge node inside
        main_merge = geo_node.createNode("merge", node_name=dir_object.name+"_merge")
        # create null node inside
        main_null = geo_node.createNode("null", node_name=dir_object.name.upper()+"_FINAL")
        main_null.setInput(0, main_merge)
        # check for specific textures folder
        self.current_textures_dir = Path(self.current_textures_dir / dir_object.name)
        # create matnet
        matnet_node = geo_node.createNode("matnet", node_name=dir_object.name+"_matnet")
        self.current_matnet = matnet_node
        # go inside the path and call createNodeTree(dir_object)
        self.createNodeTree(dir_object, geo_node, main_merge)
        geo_node.layoutChildren()
        self.current_matnet.layoutChildren()

    # layout the nodes
    hou.node("/obj").layoutChildren()

  def createNodeTree(self, parent_dir : Path, parent_node : hou.Node, child_merge : hou.Node) :
    """
    This recursive function creates the obj level node sub-tree from .abc files.
    """
    # create node tree
    for dir_object in parent_dir.iterdir() :
      if dir_object.is_file() :
        # create import node
        abc_import_node = parent_node.createNode("alembic", node_name=dir_object.stem)
        # set up import file
        abc_import_node.parm("fileName").set(str(dir_object.resolve()))
        # create material in matnet
        material_node = self.createMaterial(dir_object, parent_node)
        material_node.setInput(0, abc_import_node)
        # set up merge input
        child_merge.setNextInput(material_node)
      elif dir_object.is_dir() :
        # create merge node 
        new_merge = parent_node.createNode("merge", node_name=dir_object.name+"_merge")
        # go inside the path and call createNodeTree(dir_object)
        self.createNodeTree(dir_object, parent_node, new_merge)
        # set up merge input
        child_merge.setNextInput(new_merge)

  def createMaterial(self, dir_object : Path, parent_node : hou.Node) :
    """
    This function creates the material corresponding to the input node
    """
    # create material
    material = self.current_matnet.createNode("principledshader::2.0", node_name=dir_object.stem+"_shader")
    material.parm("basecolorr").set(1)
    material.parm("basecolorg").set(1)
    material.parm("basecolorb").set(1)
    material.parm("rough").set(1)
    material.parm("reflect").set(0.095)
    # assign textures
    # -> Base Color
    texture_file_name = dir_object.stem + "_BaseColor.rat"
    if Path(self.current_textures_dir / texture_file_name).is_file() :
      material.parm("basecolor_useTexture").set(True)
      material.parm("basecolor_texture").set(str(Path(self.current_textures_dir / texture_file_name)))
      material.parm("basecolor_useTextureAlpha").set(True)
    # -> Roughness
    texture_file_name = dir_object.stem + "_Roughness.rat"
    if Path(self.current_textures_dir / texture_file_name).is_file() :
      material.parm("rough_useTexture").set(True)
      material.parm("rough_texture").set(str(Path(self.current_textures_dir / texture_file_name)))
    # -> Metallic
    texture_file_name = dir_object.stem + "_Metallic.rat"
    if Path(self.current_textures_dir / texture_file_name).is_file() :
      material.parm("metallic_useTexture").set(True)
      material.parm("metallic_texture").set(str(Path(self.current_textures_dir / texture_file_name)))
    # Create material to assign to geo
    material_node = parent_node.createNode("material", node_name=dir_object.stem+"_material")
    material_node.parm("shop_materialpath1").set(material.path())
    return material_node

  def importToFile(self, scene_filename : str, assets_dir : str) :
    """
    This function is an extry to the process of manipulating
    houdini nodes inside .hip file
    """
    hou.hipFile.load(scene_filename)
    self.setupObjScene(assets_dir)
    hou.hipFile.setSaveMode(hou.saveMode.Text)
    hou.hipFile.save(scene_filename)
    print(f"Import to {Path(scene_filename).name} successful")

  def importerExec(self, scene_filename : str, assets_dir : str, currentDir : str) :
    """
    This function is an extry to the process of creating the nodetree of
    imported nodes.
    """
    self.importToFile(f"{currentDir}/{scene_filename}", assets_dir)


def onCreateInterface():
    importer_dialog = HoudiniAlembicImporter()
    return importer_dialog

