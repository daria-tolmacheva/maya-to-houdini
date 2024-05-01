# Automated pipeline to export animation from Maya to Houdini 

### Input:
- Maya animated scene file with objects following the naming convention and appropriately grouped
  - Scene_1 -> Character_1 -> body, hair, shorts etc
- Textures folder with png and/or rat files following the naming convention and appropriately grouped
  - Character_1 -> body_texture, hair_texture, shorts_texture etc
- (maybe) an existing Houdini scene file (with other scenes/lighting/objects) (alternatively create new file)
- (maybe) specific group name(s) to export (e.g. for animation fixes of specific objects)

### Output:
- Geometry node in Houdini scene file which:
  - imports all the animated objects,
  - creates appropriate materials (with assigned correct rat textures - converted from png if needed)
  - merges them
  - if file created from scratch, creates a basic Stage level set up

## Process
- go through all the groups in the Maya file
  - export the relevant objects as alembic files, preserving the hierarchy ans naming convension
- go through the Texture folder
  - check if there are png files
    - if png file exists, check if the corresponding rat file exists
      - if not, convert, preserving naming convention
- if no Houdini file given
  - create a new Houdini scene
  - set up stage level
- go through all the alembic files
  - import the alembic
  - generate and assign the material with corresponding textures
  - merge every group to preserve hierarchy

## Texture Conversion Step

Before:
```
└── Textures/
├── Big_brush/
│   ├── Brush_Brush_BaseColor.png
│   ├── Brush_Brush_holder_BaseColor.png
│   ├── Brush_Brush_holder_Roughness.png
│   ├── Brush_Brush_Roughness.png
│   ├── Brush_Handle_BaseColor.png
│   └── Brush_Handle_Roughness.png
└── Dirty_Cotton_Pad/
    ├── cotton_pad_cotton_pad_BaseColor.png
    ├── cotton_pad_cotton_pad_BaseColor.rat
    └── cotton_pad_cotton_pad_Roughness.png
```
After:
```
└── Textures/
    ├── Big_brush/
    │   ├── png/
    │   │   ├── Brush_Brush_BaseColor.png
    │   │   ├── Brush_Brush_holder_BaseColor.png
    │   │   ├── Brush_Brush_holder_Roughness.png
    │   │   ├── Brush_Brush_Roughness.png
    │   │   ├── Brush_Handle_BaseColor.png
    │   │   └── Brush_Handle_Roughness.png
    │   └── rat/
    │       ├── Brush_Brush_BaseColor.rat
    │       ├── Brush_Brush_holder_BaseColor.rat
    │       ├── Brush_Brush_holder_Roughness.rat
    │       ├── Brush_Brush_Roughness.rat
    │       ├── Brush_Handle_BaseColor.rat
    │       └── Brush_Handle_Roughness.rat
    └── Dirty_Cotton_Pad/
        ├── png/
        │   ├── cotton_pad_cotton_pad_BaseColor.png
        │   └── cotton_pad_cotton_pad_Roughness.png
        └── rat/
            ├── cotton_pad_cotton_pad_BaseColor.rat
            └── cotton_pad_cotton_pad_Roughness.rat
```

## Basic Stage level set up:
![basic_stage_set_up.png](images%2Fbasic_stage_set_up.png)
