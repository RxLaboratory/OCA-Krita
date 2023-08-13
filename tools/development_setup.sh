#!/bin/bash

kritaDir=~/.local/share/krita

thisModule=../src/
OCAModule=../../../OCA/lib/py

# convert to absolute paths
thisModule=$(cd "$thisModule"; pwd)
kritaDir=$(cd "$kritaDir"; pwd)
OCAModule=$(cd "$OCAModule"; pwd)

# remove existing OCA if any
rm -r -f "$kritaDir/pykrita/OCA"
rm -f "$kritaDir/pykrita/OCA.desktop"

# Link desktop file and create the plugin dir
ln -s -t "$kritaDir/pykrita" "$thisModule/OCA.desktop"
mkdir "$kritaDir/pykrita/OCA"
mkdir "$kritaDir/pykrita/OCA/oca_krita"
mkdir "$kritaDir/pykrita/OCA/oca_core"

# link plugin files
for file in $thisModule/OCA/*.*; do
    ln -s -t "$kritaDir/pykrita/OCA" "$file"
    echo "Linked $file"
done

# link OCA Core
for file in $OCAModule/oca_core/*.py; do
    ln -s -t "$kritaDir/pykrita/OCA/oca_core" "$file"
    echo "Linked $file"
done
# link OCA Krita
for file in $OCAModule/oca_krita/*.py; do
    ln -s -t "$kritaDir/pykrita/OCA/oca_krita" "$file"
    echo "Linked $file"
done

echo "Done!"