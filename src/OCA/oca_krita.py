import krita # pylint: disable=import-error
from . import utils

# correspondance table for blending modes between OCA / Krita
BLENDING_MODES = {}
BLENDING_MODES['normal'] = 'normal'
BLENDING_MODES['darken'] = 'darken'
BLENDING_MODES['burn'] = 'burn'
BLENDING_MODES['color'] = 'color'
BLENDING_MODES['dodge'] = 'dodge'
BLENDING_MODES['divide'] = 'divide'
BLENDING_MODES['overlay'] = 'overlay'
BLENDING_MODES['luminize'] = 'luminosity'
BLENDING_MODES['soft_light_svg'] = 'soft_light'
BLENDING_MODES['multiply'] = 'multiply'
BLENDING_MODES['saturation'] = 'saturation'
BLENDING_MODES['erase'] = 'erase'
BLENDING_MODES['lighten'] = 'lighten'
BLENDING_MODES['screen'] = 'screen'
BLENDING_MODES['inverse_subtract'] = 'inverse_subtract'
BLENDING_MODES['subtract'] = 'subtract'
BLENDING_MODES['darker color'] = 'darker_color'
BLENDING_MODES['easy burn'] = 'easy_burn'
BLENDING_MODES['fog_darken_ifs_illusions'] = 'fog_darken'
BLENDING_MODES['gamma_dark'] = 'gamma_dark'
BLENDING_MODES['linear_burn'] = 'linear_burn'
BLENDING_MODES['shade_ifs_illusions'] = 'shade'
BLENDING_MODES['converse'] = 'converse'
BLENDING_MODES['and'] = 'and'
BLENDING_MODES['implication'] = 'implication'
BLENDING_MODES['nand'] = 'nand'
BLENDING_MODES['nor'] = 'nor'
BLENDING_MODES['not_converse'] = 'not_converse'
BLENDING_MODES['not_implication'] = 'not_implication'
BLENDING_MODES['or'] = 'or'
BLENDING_MODES['xnor'] = 'xnor'
BLENDING_MODES['xor'] = 'xor'
BLENDING_MODES['dissolve'] = 'dissolve'
BLENDING_MODES['inc_luminosity'] = 'increase_luminosity'
BLENDING_MODES['inc_saturation'] = 'increase_saturation'
BLENDING_MODES['dec_luminosity'] = 'decrease_luminosity'
BLENDING_MODES['dec_saturation'] = 'decrease_saturation'
BLENDING_MODES['hue'] = 'hue'
BLENDING_MODES['divisive_modulo'] = 'divisive_modulo'
BLENDING_MODES['allanon'] = 'allanon'
BLENDING_MODES['alphadarken'] = 'alpha_darken'
BLENDING_MODES['destination-in'] = 'stencil_alpha'
BLENDING_MODES['hard overlay'] = 'hard_overlay'
BLENDING_MODES['interpolation'] = 'interpolation'
BLENDING_MODES['interpolation 2x'] = 'double_interpolation'
BLENDING_MODES['hard mix'] = 'hard_mix'
BLENDING_MODES['hard_mix_photoshop'] = 'hard_mix_photoshop'
BLENDING_MODES['parallel'] = 'parallel'
BLENDING_MODES['penumbra a'] = 'penumbra_a'
BLENDING_MODES['penumbra a'] = 'penumbra_b'
BLENDING_MODES['penumbra a'] = 'penumbra_c'
BLENDING_MODES['penumbra a'] = 'penumbra_d'
BLENDING_MODES['greater'] = 'greater'
BLENDING_MODES['geometric_mean'] = 'geometric_mean'
BLENDING_MODES['additive_subtractive'] = 'additive_subtractive'
BLENDING_MODES['diff'] = 'difference'
BLENDING_MODES['exclusion'] = 'exclusion'
BLENDING_MODES['negation'] = 'negation'
BLENDING_MODES['arc_tangent'] = 'arc_tangent'
BLENDING_MODES['equivalence'] = 'equivalence'
BLENDING_MODES['freeze_reflect'] = 'freeze_reflect'
BLENDING_MODES['freeze'] = 'freeze'
BLENDING_MODES['glow_heat'] = 'glow_heat'
BLENDING_MODES['heat'] = 'heat'
BLENDING_MODES['heat_glow'] = 'heat_glow'
BLENDING_MODES['heat_glow_freeze_reflect_hybrid'] = 'heat_glow_freeze_reflect'
BLENDING_MODES['glow'] = 'glow'
BLENDING_MODES['reflect_freeze'] = 'reflect_freeze'
BLENDING_MODES['reflect'] = 'reflect'
BLENDING_MODES['inc_intensity'] = 'increase_intensity'
BLENDING_MODES['inc_saturation_hsi'] = 'increase_saturation_hsi'
BLENDING_MODES['color_hsi'] = 'color_hsi'
BLENDING_MODES['dec_intensity'] = 'decrease_intensity'
BLENDING_MODES['dec_saturation_hsi'] = 'decrease_saturation_hsi'
BLENDING_MODES['intensity'] = 'intensity'
BLENDING_MODES['saturation_hsi'] = 'saturation_hsi'
BLENDING_MODES['hue_hsi'] = 'hue_hsi'
BLENDING_MODES['inc_lightness'] = 'increase_lightness'
BLENDING_MODES['inc_saturation_hsl'] = 'increase_saturation_hsl'
BLENDING_MODES['color_hsl'] = 'color_hsl'
BLENDING_MODES['dec_lightness'] = 'decrease_lightness'
BLENDING_MODES['dec_saturation_hsl'] = 'decrease_saturation_hsl'
BLENDING_MODES['lightness'] = 'lightness'
BLENDING_MODES['saturation_hsl'] = 'saturation_hsl'
BLENDING_MODES['hue_hsl'] = 'hue_hsl'
BLENDING_MODES['inc_saturation_hsv'] = 'increase_saturation_hsv'
BLENDING_MODES['inc_value'] = 'increase_value'
BLENDING_MODES['color_hsv'] = 'color_hsv'
BLENDING_MODES['dec_saturation_hsv'] = 'decrease_saturation_hsv'
BLENDING_MODES['dec_value'] = 'decrease_value'
BLENDING_MODES['saturation_hsv'] = 'saturation_hsv'
BLENDING_MODES['value'] = 'value'
BLENDING_MODES['lighter color'] = 'lighter_color'
BLENDING_MODES['easy dodge'] = 'easy_dodge'
BLENDING_MODES['flat_light'] = 'flat_light'
BLENDING_MODES['fog_lighten_ifs_illusions'] = 'fog_lighten'
BLENDING_MODES['linear light'] = 'linear_light'
BLENDING_MODES['gamma_illumination'] = 'gamma_illumination'
BLENDING_MODES['luminosity_sai'] = 'luminosity_sai'
BLENDING_MODES['gamma_light'] = 'gamma_light'
BLENDING_MODES['soft_light'] = 'soft_light'
BLENDING_MODES['hard_light'] = 'hard_light'
BLENDING_MODES['pin_light'] = 'pin_light'
BLENDING_MODES['vivid_light'] = 'vivid_light'
BLENDING_MODES['pnorm_a'] = 'pnorm_a'
BLENDING_MODES['pnorm_b'] = 'pnorm_b'
BLENDING_MODES['soft_light_ifs_illusions'] = 'soft_light_ifs'
BLENDING_MODES['soft_light_pegtop_delphi'] = 'soft_light_pegtop_delphi'
BLENDING_MODES['super_light'] = 'super_light'
BLENDING_MODES['tint_ifs_illusions'] = 'tint'
BLENDING_MODES['linear_dodge'] = 'linear_dodge'
BLENDING_MODES['add'] = 'add'

