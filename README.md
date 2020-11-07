# OCA - Open Cel Animation format for Krita
Exports Animation keyframes from Krita to [OCA](https://github.com/Rainbox-dev/OCA), a *JSON* format + *PNG*/*EXR*

This format can then be imported in After Effects (using [*DuIO*](https://rainboxlab.org/tools/duio/) for example) or any other software with just a little bit of development.

## WIP

The development of this plugin has just started and not everything is implemented yet, but a first version should be available in a couple of weeks.

## Install

This plugin is installed the same way as other Krita plugins.

### Using the plugin importer

First, if you're using the source code instead of a zipped release, you'll have to zip all the files and folders in the [src](src/) subfolder (the *OCA.desktop* file and the *OCA* folder).

1. Open the Script Importer plugin in Krita via `Tools ‣ Scripts ‣ Import Python Plugin...`
2. Locate and import the *OCA.zip* file.
3. Restart Krita
4. Go to `Settings ‣ Configure Krita...`
5. In the `Python Plugin Manager` tab, enable the *OCA* plugin
6. Restart Krita

### Manually

1. Copy (or symlink if you're developping) both the *OCA.desktop* file and the *OCA* folder to the *pykrita* subfolder of the Krita resources folder.
2. Start Krita
3. Go to `Settings ‣ Configure Krita...`
4. In the `Python Plugin Manager` tab, enable the *OCA* plugin
5. Restart Krita

Note: To find your resources folder start Krita and click the `Settings ‣ Manage Resources…` menu item. This will open a dialog box. Click the `Open Resources Folder` button.

## Features

See the [OCA](https://github.com/Rainbox-dev/OCA) format specifications.

Note that vector layers are not supported by *OCA* for Krita (yet).

## Development

### Dependencies

- [DuKRIF](https://github.com/Rainbox-dev/DuKRIF) >= 0.0.1  
Copy or symlink the *DuKRIF* module inside `src/duexportanim`
