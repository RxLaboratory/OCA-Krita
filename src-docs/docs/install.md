# How to install OCA for Krita

This plugin is installed the same way as other Krita plugins.

## Using the plugin importer

1. Open the Script Importer plugin in Krita via `Tools ‣ Scripts ‣ Import Python Plugin...`
2. Locate and import the *OCA.zip* file you've downloaded.
3. Activate the plugin
4. Restart Krita

## Manually

1. Copy (or symlink if you're developping) both the *OCA.desktop* file and the *OCA* folder to the *pykrita* subfolder of the Krita resources folder.
2. Start Krita
3. Go to `Settings ‣ Configure Krita...`
4. In the `Python Plugin Manager` tab, enable the *OCA* plugin
5. Restart Krita

!!! note
    To find your resources folder, start Krita and click the `Settings ‣ Manage Resources…` menu item. This will open a dialog box. Click the `Open Resources Folder` button.
