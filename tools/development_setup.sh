#!/bin/bash

kritaDir=~/.local/share/krita

thisModule=../src/
dukrifModule=../../DuKRIF/dukrif
OCAModule=../../../OCA/ocapy

# convert to absolute paths
thisModule=$(cd "$thisModule"; pwd)
kritaDir=$(cd "$kritaDir"; pwd)
dukrifModule=$(cd "$dukrifModule"; pwd)
OCAModule=$(cd "$OCAModule"; pwd)

# remove existing OCA if any
rm -r -f "$kritaDir/pykrita/OCA"
rm -f "$kritaDir/pykrita/OCA.desktop"

# Link desktop file and create the plugin dir
ln -s -t "$kritaDir/pykrita" "$thisModule/OCA.desktop"
mkdir "$kritaDir/pykrita/OCA"
mkdir "$kritaDir/pykrita/OCA/dukrif"
mkdir "$kritaDir/pykrita/OCA/ocapy"

# link plugin files
for file in $thisModule/OCA/*.*; do
    ln -s -t "$kritaDir/pykrita/OCA" "$file"
    echo "Linked $file"
done

# link DuKRIF
for file in $dukrifModule/*.py; do
    ln -s -t "$kritaDir/pykrita/OCA/dukrif" "$file"
    echo "Linked $file"
done

# link OCA
for file in $OCAModule/*.py; do
    ln -s -t "$kritaDir/pykrita/OCA/ocapy" "$file"
    echo "Linked $file"
done

echo "Done!"