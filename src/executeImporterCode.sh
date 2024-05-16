#!/usr/bin/env bash

echo "Importing alembics"

# Set up Houdini Environment
current_dir=$(pwd)
cd /opt/hfs20.0.506/
source houdini_setup_bash
cd $current_dir

# Execute Importer Code
hython src/importer.py $1 $2