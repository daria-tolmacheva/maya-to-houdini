import subprocess
import sys

def sceneSetUpExec(scene_filename : str, currentDir :str) :

  # result = subprocess.run("pwd", shell=True)

  # command = f"{currentDir}/src/executeSceneSetUpCode.sh {scene_filename}"

  command = f"echo \"Creating new Houdini scene\"; cd /opt/hfs20.0.506/; source houdini_setup_bash; hython houdiniSceneSetUp.py {scene_filename}"

  result = subprocess.run(command,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.STDOUT,
                          text = True,
                          shell=True)
  print(result.stdout)
  return result.stdout

if __name__ == "__main__":
  scene_filename = sys.argv[1]
  currentDir = sys.argv[2]
  sceneSetUpExec(scene_filename, currentDir)
