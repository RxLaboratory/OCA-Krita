> **[OCA, the Open Cel Animation format](https://rxlaboratorio.org/rx-tool/oca) is an open format to ease traditional/frame-by-frame/cel animation data interchange.**

It is able to export all animation keyframes from a Krita document, keeping the layer structure, blending modes, and a lot of other information. This OCA format can then be imported in other applications like Adobe After Effects or Blender. Although add-ons are available with these to import the OCA documents, it's openness makes it easy to import manually in any app (or write your own importer).

**This is the OCA exporter for Krita**.

This OCA exporter will export the most common features of all drawing/animation software:

- Exports the layers or the flattened image
- Layer Groups (and pass through mode if any)
- Layer Labels
- Layer Visibility
- Layer Inherits Alpha
- Keyframes and their duration (animation exposure)
- Opacity Keyframes
- Blending Modes (see this table for a list)
- Layer Sizes and Coordinates
- Document background color
- Document color depth
