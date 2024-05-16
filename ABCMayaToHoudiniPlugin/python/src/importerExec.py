import subprocess
import sys

def importerExec(scene_filename : str, assets_dir : str) :

  command = f"./src/executeImporterCode.sh {scene_filename} {assets_dir}"
  result = subprocess.run(command,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.STDOUT,
                          text = True,
                          shell=True)
  print(result.stdout)

if __name__ == "__main__":
  scene_filename = sys.argv[1]
  assets_dir = sys.argv[2]
  importerExec(scene_filename, assets_dir)