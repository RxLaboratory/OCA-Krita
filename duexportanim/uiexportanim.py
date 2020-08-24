# This script was made from export layers / GNU GPL v3

from . import exportanimdialog
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtWidgets import (QFormLayout, QListWidget, QHBoxLayout,
                             QDialogButtonBox, QVBoxLayout, QFrame,
                             QPushButton, QAbstractScrollArea, QLineEdit,
                             QMessageBox, QFileDialog, QCheckBox, QSpinBox,
                             QComboBox, QRadioButton, QProgressDialog)
import os
import json
import time
import krita

class UIExportAnim(object):

    def __init__(self):
        self.mainDialog = exportanimdialog.ExportAnimDialog()
        self.mainLayout = QVBoxLayout(self.mainDialog)
        self.formLayout = QFormLayout()
        self.resSpinBoxLayout = QFormLayout()
        self.documentLayout = QVBoxLayout()
        self.directorySelectorLayout = QHBoxLayout()
        self.optionsLayout = QVBoxLayout()
        self.rectSizeLayout = QHBoxLayout()
        self.timeRangeLayout = QVBoxLayout()

        self.refreshButton = QPushButton(i18n("Refresh"))
        self.widgetDocuments = QListWidget()
        self.directoryTextField = QLineEdit()
        self.directoryDialogButton = QPushButton(i18n("..."))
        self.flattenImageCheckbox = QCheckBox(
            i18n("Flatten image"))
        self.exportFilterLayersCheckBox = QCheckBox(
            i18n("Export filter layers"))
        self.ignoreInvisibleLayersCheckBox = QCheckBox(
            i18n("Ignore invisible layers"))
        self.cropToImageBounds = QCheckBox(
            i18n("Adjust export size to layer content"))

        self.rectWidthSpinBox = QSpinBox()
        self.rectHeightSpinBox = QSpinBox()
        #self.formatsComboBox = QComboBox()
        self.resSpinBox = QSpinBox()

        self.fullClipRadioButton = QRadioButton(
            i18n("Full clip"))
        self.currentSelectionRadioButton = QRadioButton(
            i18n("Selected range"))

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.kritaInstance = krita.Krita.instance()
        self.documentsList = []
        # Store Animation info whem exporting
        self.docInfo = {}

        self.directoryTextField.setReadOnly(True)
        self.directoryDialogButton.clicked.connect(self._selectDir)
        self.widgetDocuments.currentRowChanged.connect(self._setResolution)
        self.refreshButton.clicked.connect(self.refreshButtonClicked)
        self.buttonBox.accepted.connect(self.confirmButton)
        self.buttonBox.rejected.connect(self.mainDialog.close)
        self.cropToImageBounds.stateChanged.connect(self._toggleCropSize)
        self.flattenImageCheckbox.stateChanged.connect(self._toggleFlatten)

        self.mainDialog.setWindowModality(Qt.NonModal)
        self.widgetDocuments.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)

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
        self.optionsLayout.addWidget(self.exportFilterLayersCheckBox)
        self.optionsLayout.addWidget(self.ignoreInvisibleLayersCheckBox)
        self.optionsLayout.addWidget(self.cropToImageBounds)

        self.resSpinBoxLayout.addRow(i18n("dpi:"), self.resSpinBox)

        self.rectSizeLayout.addWidget(self.rectWidthSpinBox)
        self.rectSizeLayout.addWidget(self.rectHeightSpinBox)
        self.rectSizeLayout.addLayout(self.resSpinBoxLayout)

        self.timeRangeLayout.addWidget(self.fullClipRadioButton)
        self.timeRangeLayout.addWidget(self.currentSelectionRadioButton)
        self.fullClipRadioButton.setChecked(True)

        self.formLayout.addRow(i18n("Documents:"), self.documentLayout)
        self.formLayout.addRow(
            i18n("Initial directory:"), self.directorySelectorLayout)
        self.formLayout.addRow(i18n("Export options:"), self.optionsLayout)
        self.formLayout.addRow(i18n("Export size:"), self.rectSizeLayout)
        #self.formLayout.addRow(
        #    i18n("Images extensions:"), self.formatsComboBox)
        self.formLayout.addRow(i18n("Time range:"), self.timeRangeLayout)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.line)
        self.mainLayout.addWidget(self.buttonBox)

        self.mainDialog.resize(500, 300)
        self.mainDialog.setWindowTitle(i18n("Export Animation"))
        self.mainDialog.setSizeGripEnabled(True)
        self.mainDialog.show()
        self.mainDialog.activateWindow()

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

        self.msgBox = QMessageBox(self.mainDialog)
        if not selectedDocuments:
            self.msgBox.setText(i18n("Select one document."))
        elif not self.directoryTextField.text():
            self.msgBox.setText(i18n("Select the initial directory."))
        else:
            self.export(selectedDocuments[0])
            self.msgBox.setText(i18n("All layers has been exported."))
        self.msgBox.exec_()

    def mkdir(self, directory):
        target_directory = self.directoryTextField.text() + directory
        if (os.path.exists(target_directory)
                and os.path.isdir(target_directory)):
            return

        try:
            os.makedirs(target_directory)
        except OSError as e:
            raise e

    def export(self, document):
        document.setBatchmode(True)

        documentName = document.fileName() if document.fileName() else 'Untitled'  # noqa: E501
        fileName, extension = os.path.splitext(os.path.basename(documentName))
        self.mkdir('/' + fileName)

        # Collect doc info
        self.docInfo = {}
        self.docInfo['name'] = fileName
        self.docInfo['frameRate'] = document.framesPerSecond()
        self.docInfo['width'] = document.width()
        self.docInfo['height'] = document.height()
        if self.fullClipRadioButton.isChecked():
            self.docInfo['startTime'] = document.fullClipRangeStartTime()
            self.docInfo['endTime'] = document.fullClipRangeEndTime()
        else:
            self.docInfo['startTime'] = document.playBackStartTime()
            self.docInfo['endTime'] = document.playBackEndTime()

        self.progressdialog = QProgressDialog("Exporting animation...", "Cancel", 0, self.docInfo['endTime'] - self.docInfo['startTime'])
        self.progressdialog.setWindowModality(Qt.WindowModality.WindowModal)

        self.docInfo['nodes'] = []

        if self.flattenImageCheckbox.isChecked():
            nodeInfo = self._exportFlattened(
                document,
                #self.formatsComboBox.currentText(),
                'png',
                fileName
            )
            self.docInfo['nodes'].append(nodeInfo)
        else:
            pass
            #self._exportLayers(
            #    document.rootNode(),
            #    self.formatsComboBox.currentText(),
            #    'PNG',
            #   '/' + fileName)

        # Write doc info
        infoFile = open('{0}/{1}.json'.format(self.directoryTextField.text(), fileName),  "w")
        infoFile.write( json.dumps(self.docInfo, indent=4) )
        infoFile.close()

        document.setBatchmode(False)

    def _exportFlattened(self, document, fileFormat, parentDir):
        """ This method exports an flattened image of the document for each keyframe of the animation. """

        nodeInfo = {}
        nodeInfo['name'] = self.docInfo['name']
        nodeInfo['frames'] = []
        nodeInfo['childNodes'] = []
        nodeInfo['type'] = 'imageLayer'

        frame = self.docInfo['startTime']

        while frame <= self.docInfo['endTime']:
            self.progressdialog.setValue(frame)
            if (self.progressdialog.wasCanceled()):
                break
            if self._hasKeyframeAtTime(document.rootNode(), frame):
                frameInfo = self._exportFlattenedFrame(document, fileFormat, frame, parentDir)
                nodeInfo['frames'].append(frameInfo)
            frame = frame + 1

        return nodeInfo

    def _exportFlattenedFrame(self, document, fileFormat, frameNumber, parentDir, numTries = 0):

        document.setCurrentTime(frameNumber)

        imageName = '{0}_{1}'.format( self.docInfo['name'], self._intToStr(frameNumber))
        imagePath = '{0}/{1}.{2}'.format( parentDir, imageName, fileFormat)
        imageFileName = '{0}/{1}'.format( self.directoryTextField.text(), imagePath)

        succeed = document.exportImage(imageFileName, krita.InfoObject())
        frameInfo = {}
        if not succeed:
            if numTries > 5:
                frameInfo['name'] = "Export Failed"
                return frameInfo
            time.sleep(1)
            self._exportFlattenedFrame(document, fileFormat, frameNumber, parentDir, numTries+1)
            
        frameInfo['name'] = imageName
        frameInfo['fileName'] = imagePath
        frameInfo['frameNumber'] = frameNumber
        return frameInfo

    def _hasKeyframeAtTime(self, parentNode, frameNumber):
        if parentNode.hasKeyframeAtTime(frameNumber):
            return True
        for node in parentNode.childNodes():
            if self._hasKeyframeAtTime(node, frameNumber):
                return True
        return False

    def _intToStr(self, i, numCharacters = 5):
        s = str(i)
        while len(s) < numCharacters:
            s = "0" + s
        return s

    def _selectDir(self):
        directory = QFileDialog.getExistingDirectory(
            self.mainDialog,
            i18n("Select a Folder"),
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
        self.ignoreInvisibleLayersCheckBox.setDisabled(flatten)
        self.cropToImageBounds.setDisabled(flatten)

        if flatten:
            self.exportFilterLayersCheckBox.setChecked(True)
            self.ignoreInvisibleLayersCheckBox.setChecked(False)
            self.cropToImageBounds.setChecked(False)