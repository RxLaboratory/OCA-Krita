import os
import json
import krita # pylint: disable=import-error
from PyQt5.QtCore import (Qt, QRect) # pylint: disable=no-name-in-module # pylint: disable=import-error
from PyQt5.QtWidgets import ( # pylint: disable=no-name-in-module # pylint: disable=import-error
    QFormLayout,
    QListWidget,
    QHBoxLayout, 
    QDialogButtonBox,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QAbstractScrollArea,
    QLineEdit,
    QMessageBox,
    QFileDialog,
    QCheckBox,
    QSpinBox,
    QRadioButton,
    QProgressDialog,
    QAbstractItemView,
    QDialog
    )

from . import utils
from . import oca_krita
from . import oca
from .config import VERSION, OCA_VERSION

class OCAExportDialog(QDialog):

    disabled_layers = []

    def __init__(self, parent = None):
        super(OCAExportDialog, self).__init__(parent)

        self.version = VERSION
        self.ocaVersion = OCA_VERSION

        self.mainLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.resSpinBoxLayout = QFormLayout()
        self.documentLayout = QVBoxLayout()
        self.directorySelectorLayout = QHBoxLayout()
        self.optionsLayout = QVBoxLayout()
        self.rectSizeLayout = QHBoxLayout()
        self.timeRangeLayout = QVBoxLayout()

        self.refreshButton = QPushButton(i18n("Refresh")) # pylint: disable=undefined-variable
        self.widgetDocuments = QListWidget()
        self.directoryTextField = QLineEdit()
        self.directoryDialogButton = QPushButton(i18n("...")) # pylint: disable=undefined-variable
        self.flattenImageCheckbox = QCheckBox(i18n("Flatten image")) # pylint: disable=undefined-variable
        self.exportReferenceCheckbox = QCheckBox(i18n("Export \"_reference_\" layers")) # pylint: disable=undefined-variable
        self.exportFilterLayersCheckBox = QCheckBox(i18n("Export filter layers")) # pylint: disable=undefined-variable
        self.exportInvisibleLayersCheckBox = QCheckBox(i18n("Export invisible layers")) # pylint: disable=undefined-variable
        self.cropToImageBounds = QCheckBox(i18n("Adjust export size to layer content")) # pylint: disable=undefined-variable

        self.rectWidthSpinBox = QSpinBox()
        self.rectHeightSpinBox = QSpinBox()
        #self.formatsComboBox = QComboBox()
        self.resSpinBox = QSpinBox()

        self.fullClipRadioButton = QRadioButton(i18n("Full clip")) # pylint: disable=undefined-variable
        self.currentSelectionRadioButton = QRadioButton(i18n("Selected range")) # pylint: disable=undefined-variable

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.kritaInstance = krita.Krita.instance()
        self.documentsList = []
        # Store Animation info whem exporting
        self.docInfo = {}
        # Store Export dir
        self.exportDir = ''

        self.directoryTextField.setReadOnly(True)
        self.directoryDialogButton.clicked.connect(self._selectDir)
        self.widgetDocuments.currentRowChanged.connect(self._setResolution)
        self.refreshButton.clicked.connect(self.refreshButtonClicked)
        self.buttonBox.accepted.connect(self.confirmButton)
        self.buttonBox.rejected.connect(self.close)
        self.cropToImageBounds.stateChanged.connect(self._toggleCropSize)
        self.flattenImageCheckbox.stateChanged.connect(self._toggleFlatten)

        self.setWindowModality(Qt.NonModal)
        self.widgetDocuments.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.widgetDocuments.setSelectionMode(QAbstractItemView.MultiSelection)

    def initialize(self):
        self.loadDocuments()

        self.rectWidthSpinBox.setRange(1, 10000)
        self.rectHeightSpinBox.setRange(1, 10000)
        self.resSpinBox.setRange(20, 1200)

        #self.formatsComboBox.addItem(i18n("PNG"))
        #self.formatsComboBox.addItem(i18n("EXR"))

        self.documentLayout.addWidget(self.widgetDocuments)
        self.documentLayout.addWidget(self.refreshButton)

        self.directorySelectorLayout.addWidget(self.directoryTextField)
        self.directorySelectorLayout.addWidget(self.directoryDialogButton)

        self.optionsLayout.addWidget(self.flattenImageCheckbox)
        self.optionsLayout.addWidget(self.exportReferenceCheckbox)
        self.optionsLayout.addWidget(self.exportFilterLayersCheckBox)
        self.optionsLayout.addWidget(self.exportInvisibleLayersCheckBox)
        self.optionsLayout.addWidget(self.cropToImageBounds)
        self.exportReferenceCheckbox.setChecked(True)

        self.resSpinBoxLayout.addRow(i18n("dpi:"), self.resSpinBox) # pylint: disable=undefined-variable

        self.rectSizeLayout.addWidget(self.rectWidthSpinBox)
        self.rectSizeLayout.addWidget(self.rectHeightSpinBox)
        self.rectSizeLayout.addLayout(self.resSpinBoxLayout)

        self.timeRangeLayout.addWidget(self.fullClipRadioButton)
        self.timeRangeLayout.addWidget(self.currentSelectionRadioButton)
        self.fullClipRadioButton.setChecked(True)

        self.formLayout.addRow(i18n("Documents:"), self.documentLayout) # pylint: disable=undefined-variable
        self.formLayout.addRow(i18n("Destination:"), self.directorySelectorLayout) # pylint: disable=undefined-variable
        self.formLayout.addRow(i18n("Export options:"), self.optionsLayout) # pylint: disable=undefined-variable
        self.formLayout.addRow(i18n("Export size:"), self.rectSizeLayout) # pylint: disable=undefined-variable
        #self.formLayout.addRow(
        #    i18n("Images extensions:"), self.formatsComboBox)
        self.formLayout.addRow(i18n("Time range:"), self.timeRangeLayout) # pylint: disable=undefined-variable

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.line)
        self.mainLayout.addWidget(self.buttonBox)

        self.resize(500, 300)
        self.setWindowTitle(i18n("OCA Export ") + " v" + self.version) # pylint: disable=undefined-variable
        self.setSizeGripEnabled(True)
        self.show()
        self.activateWindow()

    def closeEvent(self, event):
        """Accept close"""
        event.accept()

    def loadDocuments(self):
        self.widgetDocuments.clear()

        self.documentsList = [
            document for document in self.kritaInstance.documents()
            if document.fileName()
        ]

        for document in self.documentsList:
            self.widgetDocuments.addItem(document.fileName())

    def refreshButtonClicked(self):
        self.loadDocuments()

    def confirmButton(self):
        selectedPaths = [
            item.text() for item in self.widgetDocuments.selectedItems()]
        selectedDocuments = [
            document for document in self.documentsList
            for path in selectedPaths if path == document.fileName()
        ]

        self.msgBox = QMessageBox(self)
        if not selectedDocuments:
            self.msgBox.setText(i18n("Select at least one document.")) # pylint: disable=undefined-variable
        elif not self.directoryTextField.text():
            self.msgBox.setText(i18n("Select the initial directory.")) # pylint: disable=undefined-variable
        else:
            for doc in selectedDocuments:
                self.export(doc)
            self.msgBox.setText(i18n("All Documents have been exported.")) # pylint: disable=undefined-variable
        self.msgBox.exec_()

    def mkdir(self, directory):
        target_directory = self.getAbsolutePath(directory)
        if (os.path.exists(target_directory)
                and os.path.isdir(target_directory)):
            return

        try:
            os.makedirs(target_directory)
        except OSError as e:
            raise e

    def getAbsolutePath(self, directory):
        return self.directoryTextField.text() + '/' +  self.getRelativePath(directory)

    def getRelativePath(self, directory):
        return self.exportDir + '/' +  directory

    def export(self, document):
        Application.setBatchmode(True) # pylint: disable=undefined-variable

        # Let's duplicate the document first
        document = document.clone()

        document.setBatchmode(True)

        documentName = document.fileName() if document.fileName() else 'Untitled'  # noqa: E501
        fileName, extension = os.path.splitext(os.path.basename(documentName)) # pylint: disable=unused-variable
        self.exportDir = fileName + '.oca'
        self.mkdir('')

        # Collect doc info
        self.docInfo = oca_krita.getDocInfo(document)
        self.docInfo['ocaVersion'] = self.ocaVersion
        if self.docInfo['name'] == "":
            self.docInfo['name'] = "Document"
        documentDir = self.docInfo['name']
        self.mkdir(documentDir)

        if not self.fullClipRadioButton.isChecked():
            self.docInfo['startTime'] = document.playBackStartTime()
            self.docInfo['endTime'] = document.playBackEndTime()
            
        self.progressdialog = QProgressDialog("Exporting animation...", "Cancel", 0, self.docInfo['endTime'] - self.docInfo['startTime'])
        self.progressdialog.setWindowModality(Qt.WindowModality.WindowModal)

        if self.flattenImageCheckbox.isChecked():
            nodeInfo = self._exportFlattened(
                document,
                #self.formatsComboBox.currentText(),
                'png',
                documentDir
            )
            self.docInfo['layers'].append(nodeInfo)
        else:
            nodes = self._exportLayers(
                document,
                document.rootNode(),
                #self.formatsComboBox.currentText(),
                'png',
                documentDir
            )
            self.docInfo['layers'] = nodes

        # Write doc info
        infoFile = open('{0}.oca'.format(self.getAbsolutePath(fileName)),  "w")
        infoFile.write( json.dumps(self.docInfo, indent=4) )
        infoFile.close()

        self.progressdialog.close()

        document.setBatchmode(False)

        # close document
        document.close()

        Application.setBatchmode(False) # pylint: disable=undefined-variable
        
    def _end_export(self):
        # Re-enable all layers
        for node in self.disabled_layers:
            node.setVisible(True)
        self.disabled_layers = []

    def _exportFlattened(self, document, fileFormat, parentDir):
        """ This method exports a flattened image of the document for each keyframe of the animation. """

        nodeInfo = oca_krita.createNodeInfo( self.docInfo['name'])
        nodeInfo['fileType'] = fileFormat
        nodeInfo['animated'] = True
        nodeInfo['position'] = [ self.docInfo['width'] / 2, self.docInfo['height'] / 2 ]
        nodeInfo['width'] = self.docInfo['width']
        nodeInfo['height'] = self.docInfo['height']

        frame = self.docInfo['startTime']
        prevFrameNumber = -1

        self._disable_ignore_nodes(document.rootNode())
        if not self.exportReferenceCheckbox.isChecked():
            self._disable_reference_nodes(document.rootNode())

        while frame <= self.docInfo['endTime']:
            self.progressdialog.setValue(frame)
            if (self.progressdialog.wasCanceled()):
                self._end_export()
                break
            if utils.krita.hasKeyframeAtTime(document.rootNode(), frame):
                frameInfo = self._exportFlattenedFrame(document, fileFormat, frame, parentDir)
                if prevFrameNumber >= 0:
                    nodeInfo['frames'][-1]['duration'] = frame - prevFrameNumber
                nodeInfo['frames'].append(frameInfo)
                prevFrameNumber = frame
            frame = frame + 1

        # set the last frame duration
        if len(nodeInfo['frames']) > 0:
            f = nodeInfo['frames'][-1]
            f['duration'] = document.fullClipRangeEndTime() - f['frameNumber']

        return nodeInfo

    def _exportFlattenedFrame(self, document, fileFormat, frameNumber, parentDir):

        utils.krita.setCurrentFrame(document, frameNumber)

        imageName = '{0}_{1}'.format( self.docInfo['name'], utils.str.intToStr(frameNumber))
        imagePath = '{0}/{1}.{2}'.format( parentDir, imageName, fileFormat)
        imageFileName = self.getAbsolutePath(imagePath)

        succeed = utils.krita.exportDocument(document, imageFileName)
        
        if not succeed:
            frameInfo = oca_krita.createKeyframeInfo("Export failed", "", frameNumber)
        else:       
            frameInfo = oca_krita.createKeyframeInfo(imageName, imagePath, frameNumber)
            frameInfo['position'] = [ self.docInfo['width'] / 2, self.docInfo['height'] / 2 ]
            frameInfo['width'] = self.docInfo['width']
            frameInfo['height'] = self.docInfo['height']
            
        return frameInfo

    def _exportLayers(self, document, parentNode, fileFormat, parentDir):
        """ This method get all sub-nodes from the current node and export them in
            the defined format."""

        nodes = []

        print("OCA >> Listing children of: " + parentNode.name())

        for i, node in enumerate(parentNode.childNodes()):

            if (self.progressdialog.wasCanceled()):
                self._end_export()
                break

            newDir = ''
            nodeName = node.name().strip()

            print("OCA >> Loading node: " + nodeName)

            # ignore filters
            if (not self.exportFilterLayersCheckBox.isChecked()
                  and 'filter' in node.type()):
                continue
            # ignore invisible
            if (not self.exportInvisibleLayersCheckBox.isChecked()
                  and not node.visible()):
                continue
            # ignore reference
            if (not self.exportReferenceCheckbox.isChecked
                  and "_reference_" in nodeName):
                continue
            # ignore _ignore_
            if "_ignore_" in nodeName:
                continue

            merge = "_merge_" in nodeName

            if merge:
                print("OCA >> Merging node: " + nodeName)
                utils.krita.disableNodes(node)
                node = utils.krita.flattenNode(document, node, i, parentNode)
                nodeName = nodeName.replace("_merge_","").strip()
                node.setName( nodeName )
                print("OCA >> Merged and renamed node: " + node.name())

            nodeInfo = oca_krita.getNodeInfo(document, node)
            nodeInfo['fileType'] = fileFormat
            nodeInfo['reference'] = "_reference_" in nodeName
            # Update size if not cropped:
            if not self.cropToImageBounds.isChecked():
                nodeInfo['width'] = document.width()
                nodeInfo['height'] = document.height()
                nodeInfo['position'] = [ document.width() / 2, document.height() / 2 ]

            # translate blending mode to OCA
            nodeInfo['blendingMode'] = oca_krita.BLENDING_MODES.get( nodeInfo['blendingMode'], 'normal' )

            # if there are children and not merged, export them
            if node.childNodes() and not merge:
                newDir = os.path.join(parentDir, nodeName)
                self.mkdir(newDir)
                childNodes = self._exportLayers(document, node, fileFormat, newDir)
                nodeInfo['childLayers'] = childNodes
            # if not a group
            else:
                self._exportNode(document, node, nodeInfo, fileFormat, parentDir)
            
            nodes.append(nodeInfo)

        return nodes

    def _exportNode(self, document, node, nodeInfo, fileFormat, parentDir):
        nodeName = node.name().strip()

        print("OCA >> Exporting node: " + nodeName + " (" + node.type() + ")")

        self.progressdialog.setLabelText(i18n("Exporting") + " " + nodeName) # pylint: disable=undefined-variable

        _fileFormat = fileFormat
        if '[jpeg]' in nodeName:
            _fileFormat = 'jpeg'
        elif '[png]' in nodeName:
            _fileFormat = 'png'
        elif '[exr]' in nodeName:
            _fileFormat = 'exr'

        frame = self.docInfo['startTime']

        if node.animated() or node.type() == 'grouplayer':
            nodeDir = parentDir + '/' + nodeName
            prevFrameNumber = -1
            self.mkdir(nodeDir)
            while frame <= self.docInfo['endTime']:
                self.progressdialog.setValue(frame)
                if (self.progressdialog.wasCanceled()):
                    self._end_export()
                    break
                if utils.krita.hasKeyframeAtTime(node, frame):
                    frameInfo = self._exportNodeFrame(document, node, _fileFormat, frame, nodeDir)
                    if prevFrameNumber >= 0:
                        nodeInfo['frames'][-1]['duration'] = frame - prevFrameNumber
                    nodeInfo['frames'].append(frameInfo)
                    prevFrameNumber = frame
                frame = frame + 1

            # set the last frame duration
            if len(nodeInfo['frames']) > 0:
                f = nodeInfo['frames'][-1]
                f['duration'] = document.fullClipRangeEndTime() - f['frameNumber']

        else:
            frameInfo = self._exportNodeFrame(document, node, _fileFormat, frame, parentDir)
            frameInfo['duration'] = document.playBackEndTime() - document.playBackStartTime()
            nodeInfo['frames'].append(frameInfo)

    def _exportNodeFrame(self, document, node, fileFormat, frameNumber, parentDir):

        utils.krita.setCurrentFrame(document, frameNumber)

        if node.bounds().width() == 0:
            frameInfo = oca_krita.createKeyframeInfo("_blank", "", frameNumber)
            return frameInfo

        imageName = '{0}_{1}'.format( node.name().strip(), utils.str.intToStr(frameNumber))
        imagePath = '{0}/{1}.{2}'.format( parentDir, imageName, fileFormat)
        imageFileName = imageFileName = self.getAbsolutePath(imagePath)

        if self.cropToImageBounds.isChecked():
            bounds = QRect()
        else:
            bounds = QRect(0, 0, self.rectWidthSpinBox.value(), self.rectHeightSpinBox.value())

        opacity = node.opacity()
        node.setOpacity(255)

        node.save(imageFileName, self.resSpinBox.value() / 72., self.resSpinBox.value() / 72., krita.InfoObject(), bounds)

        node.setOpacity(opacity)
        
        # TODO check if the file was correctly exported. The Node.save() method always reports False :/

        frameInfo = oca_krita.getKeyframeInfo(document, node, frameNumber, not self.cropToImageBounds.isChecked())
        frameInfo['fileName'] = imagePath

        return frameInfo

    def _selectDir(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            i18n("Select a Folder"), # pylint: disable=undefined-variable
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly)
        self.directoryTextField.setText(directory)

    def _setResolution(self, index):
        document = self.documentsList[index]
        self.rectWidthSpinBox.setValue(document.width())
        self.rectHeightSpinBox.setValue(document.height())
        self.resSpinBox.setValue(document.resolution())

    def _toggleCropSize(self):
        cropToLayer = self.cropToImageBounds.isChecked()
        self.rectWidthSpinBox.setDisabled(cropToLayer)
        self.rectHeightSpinBox.setDisabled(cropToLayer)

    def _toggleFlatten(self):
        flatten = self.flattenImageCheckbox.isChecked()
        self.exportFilterLayersCheckBox.setDisabled(flatten)
        self.exportInvisibleLayersCheckBox.setDisabled(flatten)
        self.cropToImageBounds.setDisabled(flatten)

        if flatten:
            self.exportFilterLayersCheckBox.setChecked(True)
            self.exportInvisibleLayersCheckBox.setChecked(False)
            self.exportReferenceCheckbox.setChecked(False)
            self.cropToImageBounds.setChecked(False)
        else:
            self.exportFilterLayersCheckBox.setChecked(False)
            self.exportReferenceCheckbox.setChecked(True)

    def _disable_reference_nodes(self, parentNode, disable=True):
        for node in parentNode.childNodes():
            if node.visible():
                if '_reference_' in node.name():
                    node.setVisible(not disable)
                    self.disabled_layers.append(node)

                if node.type() == 'grouplayer':
                    self._disable_reference_nodes(node)