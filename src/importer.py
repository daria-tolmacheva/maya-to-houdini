# Houdini scene set up script
# Called when importing animation to existing file

import hou
import sys
from pathlib import Path

def setupObjScene(assets_dir : str) :
  # check if geometry dir exists, if yes - assign geometry_dir
  assets_path = Path(assets_dir)
  if Path(assets_path / 'Geometry').is_dir() == False :
    print(f"{assets_path}/Geometry not found")
    return
  geometry_dir = Path(assets_path / 'Geometry')
  # check if textures dir exists, if yes - assign textures_dir
  # if Path(assets_path / 'Textures').is_dir() == False :
  #   return
  # textures_dir = Path(assets_path / 'Textures')

  for dir_object in geometry_dir.iterdir() :
    if dir_object.is_dir() :
      # create geo node
      geo_node = hou.node("/obj").createNode("geo", node_name=dir_object.name+"_Geo")
      # crete merge node inside
      main_merge = hou.node("/obj/" + geo_node.name()).createNode("merge", node_name=dir_object.name+"_merge")
      # create null node inside
      main_null = hou.node("/obj/" + geo_node.name()).createNode("null", node_name=dir_object.name.upper()+"_FINAL")
      main_null.setInput(0, main_merge)
      # go inside the path and call createNodeTree(dir_object)
      createNodeTree(dir_object, geo_node, main_merge)
      geo_node.layoutChildren()

  # layout the nodes
  hou.node("/obj").layoutChildren()

def createNodeTree(parent_dir : Path, parent_node : hou.Node, child_merge : hou.Node) :
  # create node tree
  for dir_object in parent_dir.iterdir() :
    if dir_object.is_file() :
      # create import node
      abc_import_node = parent_node.createNode("alembic", node_name=dir_object.stem)
      # set up import file
      abc_import_node.parm("fileName").set(str(dir_object.resolve()))
      # set up merge input
      child_merge.setNextInput(abc_import_node)
    elif dir_object.is_dir() :
      # create merge node 
      new_merge = parent_node.createNode("merge", node_name=dir_object.name+"_merge")
      # go inside the path and call createNodeTree(dir_object)
      createNodeTree(dir_object, parent_node, new_merge)
      # set up merge input
      child_merge.setNextInput(new_merge)
    


def importToFile(scene_filename : str, assets_dir : str) :
  hou.hipFile.load(scene_filename)
  setupObjScene(assets_dir)
  hou.hipFile.setSaveMode(hou.saveMode.Text)
  hou.hipFile.save(scene_filename)

if __name__ == "__main__":
  scene_filename = sys.argv[1]
  assets_dir = sys.argv[2]
  importToFile(scene_filename, assets_dir)