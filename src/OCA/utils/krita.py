import time
import krita # pylint: disable=import-error

def setCurrentFrame(document, frameNumber):
    """Sets the current frame in the document and waits for the image to be cached."""
    document.setCurrentTime(frameNumber)
    document.refreshProjection()

def hasKeyframeAtTime(parentNode, frameNumber, visibleNodesOnly=True ):
    """Checks if the node or one of its children has a keyframe at the given frame number"""

    if visibleNodesOnly and not parentNode.visible():
        return False

    if parentNode.hasKeyframeAtTime(frameNumber):
        return True

    for node in parentNode.childNodes():
        if hasKeyframeAtTime(node, frameNumber):
            return True

    return False

def flattenNode(document, node, nodeIndex, parentNode):
    # create a layer right above the node to merge
    mergeNode = document.createNode(node.name(), 'paintlayer')
    parentNode.addChildNode(mergeNode, node)
    mergeNode.mergeDown()
    newNode = parentNode.childNodes()[nodeIndex]
    return newNode

def disableNodes(parentNode, disable=True, tag='_ignore_'):
    """Disables all nodes containing '_ignore_' in their name."""
    for node in parentNode.childNodes():
        if node.visible():
            if tag in node.name():
                node.setVisible(not disable)

            if node.type() == 'grouplayer':
                disableNodes(node, disable, tag)

def exportDocument(document, fileName, timeOut=10000):
    """Attempts to export the document for timeOut milliseconds"""

    succeed = False

    currentTime = 0
    while currentTime < timeOut:
        succeed = document.exportImage(fileName, krita.InfoObject())
        if succeed:
            break
        time.sleep(0.5)
        currentTime = currentTime + 500

    return succeed
