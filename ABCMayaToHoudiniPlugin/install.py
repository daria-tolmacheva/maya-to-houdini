################################################################################################
# This file is a modified version of Jon Macey's installMdule.py script.
# Original: https://github.com/NCCA/MayaAPICode/blob/master/PythonPlugins/QtUI/installModule.py
################################################################################################

import pathlib
import platform
import os
import sys
import subprocess

mayaLocations = {
        "Linux": "/maya/"
}
houdiniLocations = {
        "Linux": "/houdini20.0/"
}
def installModules(mayaLoc, houLoc, opSys):
    location = pathlib.Path(mayaLoc)
    houLocation = pathlib.Path(houLoc)
    createMod(location)
    moveShelfScript(location)
    movePythonPanel(houLocation)
        

def createMod(location):
    currentDir = pathlib.Path.cwd()
    moduleDir = pathlib.Path.joinpath(pathlib.Path(location), "modules")
    modulePath = pathlib.Path.joinpath(moduleDir, "ABCMayaToHoudini.mod")

    moduleDir.mkdir(exist_ok=True)

    if not pathlib.Path(modulePath).is_file():
        print("writing module file")
        with open(modulePath, "w") as file:
            file.write(f"+ ABCMayaToHoudini 1.0 {currentDir}\n")
            file.write("MAYA_PLUG_IN_PATH +:= plugins\n")
            file.write("PYTHONPATH +:= python")

    print("Module installed")

def moveShelfScript(location) :
    currentDir = pathlib.Path.cwd()
    shelfDir = pathlib.Path.joinpath(currentDir, "shelf")
    shelfPath = pathlib.Path.joinpath(shelfDir, "shelf_AbcExporter.mel")
    shelfPathLocation = pathlib.Path.joinpath(location, "2023/prefs/shelves")
    
    shelfPathLocation.mkdir(exist_ok=True)

    command = f"cp {shelfPath} {shelfPathLocation}"
    subprocess.run(command, shell=True)
    print("Shelf file copied")

def movePythonPanel(location) :
    currentDir = pathlib.Path.cwd()
    panelDir = pathlib.Path.joinpath(currentDir, "../ABCHoudiniImporter")
    panelPath = pathlib.Path.joinpath(panelDir, "abc_importer.pypanel")
    panelPathLocation = pathlib.Path.joinpath(location, "python_panels")

    panelPathLocation.mkdir(exist_ok=True)

    command = f"cp {panelPath} {panelPathLocation}"
    subprocess.run(command, shell=True)
    print("Python panel file copied")



def checkMayaInstalled(opSys):
    mayaLoc = f"{pathlib.Path.home()}{mayaLocations.get(opSys)}"
    if not os.path.isdir(mayaLoc):
        raise
    return mayaLoc

def checkHoudiniInstalled(opSys):
    houLoc = f"{pathlib.Path.home()}{houdiniLocations.get(opSys)}"
    if not os.path.isdir(houLoc):
        raise
    return houLoc

if __name__ == "__main__":

    try:
        opSys = platform.system()
        mayaLoc = checkMayaInstalled(opSys)
    except:
        print("Error can't find maya install")
        sys.exit(-1)

    try:
        opSys = platform.system()
        houLoc = checkHoudiniInstalled(opSys)
    except:
        print("Error can't find houdini20 install")
        sys.exit(-1)

    installModules(mayaLoc, houLoc, opSys)