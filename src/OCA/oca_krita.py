import krita # pylint: disable=import-error
from . import utils

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