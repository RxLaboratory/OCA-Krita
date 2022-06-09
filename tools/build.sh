#!/bin/bash

thisModule=../src/
dukrifModule=../../DuKRIF/dukrif
OCAModule=../../../OCA/ocapy

# convert to absolute paths
thisModule=$(cd "$thisModule"; pwd)
dukrifModule=$(cd "$dukrifModule"; pwd)
OCAModule=$(cd "$OCAModule"; pwd)

# remove existing OCA if any
rm -rf "build"
mkdir "build"

# Link desktop file and create the plugin dir
cp "$thisModule/OCA.desktop" "build/OCA.desktop"

# copy plugin files
cp -rf "$thisModule/OCA"  "build/OCA"
# copy DuKRIF
cp -rf "$dukrifModule"  "build/OCA/dukrif"
# copy OCA
cp -rf "$OCAModule"  "build/OCA/ocapy"

# Build doc
cd ../src-docs
mkdocs build

echo "Done!"