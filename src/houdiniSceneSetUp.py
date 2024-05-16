# Houdini scene set up script
# Called if importing animation to new file

import hou
import sys

# Set up the stage level network to organise the scene
# including /obj geometry, lighting and render nodes
def stageSetUp() :
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

  # load_render_settings(karma_render_setting)

  usd_render_rop = hou.node("/stage").createNode("usdrender_rop", node_name="usd_render_rop")
  usd_render_rop.setInput(0, karma_render_setting)

  # Same as "L" shortcut (Layout All)
  # Makes the network readable
  hou.node("/stage").layoutChildren()

# def load_render_settings(settings_node) :
#   ...

# Create, initialise and save the new file
def createNewFile(filename : str) :
  hou.hipFile.clear()
  stageSetUp()
  hou.hipFile.setSaveMode(hou.saveMode.Text)
  hou.hipFile.save(filename)

if __name__ == "__main__":
  scene_filename = sys.argv[1]
  createNewFile(scene_filename)
