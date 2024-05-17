# Houdini scene set up script
# Called when importing animation to existing file

import hou
import sys
from pathlib import Path

class HoudiniAlembicsImporter() :

  def setupObjScene(self, assets_dir : str) :
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
    hou.hipFile.load(scene_filename)
    self.setupObjScene(assets_dir)
    hou.hipFile.setSaveMode(hou.saveMode.Text)
    hou.hipFile.save(scene_filename)
    print(f"Import to {Path(scene_filename).name} successful")
    # logging to file
    # with open ("debug.txt", "w") as file :
    #   file.write(f"Import to {Path(scene_filename).name} successful")


if __name__ == "__main__":
  scene_filename = sys.argv[1]
  assets_dir = sys.argv[2]
  HoudiniAlembicsImporter().importToFile(scene_filename, assets_dir)