def getDocInfo(document):
    """Creates a new document info."""
    docInfo = {}
    docInfo['name'] = document.name()
    docInfo['frameRate'] = document.framesPerSecond()
    docInfo['width'] = document.width()
    docInfo['height'] = document.height()
    docInfo['startTime'] = document.fullClipRangeStartTime()
    docInfo['endTime'] = document.fullClipRangeEndTime()
    docInfo['colorDepth'] = document.colorDepth()
    bgColor = document.backgroundColor()
    docInfo['backgroundColor'] = [ bgColor.redF(), bgColor.greenF(), bgColor.blueF(), bgColor.alphaF() ]
    docInfo['layers'] = []
    docInfo['originApp'] = 'Krita'
    docInfo['originAppVersion'] = krita.Krita.instance().version()
    return docInfo

def createNodeInfo(name, nodeType = 'paintlayer'):
    """Creates a new default node info of a given type with a given name."""
    nodeInfo = {}
    nodeInfo['name'] = name
    nodeInfo['frames'] = []
    nodeInfo['childLayers'] = []
    nodeInfo['type'] = nodeType
    nodeInfo['fileType'] = ""
    nodeInfo['blendingMode'] = 'normal'
    nodeInfo['animated'] = False
    nodeInfo['position'] = [ 0, 0 ]
    nodeInfo['width'] = 0
    nodeInfo['height'] = 0
    nodeInfo['label'] = -1
    nodeInfo['opacity'] = 1.0
    nodeInfo['visible'] = True
    nodeInfo['reference'] = False
    nodeInfo['passThrough'] = False
    nodeInfo['inheritAlpha'] = False
    return nodeInfo

