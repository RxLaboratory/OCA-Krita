# OCA - Open Cel Animation format for Krita
Exports Animation keyframes from Krita to [OCA](https://github.com/Rainbox-dev/OCA), a *JSON* format + *PNG*/*EXR*

This format can then be imported in After Effects (using [*DuIO*](https://rainboxlab.org/tools/duio/) for example) or any other software with just a little bit of development.

## WIP

The development of this plugin has just started and not everything is implemented yet, but a first version should be available in a couple of weeks.

## Features

See the [OCA](https://github.com/Rainbox-dev/OCA) format specifications.

Note that vector layers are not supported by *OCA* for Krita (yet).

## Development

### Dependencies

- [DuKRIF](https://github.com/Rainbox-dev/DuKRIF) >= 0.0.1  
Copy or symlink the *DuKRIF* module inside `src/duexportanim`
