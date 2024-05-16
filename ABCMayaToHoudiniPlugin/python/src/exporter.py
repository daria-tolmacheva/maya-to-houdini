import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import os

class MayaExporter() :

  def exportSelected(self) :
    # Get the selected Objects
    current_view = cmds.getPanel(withFocus=True)
    objects = cmds.ls(sl=True)
    if len(objects) == 0 :
      cmds.warning("No objects selected")
      return
    file_name = cmds.file(q=True, sn=True).rpartition('/')
    project_dir = file_name[0]
    current_dir = os.path.join(project_dir, "Assets", "Geometry")
    os.makedirs(current_dir, exist_ok=True)
    print(f"current_dir = {current_dir}")
    self.exportNodes(objects, current_dir)

  # Depth-first iteration over node tree
  # to create corresponding directory structure
  # and export files accordingly
  def exportNodes(self, nodes, current_dir) :
    for node in nodes :
      children = cmds.listRelatives(node, children=True, type="transform")
      if children is None :
        file_name = self.splitName(node)
        file_name = os.path.join(current_dir, file_name)
        # export selection as alembic
        startTime = cmds.playbackOptions(minTime =True, q=True)
        endTime = cmds.playbackOptions(maxTime =True, q=True)
        abc_export_args = f"-frameRange {startTime} {endTime} -root {node} -uvWrite -worldSpace -file {file_name}.abc"
        cmds.AbcExport(j = abc_export_args)
        print(f"Exported {node} as alembic")
      else :
        folder_name = self.splitName(node)
        folder_name = os.path.join(current_dir, folder_name)
        os.makedirs(folder_name, exist_ok=True)
        print(f"Created folder named {folder_name}")
        self.exportNodes(children, folder_name)

  # Split names on : and only take right-hand side
  # to avoid long names for referenced-in objects
  def splitName(self, name_to_split) :
    split_name = name_to_split.split(":")
    if len(split_name) > 1 :
      file_name = split_name[1]
    else :
      file_name = name_to_split
    return file_name

if __name__ == "__main__" :
  MayaExporter().exportSelected()

