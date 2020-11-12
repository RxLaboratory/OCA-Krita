# DuExportAnim - Duduf Export Animation for Krita
# Copyright (c) 2020 - Nicolas Dufresne, Rainbox Laboratory
# This script is licensed under the GNU General Public License v3
# https://rainboxlab.org
# 
# DuExportAnim was made using "Export Layers" for Krita, which is licensed CC 0 1.0  - public domain
#
# This file is part of DuExportAnim.
#   DuExportAnim is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DuExportAnim is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DuExportAnim. If not, see <http://www.gnu.org/licenses/>.

from . import (exportanimdialog, ocaLib)
from .dukrif import (DuKRIF_utils, DuKRIF_animation, DuKRIF_json, DuKRIF_io)
from PyQt5.QtCore import (Qt, QRect) # pylint: disable=no-name-in-module # pylint: disable=import-error
from PyQt5.QtWidgets import (QFormLayout, QListWidget, QHBoxLayout, # pylint: disable=no-name-in-module # pylint: disable=import-error
                             QDialogButtonBox, QVBoxLayout, QFrame,
                             QPushButton, QAbstractScrollArea, QLineEdit,
                             QMessageBox, QFileDialog, QCheckBox, QSpinBox,
                             QComboBox, QRadioButton, QProgressDialog, QAbstractItemView)
import os
import json
import krita # pylint: disable=import-error

