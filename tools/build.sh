#!/bin/bash

thisModule=../src/
OCAModule=../../../OCA/lib/py

# convert to absolute paths
thisModule=$(cd "$thisModule"; pwd)
OCAModule=$(cd "$OCAModule"; pwd)

# remove existing OCA if any
rm -rf "build"
mkdir "build"

# Link desktop file and create the plugin dir
cp "$thisModule/OCA.desktop" "build/OCA.desktop"

# copy plugin files
cp -rf "$thisModule/OCA"  "build/OCA"
# copy OCA
cp -rf "$OCAModule/oca_core"  "build/OCA/oca_core"
cp -rf "$OCAModule/oca_krita"  "build/OCA/oca_krita"

# Build doc
cd ../src-docs
mkdocs build

echo "Done!"