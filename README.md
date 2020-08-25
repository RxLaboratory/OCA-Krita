# DuExportAnim
 Exports Animation keyframes from Krita to a *JSON* format + *PNG*/*EXR*
 
 This format can then be imported in After Effects (using [*DuIO*](https://rainboxlab.org/tools/duio/) for example) or any other software with just a little bit of development.
 
 ## WIP
 
 The development of this plugin has just started and not everything is implemented yet, but a first version should be available in a couple of weeks.
 
 ## Features
 
 - Layers
 - Layer groups
 - Layer color labels
 - Layer visibility
 - Keyframes / Animation exposure
 - Blending Modes
 - Layer sizes and coordinates
 - Opacity and opacity keyframes
 - Document background color
 - Document color depth
 
 All these properties are stored in the *JSON* file, and the images are stored in *PNG* or *EXR* images.

## Development

### Dependencies

- [DuKRIF](https://github.com/Rainbox-dev/DuKRIF) >= 0.0.1  
Copy or symlink the *DuKRIF* module inside `src/duexportanim`
