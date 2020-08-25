# DuKRIF - The Duduf Krita Framework
# A Python framework used in the developement of Krita Plugins
# GNU GPL v3

class DuKRIF_utils():
    """Utilitaries"""

    @staticmethod
    def intToStr(i, numDigits = 5):
        """Converts an integer to a string, prepending some 0 to get a certain number of digits"""
        s = str(i)
        while len(s) < numDigits:
            s = "0" + s
        return s

class DuKRIF_animation():
    """Methods to manage animations"""

    @staticmethod
    def hasKeyframeAtTime(parentNode, frameNumber):
        """Checks if the node or one of its children has a keyframe at the given frame number"""
        if parentNode.hasKeyframeAtTime(frameNumber):
            return True
        for node in parentNode.childNodes():
            if DuKRIF_animation.hasKeyframeAtTime(node, frameNumber):
                return True
        return False

class DuKRIF_json():
    """Methods used to export and manage JSON files"""

    @staticmethod
    def getDocInfo(document):
        """Creates a new document info."""
        docInfo = {}
        docInfo['name'] = document.name()
        docInfo['frameRate'] = document.framesPerSecond()
        docInfo['width'] = document.width()
        docInfo['height'] = document.height()
        docInfo['startTime'] = document.fullClipRangeStartTime()
        docInfo['endTime'] = document.fullClipRangeEndTime()
        docInfo['nodes'] = []
        docInfo['colorDepth'] = document.colorDepth()
        bgColor = document.backgroundColor()
        docInfo['backgroundColor'] = [ bgColor.red(), bgColor.green(), bgColor.blue(), bgColor.alpha() ]
        return docInfo

    @staticmethod
    def createNodeInfo(name, nodeType = 'paintlayer'):
        """Creates a new default node info of a given type with a given name."""
        nodeInfo = {}
        nodeInfo['name'] = name
        nodeInfo['frames'] = []
        nodeInfo['childNodes'] = []
        nodeInfo['type'] = nodeType
        nodeInfo['blendingMode'] = 'normal'
        nodeInfo['animated'] = False
        nodeInfo['anchorPoint'] = [ 0, 0 ]
        nodeInfo['width'] = 0
        nodeInfo['height'] = 0
        nodeInfo['colorLabel'] = -1
        nodeInfo['opacity'] = 255
        nodeInfo['visible'] = True
        return nodeInfo

    @staticmethod
    def getNodeInfo(node):
        """Constructs a new node info based on a given node"""
        nodeInfo = {}
        nodeInfo['name'] = node.name()
        nodeInfo['frames'] = []
        nodeInfo['childNodes'] = []
        nodeInfo['type'] = node.type()
        nodeInfo['blendingMode'] = 'normal'
        nodeInfo['animated'] = node.animated()
        nodeInfo['anchorPoint'] = node.bounds().center()
        nodeInfo['width'] = node.bounds().width()
        nodeInfo['height'] = node.bounds().height()
        nodeInfo['colorLabel'] = node.colorLabel()
        nodeInfo['opacity'] = node.opacity()
        nodeInfo['visible'] = node.visible()
        return nodeInfo