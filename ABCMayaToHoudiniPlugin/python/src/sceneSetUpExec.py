import subprocess
import sys

def sceneSetUpExec(scene_filename : str) :

  command = f"./src/executeSceneSetUpCode.sh {scene_filename}"
  result = subprocess.run(command,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.STDOUT,
                          text = True,
                          shell=True)
  print(result.stdout)

if __name__ == "__main__":
  scene_filename = sys.argv[1]
  sceneSetUpExec(scene_filename)
