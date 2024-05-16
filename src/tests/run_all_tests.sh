#!/usr/bin/env bash

echo "Running Houdini tests"

current_dir=$(pwd)
# /public/devel/23-24/bin/hou20shell.sh
cd /opt/hfs20.0.506/
source houdini_setup_bash
cd $current_dir

# set up test
echo "hython src/tests/test_houdiniSceneSetUp.py"
hython src/tests/test_houdiniSceneSetUp.py

# importer test
echo "hython src/tests/test_importer.py"
hython src/tests/test_importer.py 