import hou
import unittest
from os.path import exists
from os import remove
from src.houdiniSceneSetUp import createNewFile

class TestHoudiniSceneSetUp(unittest.TestCase) :

  @classmethod
  def setUpClass(self) :
    self.test_file = "./TestFile.hip"

  @classmethod
  def tearDown(self) :
    if exists(self.test_file): remove(self.test_file)

  # Test file creation
  def test_createNewFile(self) :

    file_exists = exists(self.test_file)
    self.assertFalse(file_exists)
    
    createNewFile(self.test_file)
    file_exists = exists(self.test_file)
    self.assertTrue(file_exists)

  # Test stage level node tree
  def test_stageSetUp(self) :

    createNewFile(self.test_file)
    file_exists = exists(self.test_file)
    self.assertTrue(file_exists)

    hou.hipFile.load(self.test_file)
    stage_nodes = hou.node("/stage").children()

    # Check existance and order of nodes
    self.assertEqual(len(stage_nodes), 6)
    self.assertEqual(stage_nodes[0].name(), "import_scene")
    self.assertEqual(stage_nodes[1].name(), "skydome_light")
    self.assertEqual(stage_nodes[2].name(), "merge_skydome")
    self.assertEqual(stage_nodes[3].name(), "light_linker")
    self.assertEqual(stage_nodes[4].name(), "karma_render_settings")
    self.assertEqual(stage_nodes[5].name(), "usd_render_rop")

    # Check merge node inputs
    self.assertEqual(hou.node("/stage/merge_skydome").input(0), hou.node("/stage/import_scene"))
    self.assertEqual(hou.node("/stage/merge_skydome").input(1), hou.node("/stage/skydome_light"))


if __name__ == '__main__':
    unittest.main()