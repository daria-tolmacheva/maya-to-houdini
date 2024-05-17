import hou
import unittest
from os.path import exists
from os import remove
from pathlib import Path

from src.houdiniSceneSetUp import createNewFile
from src.importer import HoudiniAlembicsImporter

class TestHoudiniImporter(unittest.TestCase) :

  @classmethod
  def setUpClass(self) :
    self.test_file = "./TestFile.hip"
    self.assets_dir = "./src/tests/Importer_Test_Assets"

  @classmethod
  def tearDown(self) :
    if exists(self.test_file): remove(self.test_file)

  @classmethod
  def sceneSetUp(self) :
    createNewFile(self.test_file)
    hou.hipFile.load(self.test_file)
    # import animation
    importer = HoudiniAlembicsImporter()
    importer.importToFile(self.test_file, self.assets_dir)

   # Test node tree structure correct
  def test_treeStructure(self) :
    createNewFile(self.test_file)
    hou.hipFile.load(self.test_file)

    # check things dont exist
    obj_nodes = hou.node("/obj").children()
    self.assertEqual(len(obj_nodes), 0)

    # import animation
    importer = HoudiniAlembicsImporter()
    importer.importToFile(self.test_file, self.assets_dir)

    # check things exist
    # obj level
    obj_nodes = hou.node("/obj").children()
    self.assertEqual(len(obj_nodes), 1)
    self.assertEqual(obj_nodes[0].name(), "Final_Kate_v1_Geo")

    # inside geo node
    geo_children = obj_nodes[0].children()
    self.assertEqual(len(geo_children), 27)
    # only test one subtree structure
    self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/Final_Tshirt_material").input(0), hou.node("/obj/Final_Kate_v1_Geo/Final_Tshirt"))
    self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/Final_UnderWear_material").input(0), hou.node("/obj/Final_Kate_v1_Geo/Final_UnderWear"))
    # Merge input order proved to be unreliable
    # self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/Final_Clothes_grp_merge").input(1), hou.node("/obj/Final_Kate_v1_Geo/Final_UnderWear_material"))
    # self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/Final_Clothes_grp_merge").input(0), hou.node("/obj/Final_Kate_v1_Geo/Final_Tshirt_material"))
    # self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_merge").input(0), hou.node("/obj/Final_Kate_v1_Geo/Final_Clothes_grp_merge"))
    self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/FINAL_KATE_V1_FINAL").input(0), hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_merge"))

  # Test alembics import
  def test_importAlembics(self) :
    self.sceneSetUp()

    # check alembics imported as expected
    imported_file_name = hou.node("/obj/Final_Kate_v1_Geo/Final_Tshirt").parm("fileName").eval()
    self.assertEqual(Path(imported_file_name).name, "Final_Tshirt.abc")
    imported_file_name = hou.node("/obj/Final_Kate_v1_Geo/Final_Eyelash").parm("fileName").eval()
    self.assertEqual(Path(imported_file_name).name, "Final_Eyelash.abc")

  # Test material creation
  def test_createMaterial(self) :
    self.sceneSetUp()

    # check things exist
    self.assertTrue(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet"))
    self.assertTrue(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader"))
    # check material parameters
    self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("basecolorr").eval(), 1)
    self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("basecolorg").eval(), 1)
    self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("basecolorb").eval(), 1)
    self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("rough").eval(), 1)
    self.assertEqual(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("reflect").eval(), 0.095)
    
  # Test assigning textures
  def test_createMaterial(self) :
    self.sceneSetUp()

    # check textures
    # -> Base Color
    self.assertTrue(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("basecolor_useTexture").eval())
    texture_name = hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("basecolor_texture").eval()
    self.assertEqual(Path(texture_name).name, "Final_Body_BaseColor.rat")
    # -> Metallic
    self.assertTrue(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("metallic_useTexture").eval())
    texture_name = hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("metallic_texture").eval()
    self.assertEqual(Path(texture_name).name, "Final_Body_Metallic.rat")
    # -> Roughness
    self.assertTrue(hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("rough_useTexture").eval())
    texture_name = hou.node("/obj/Final_Kate_v1_Geo/Final_Kate_v1_matnet/Final_Body_shader").parm("rough_texture").eval()
    self.assertEqual(Path(texture_name).name, "Final_Body_Roughness.rat")

if __name__ == '__main__':
    unittest.main()