import subprocess
import sys
from pathlib import Path
import os

def convertTextures(textures_dir : str) :
  for root, dirs, files in os.walk(textures_dir) :
    for file in files :
      if file.endswith('.png') :
        command = f"/public/devel/23-24/bin/hou20shell.sh; iconvert {os.path.join(root, file)} {root}/{Path(file).stem}.rat"
        subprocess.run(command, shell=True)


if __name__ == "__main__":
  textures_dir = sys.argv[1]
  convertTextures(textures_dir)