import pathlib
import platform
import os
import sys

mayaLocations = {
        "Linux": "/maya/",
}

def installModules(mayaLoc, opSys):
    currentDir = pathlib.Path.cwd()
    location = pathlib.Path(mayaLoc)
    moduleDir = pathlib.Path.joinpath(location, "modules")
    modulePath = pathlib.Path.joinpath(moduleDir, "ABCMayaToHoudini.mod")

    moduleDir.mkdir(exist_ok=True)

    if not pathlib.Path(modulePath).is_file():
        print("writing module file")
        with open(modulePath, "w") as file:
            file.write(f"+ <MayaEditor 1.0 {currentDir}\n")
            file.write("MAYA_PLUG_IN_PATH +:= plugins\n")
            file.write("PYTHONPATH +:= python")

def checkMayaInstalled(opSys):
    mayaLoc = f"{pathlib.Path.home()}{mayaLocations.get(opSys)}"
    if not os.path.isdir(mayaLoc):
        raise
    return mayaLoc

if __name__ == "__main__":

    try:
        opSys = platform.system()
        mayaLoc = checkMayaInstalled(opSys)
    except:
        print("Error can't find maya install")
        sys.exit(-1)
    installModules(mayaLoc, opSys)