class UIExportAnim(object):

    def __init__(self):
        self.version = "1.1.0"

        self.mainDialog = exportanimdialog.ExportAnimDialog()
        self.mainLayout = QVBoxLayout(self.mainDialog)
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
        self.exportFilterLayersCheckBox = QCheckBox(i18n("Export filter layers")) # pylint: disable=undefined-variable
        self.ignoreInvisibleLayersCheckBox = QCheckBox(i18n("Ignore invisible layers")) # pylint: disable=undefined-variable
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
        self.buttonBox.rejected.connect(self.mainDialog.close)
        self.cropToImageBounds.stateChanged.connect(self._toggleCropSize)
        self.flattenImageCheckbox.stateChanged.connect(self._toggleFlatten)

        self.mainDialog.setWindowModality(Qt.NonModal)
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
        self.optionsLayout.addWidget(self.exportFilterLayersCheckBox)
        self.optionsLayout.addWidget(self.ignoreInvisibleLayersCheckBox)
        self.optionsLayout.addWidget(self.cropToImageBounds)
        self.ignoreInvisibleLayersCheckBox.setChecked(True)

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

        self.mainDialog.resize(500, 300)
        self.mainDialog.setWindowTitle(i18n("OCA Export ") + " v" + self.version) # pylint: disable=undefined-variable
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
            self.msgBox.setText(i18n("Select one document.")) # pylint: disable=undefined-variable
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
        document.setBatchmode(True)

        documentName = document.fileName() if document.fileName() else 'Untitled'  # noqa: E501
        fileName, extension = os.path.splitext(os.path.basename(documentName)) # pylint: disable=unused-variable
        self.exportDir = fileName + '.oca'
        self.mkdir('')

        # Collect doc info
        self.docInfo = DuKRIF_json.getDocInfo(document)
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

        Application.setBatchmode(False) # pylint: disable=undefined-variable
        document.setBatchmode(False)

    def _exportFlattened(self, document, fileFormat, parentDir):
        """ This method exports an flattened image of the document for each keyframe of the animation. """

        nodeInfo = DuKRIF_json.createNodeInfo( self.docInfo['name'])
        nodeInfo['fileType'] = fileFormat
        nodeInfo['animated'] = True
        nodeInfo['position'] = [ self.docInfo['width'] / 2, self.docInfo['height'] / 2 ]
        nodeInfo['width'] = self.docInfo['width']
        nodeInfo['height'] = self.docInfo['height']

        frame = self.docInfo['startTime']
        prevFrameNumber = -1

        while frame <= self.docInfo['endTime']:
            self.progressdialog.setValue(frame)
            if (self.progressdialog.wasCanceled()):
                break
            if DuKRIF_animation.hasKeyframeAtTime(document.rootNode(), frame):
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

        DuKRIF_animation.setCurrentFrame(document, frameNumber)

        imageName = '{0}_{1}'.format( self.docInfo['name'], DuKRIF_utils.intToStr(frameNumber))
        imagePath = '{0}/{1}.{2}'.format( parentDir, imageName, fileFormat)
        imageFileName = self.getAbsolutePath(imagePath)

        succeed = DuKRIF_io.exportDocument(document, imageFileName)
        
        if not succeed:
            frameInfo = DuKRIF_json.createKeyframeInfo("Export failed", "", frameNumber)
        else:       
            frameInfo = DuKRIF_json.createKeyframeInfo(imageName, imagePath, frameNumber)
            frameInfo['position'] = [ self.docInfo['width'] / 2, self.docInfo['height'] / 2 ]
            frameInfo['width'] = self.docInfo['width']
            frameInfo['height'] = self.docInfo['height']
            
        return frameInfo

    def _exportLayers(self, document, parentNode, fileFormat, parentDir):
        """ This method get all sub-nodes from the current node and export them in
            the defined format."""

        nodes = []

        for node in parentNode.childNodes():
            newDir = ''
            if (not self.exportFilterLayersCheckBox.isChecked()
                  and 'filter' in node.type()):
                continue
            elif (self.ignoreInvisibleLayersCheckBox.isChecked()
                  and not node.visible()):
                continue

            nodeInfo = DuKRIF_json.getNodeInfo(document, node)
            nodeInfo['fileType'] = fileFormat

            # translate blending mode to OCA
            if ocaLib.OCABlendingModes[nodeInfo['blendingMode']]:
                nodeInfo['blendingMode'] = ocaLib.OCABlendingModes[nodeInfo['blendingMode']]

            if node.type() == 'grouplayer':
                newDir = os.path.join(parentDir, node.name())
                self.mkdir(newDir)
            else:
                nodeName = node.name()

                self.progressdialog.setLabelText(i18n("Exporting") + " " + node.name()) # pylint: disable=undefined-variable

                _fileFormat = fileFormat
                if '[jpeg]' in nodeName:
                    _fileFormat = 'jpeg'
                elif '[png]' in nodeName:
                    _fileFormat = 'png'
                elif '[exr]' in nodeName:
                    _fileFormat = 'exr'

                frame = self.docInfo['startTime']

                if node.animated():
                    nodeDir = parentDir + '/' + node.name()
                    prevFrameNumber = -1
                    self.mkdir(nodeDir)
                    while frame <= self.docInfo['endTime']:
                        self.progressdialog.setValue(frame)
                        if (self.progressdialog.wasCanceled()):
                            break
                        if node.hasKeyframeAtTime(frame):
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

            if node.childNodes():
                childNodes = self._exportLayers(document, node, fileFormat, newDir)
                nodeInfo['childLayers'] = childNodes

            nodes.append(nodeInfo)

        return nodes

    def _exportNodeFrame(self, document, node, fileFormat, frameNumber, parentDir):

        DuKRIF_animation.setCurrentFrame(document, frameNumber)

        if node.bounds().width() == 0:
            frameInfo = DuKRIF_json.createKeyframeInfo("_blank", "", frameNumber)
            return frameInfo

        imageName = '{0}_{1}'.format( node.name(), DuKRIF_utils.intToStr(frameNumber))
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

        frameInfo = DuKRIF_json.getKeyframeInfo(document, node, frameNumber, not self.cropToImageBounds.isChecked())
        frameInfo['fileName'] = imagePath

        return frameInfo

    def _selectDir(self):
        directory = QFileDialog.getExistingDirectory(
            self.mainDialog,
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
        self.ignoreInvisibleLayersCheckBox.setDisabled(flatten)
        self.cropToImageBounds.setDisabled(flatten)

        if flatten:
            self.exportFilterLayersCheckBox.setChecked(True)
            self.ignoreInvisibleLayersCheckBox.setChecked(True)
            self.cropToImageBounds.setChecked(False)