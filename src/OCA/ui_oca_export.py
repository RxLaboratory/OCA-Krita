"""! @brief The OCA Export Dialog, including export functions
 @file ui_oca_export.py
 @section authors Author(s)
  - Created by Nicolas Dufresne on 4/1/2024 .
"""

import os
import datetime
import krita # pylint: disable=import-error
from PyQt5.QtCore import ( # pylint: disable=no-name-in-module,import-error
    Qt,
    QSize,
)
from PyQt5.QtGui import ( # pylint: disable=no-name-in-module,import-error
    QIcon,
    QPixmap,
)
from PyQt5.QtWidgets import ( # pylint: disable=no-name-in-module,import-error
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
    QAbstractItemView,
    QDialog,
    QTabWidget,
    QWidget,
    QLabel,
    QTextEdit,
    QListWidgetItem,
    QListView,
    )

# oca_krita contains the actual OCA for Krita code,
# it is available in the OCA main repo at https://codeberg.org/RxLaboratory/OCA
import oca_krita as oca # pylint: disable=no-name-in-module
from .config import VERSION
from .ui_settings_dialog import SettingsDialog

class OCAExportDialog(QDialog):

    disabled_layers:list = []

    def __init__(self, parent = None):
        super(OCAExportDialog, self).__init__(parent)

        self.version = VERSION
        self.ocaVersion = oca.VERSION

        self.mainLayout = QVBoxLayout(self)

        self.tabWidget = QTabWidget(self)
        self.mainLayout.addWidget(self.tabWidget)

        self.optionsWidget = QWidget(self.tabWidget)
        self.tabWidget.addTab(self.optionsWidget,"Export options")

        self.formLayout = QFormLayout(self.optionsWidget)
        self.resSpinBoxLayout = QFormLayout()
        self.documentLayout = QVBoxLayout()
        self.directorySelectorLayout = QHBoxLayout()
        self.optionsLayout = QVBoxLayout()
        self.rectSizeLayout = QHBoxLayout()
        self.timeRangeLayout = QVBoxLayout()

        self.refreshButton = QPushButton(i18n("Refresh")) # pylint: disable=undefined-variable
        self.widgetDocuments = QListWidget()
        self.widgetDocuments.setViewMode(QListView.IconMode)
        self.widgetDocuments.setIconSize(QSize(128,128))
        self.widgetDocuments.setGridSize(QSize(138,140))
        self.widgetDocuments.setMinimumHeight(150)
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

        self.metadataWidget = QWidget(self.tabWidget)
        self.tabWidget.addTab(self.metadataWidget,"Metadata")

        self.metadataLayout = QFormLayout(self.metadataWidget)

        now = datetime.datetime.now()
        meta = oca.kMetadata.PLUGIN_METADATA

        self.authorEdit = QLineEdit()
        self.descriptionEdit = QTextEdit()
        self.copyrightEdit = QLineEdit("ⓒ Copyright " + str(now.date().year))
        self.licenseEdit = QLineEdit()
        self.licenseEdit.setPlaceholderText("CC-BY-NC-SA 4.0")
        self.licenseLongEdit = QLineEdit()
        self.licenseLongEdit.setPlaceholderText("Creative Commons-Attribution-NonCommercial-ShareAlike 4.0")
        self.licenseURLEdit = QLineEdit()
        self.licenseURLEdit.setPlaceholderText("https://creativecommons.org/licenses/by-nc-sa/4.0/")
        self.createdLabel = QLabel(now.strftime("%Y-%m-%d %H:%M:%S"))
        self.originAppLabel = QLabel(meta.get('originApp', ""))
        self.originAppVersionLabel = QLabel(meta.get('originAppVersion', ""))
        self.exportedByLabel = QLabel(meta.get('exportedBy', ""))
        self.exportedByIDLabel = QLabel(meta.get('exportedByID', ""))
        self.exportedByOrgLabel = QLabel(meta.get('exportedByOrg', ""))
        self.exportedByURLabel = QLabel(meta.get('exportedByURL', ""))

        self.line = QFrame()

        self.bottomLayout = QHBoxLayout()

        self.settingsButton = QPushButton("⚙ " + i18n("Settings") ) # pylint: disable=undefined-variable

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.kritaInstance = krita.Krita.instance()
        self.documentsList = []

        self.directoryTextField.setReadOnly(True)
        self.directoryDialogButton.clicked.connect(self._selectDir)
        self.widgetDocuments.currentRowChanged.connect(self._setResolution)
        self.refreshButton.clicked.connect(self.refreshButtonClicked)
        self.buttonBox.accepted.connect(self.confirmButton)
        self.buttonBox.rejected.connect(self.close)
        self.cropToImageBounds.stateChanged.connect(self._toggleCropSize)
        self.flattenImageCheckbox.stateChanged.connect(self._toggleFlatten)
        self.settingsButton.clicked.connect(self.settingsButtonClicked)

        self.setWindowModality(Qt.NonModal)
        self.widgetDocuments.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.widgetDocuments.setSelectionMode(QAbstractItemView.MultiSelection)

    def initialize(self):
        """Loads  the documents and sets default values to the UI"""
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

        self.metadataLayout.addRow(i18n("Author:"), self.authorEdit) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("Description:"), self.descriptionEdit) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("Copyright:"), self.copyrightEdit) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("License short name:"), self.licenseEdit) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("License complete name:"), self.licenseLongEdit) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("License URL:"), self.licenseURLEdit) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("Creation date:"), self.createdLabel) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("Origin app:"), self.originAppLabel) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("Origin app version:"), self.originAppVersionLabel) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("Export add-on:"), self.exportedByLabel) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("Export add-on URI:"), self.exportedByIDLabel) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("Export add-on maintainer:"), self.exportedByOrgLabel) # pylint: disable=undefined-variable
        self.metadataLayout.addRow(i18n("Export add-on URL:"), self.exportedByURLabel) # pylint: disable=undefined-variable

        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.line)
        self.mainLayout.addLayout(self.bottomLayout)
        self.bottomLayout.addWidget(self.settingsButton)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.buttonBox)

        self.resize(500, 300)
        self.setWindowTitle(i18n("OCA Export ") + " v" + self.version) # pylint: disable=undefined-variable
        self.setSizeGripEnabled(True)
        self.show()
        self.activateWindow()

    def closeEvent(self, event):
        """Accept close"""
        event.accept()

    def settingsButtonClicked(self):
        d = SettingsDialog(self)
        d.exec()

    def loadDocuments(self):
        self.widgetDocuments.clear()

        self.documentsList = [
            document for document in self.kritaInstance.documents()
            if document.fileName()
        ]

        activeDoc = Application.activeDocument() # pylint: disable=undefined-variable

        for document in self.documentsList:
            item = QListWidgetItem (
                QIcon(QPixmap.fromImage(document.thumbnail(128,128))),
                document.fileName(),
                self.widgetDocuments
                )
            if document == activeDoc:
                item.setSelected(True)
        
        # If the path is empty, set to the path of the active doc
        if self.directoryTextField.text() == "":
            fileName = activeDoc.fileName()
            self.directoryTextField.setText(
                os.path.dirname(fileName)
            )

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

    def export(self, document):

        oca.kDocument.export( document, self.directoryTextField.text(), {
                                    'fullClip': self.fullClipRadioButton.isChecked(),
                                    'flattenImage': self.flattenImageCheckbox.isChecked(),
                                    'exportReference': self.exportReferenceCheckbox.isChecked(),
                                    'exportFilterLayers': self.exportFilterLayersCheckBox.isChecked(),
                                    'exportInvisibleLayers': self.exportInvisibleLayersCheckBox.isChecked(),
                                    'cropToImageBounds': self.cropToImageBounds.isChecked(),
                                    'width': self.rectWidthSpinBox.value(),
                                    'height': self.rectHeightSpinBox.value(),
                                    'resolution': self.resSpinBox.value() / 72.0,
                                },
                                {
                                    'author': self.authorEdit.text(),
                                    'copyright': self.copyrightEdit.text(),
                                    'description': self.descriptionEdit.toPlainText(),
                                    'license': self.licenseEdit.text(),
                                    'licenseLong': self.licenseLongEdit.text(),
                                    'licenseURL': self.licenseURLEdit.text(),
                                } )

    def _selectDir(self):
        current = self.directoryTextField.text()
        if current == "":
            current = os.path.expanduser("~")

        directory = QFileDialog.getExistingDirectory(
            self,
            i18n("Select a Folder"), # pylint: disable=undefined-variable
            current,
            QFileDialog.ShowDirsOnly)
        
        if directory != "":
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
