import subprocess
import sys

def importerExec(scene_filename : str, assets_dir : str, currentDir : str) :

  # result = subprocess.run("pwd", shell=True)

  # command = f"{currentDir}/src/executeImporterCode.sh {scene_filename} {assets_dir}"

  command = f"echo \"Importing alembics\"; # Set up Houdini Environment; cd /opt/hfs20.0.506/; source houdini_setup_bash; hython src/importer.py {scene_filename} {assets_dir}"

  result = subprocess.run(command,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.STDOUT,
                          text = True,
                          shell=True)
  print(result.stdout)
  return result.stdout

if __name__ == "__main__":
  scene_filename = sys.argv[1]
  assets_dir = sys.argv[2]
  currentDir = sys.argv[3]
  importerExec(scene_filename, assets_dir, currentDir)