def getNodeInfo(document, node, useDocumentSize = False):
    """Constructs a new node info based on a given node"""
    nodeInfo = {}
    nodeInfo['name'] = node.name().strip()
    nodeInfo['frames'] = []
    nodeInfo['childLayers'] = []
    nodeInfo['type'] = node.type()
    nodeInfo['fileType'] = ""
    nodeInfo['blendingMode'] = node.blendingMode()
    nodeInfo['animated'] = node.animated()
    if useDocumentSize or node.animated():
        nodeInfo['position'] = [ document.width() / 2, document.height() / 2 ]
        nodeInfo['width'] = document.width()
        nodeInfo['height'] = document.height()
    else:
        nodeInfo['position'] = [ node.bounds().center().x(), node.bounds().center().y() ]
        nodeInfo['width'] = node.bounds().width()
        nodeInfo['height'] = node.bounds().height()
    nodeInfo['label'] = node.colorLabel()
    nodeInfo['opacity'] = node.opacity() / 255.0
    nodeInfo['visible'] = node.visible()
    nodeInfo['passThrough'] = False
    nodeInfo['reference'] = False
    nodeInfo['inheritAlpha'] = node.inheritAlpha()
    if node.type() == 'grouplayer':
        nodeInfo['passThrough'] = node.passThroughMode()
        nodeInfo['width'] = document.width()
        nodeInfo['height'] = document.height()
        nodeInfo['position'] = [ document.width() / 2, document.height() / 2 ]

    return nodeInfo

def createKeyframeInfo(name, fileName, frameNumber):
    """Creates a new default keyframe info."""
    frameInfo = {}
    frameInfo['name'] = name
    frameInfo['fileName'] = fileName
    frameInfo['frameNumber'] = frameNumber
    frameInfo['opacity'] = 1.0
    frameInfo['position'] = [0,0]
    frameInfo['width'] = 0
    frameInfo['height'] = 0
    frameInfo['duration'] = 1

    return frameInfo

def getKeyframeInfo(document, node, frameNumber, useDocumentSize = False):
    """Constructs a new keyframe info based on a given node at a given frame"""
    utils.krita.setCurrentFrame(document, frameNumber)

    frameInfo = {}
    frameInfo['name'] = '{0}_{1}'.format( node.name(), utils.str.intToStr(frameNumber))
    frameInfo['fileName'] = ''
    frameInfo['frameNumber'] = frameNumber
    frameInfo['opacity'] = node.opacity() / 255.0
    if useDocumentSize:
        frameInfo['position'] = [ document.width() / 2, document.height() / 2 ]
        frameInfo['width'] = document.width()
        frameInfo['height'] = document.height()
    else:
        frameInfo['position'] = [ node.bounds().center().x(), node.bounds().center().y() ]
        frameInfo['width'] = node.bounds().width()
        frameInfo['height'] = node.bounds().height()
    frameInfo['duration'] = 1

    return frameInfo