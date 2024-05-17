#!/usr/bin/env bash

echo "Creating new Houdini scene"

# Set up Houdini Environment
current_dir=$(pwd)
cd /opt/hfs20.0.506/
source houdini_setup_bash
cd $current_dir

# Execute SceneSetUp Code
hython houdiniSceneSetUp.py $1