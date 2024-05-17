# Automated pipeline to export animation from Maya to Houdini 

This pipeline is developed to make the task of transferring animated multi-textured objects from Maya to Houdini. 
Maya Exporter helps quickly export animated meshes as Alembic Cache files preserving the hierarchy in the firm of file structure.
Houdini Importer helps quickly import those alembic files, while recreating the object hierarcy and creating individual materials with assigned textures to each component.

## Pre-Requisites
- Maya 2023
- Houdini20
- Python 3 (for installation script)
- PySide2

## Installation
1. Download the project zip from GitHub via the green button above the list of files (or clone the repository).
   1. Unzip if needed.
2. Right-click folder `ABCMayaToHoudiniPlugin` and choose "Open in Terminal" (or otherwise navigate to this folder in the terminal).
3. Copy the following code and press `Enter`:
    ```python install.py```
4. Now open Maya 2023 (or restart if already open) and click on shelf "AbcExporter".
   1. The "AbcExporter" shelf tool is available and will be opened with a click.
   2. Once open, it can be docked like any other Maya window.
5. Open Houdini20 (or restart if already open).
   1. Press `+` for "New Tab" -> New Pane Tab Type -> Misc -> Python Panel
   2. Switch from "Quick Start: Calendar Example" to "Alembics Importer"
   3. Once open, it is ready to be used and can be treated as any other Tab.

## Use

### Maya Exporter
Select root-most transform nodes of the objects you want to export, select the approppriate export settings and click Export Alembics to use.
1. Find Asset Folder: a folder where Geometry folder wil be created where the alembic files to be exported.
2. Start/End Frames: frame range of the alembics to export. Be default has slider range values. Can be both set to 1 to export static objects.

The Assets folder will then have the following structure:
```
└── Assets/
    └── Geometry/
        ├── Object1/
        │   ├── Body/
        │   │   ├── Head.abc
        │   │   └── Body.abc
        │   └── Clothes/
        │       ├── Top.abc
        │       └── Bottom.abc
        └── Object2/
            ├── Part1.abc
            └── Part2.abc
```
The corresponding Textures folder should be organised as such:
```
└── Assets/
    └── Geometry/
        ├── Object1/
        │   ├── Head_BaseColor.rat
        │   ├── Body_BaseColor.rat
        │   ├── Top_BaseColor.rat
        │   ├── Bottom_BaseColor.rat
        │   ├── Head_Roughness.rat
        │   ├── Body_Roughness.rat
        │   ├── Top_Roughness.rat
        │   ├── Bottom_Roughness.rat
        │   ├── Head_Metallic.rat
        │   └── Body_Metallic.rat
        └── Object2/
            ├── Part1_BaseColor.rat
            ├── Part2_BaseColor.rat
            ├── Part1_Roughness.rat
            └── Part2_Roughness.rat
```
The naming convention must be followed:
Name.abc = Name_BaseColor.rat = Name_Roughness.rat = Name_Metallic.rat

### Houdini Importer
Choose the following Import Settings and click Import Alembics to recreate geometry tree:
1. Find Assets Folder: a folder where Geometry folder lives with the alembic files to be imported.
2. Find Textures Folder: a folder where textures associated with each alembic file live.
3. Import destination: choose to create a new scene file or use an existing one.
4. If "Create a new .hip file is chosen":
   1. Destination folder: folder where the newly created scene file should be saved.
   2. Houdini Scene Filename: new file name including the extention(!)
5. If "Use existing .hip file" is chosen:
   1. Destination file: choose the file you want to load and import alembics to.

Once imported, the alembics will show up in `obj/` level merged accorfding to the file structure of `Geometry` folder with corresponding textured being assigned from `Textures` folder. The materials will be created in a matnet inside a corresponding `Geo` node for better organisation.
Only base color, metallic and roughness textures are supported.
The `/stage` level will include the basic Karma render nodes, object level import and basic light (skydome). The cameras would still need to be added. 

## Basic Stage level set up:
![basic_stage_set_up.png](images%2Fbasic_stage_set_up.png)

## Running tests
Tests for Houdini part of the pipeline can be run from inside `python` folder with
```hython -m unittest discover -s src/tests/```

