#!/usr/bin/env bash

echo "Converting textures"

# for d in ./*
# do
#   for file in $d/*.png
#   do
#   echo "iconvert $file ${file%.*}.rat"
#   iconvert $file "${file%.*}.rat"
#   done
# done


# Very basic version
# just goes though current directory and converts all
# pngs to rat and leaves them there

directory="."
pattern="*.png"

for file in "$directory"/*.png;
do
  echo "iconvert $file ${file%.*}.rat"
  iconvert $file "${file%.*}.rat"
done
