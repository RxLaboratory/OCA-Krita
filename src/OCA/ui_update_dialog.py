"""The Dialog used to warn an update is available, and show details about it"""

from PyQt5.QtWidgets import ( # pylint: disable=import-error disable=no-name-in-module
    QDialog,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton
)
from PyQt5.QtGui import ( # pylint: disable=no-name-in-module,import-error
    QDesktopServices,
)
from PyQt5.QtCore import ( # pylint: disable=no-name-in-module
    QUrl
)

class UpdateDialog( QDialog ):
    """The dialog to show details about an update"""

    def __init__(self, updateInfo, toolName, toolVersion, parent=None):
        if parent is None:
            parent = Application.activeWindow().qwindow() # pylint: disable=undefined-variable
        super(UpdateDialog, self).__init__(parent)
        self.__setupUi(updateInfo, toolName, toolVersion)

    def __setupUi(self, updateInfo, toolName, toolVersion):
        self.setModal(True)

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(3)
        self.setLayout(mainLayout)

        if updateInfo.get("update", False):
            self.setWindowTitle("New " + toolName + " available!" )

            latestVersionLabel = QLabel("version: " + updateInfo.get("version") )
            mainLayout.addWidget(latestVersionLabel)

            descriptionEdit = QTextEdit()
            descriptionEdit.setMarkdown(updateInfo.get("description"))
            descriptionEdit.setReadOnly(True)
            mainLayout.addWidget(descriptionEdit)

            currentVersionLabel = QLabel("Current version: " + toolVersion )
            currentVersionLabel.setEnabled(False)
            mainLayout.addWidget(currentVersionLabel)

            self.__downloadURL = updateInfo.get("downloadURL", "")
            if self.__downloadURL != "":
                self.__ui_downloadButton = QPushButton("↧ Download")
                mainLayout.addWidget(self.__ui_downloadButton)
                self.__ui_downloadButton.clicked.connect(self.download)

            self.__changelogURL = updateInfo.get("changelogURL", "")
            if self.__changelogURL != "":
                self.__ui_changelogButton = QPushButton("☷ Changelog")
                mainLayout.addWidget(self.__ui_changelogButton)
                self.__ui_changelogButton.clicked.connect(self.changelog)

            self.__donateURL = updateInfo.get("donateURL", "")
            if self.__donateURL != "":
                self.__ui_donateButton = QPushButton("I ♥ " + toolName)
                mainLayout.addWidget(self.__ui_donateButton)
                self.__ui_donateButton.clicked.connect(self.donate)

            self.__ui_okButton = QPushButton("✕ Close")
            mainLayout.addWidget(self.__ui_okButton)
            self.__ui_okButton.clicked.connect(self.reject)
        elif updateInfo.get("accepted", False):
            self.setWindowTitle( "Update" )

            versionLabel = QLabel("I'm already up-to-date!" )
            mainLayout.addWidget(versionLabel)

            self.__ui_okButton = QPushButton("✕ Close")
            mainLayout.addWidget(self.__ui_okButton)
            self.__ui_okButton.clicked.connect(self.reject)
        elif not updateInfo.get("success", False):
            self.setWindowTitle( "Server error" )
            label = QLabel("Sorry, the server could not get update information." )
            mainLayout.addWidget(label)

            descriptionEdit = QTextEdit(updateInfo.get("description", ""))
            descriptionEdit.setReadOnly(True)
            mainLayout.addWidget(descriptionEdit)

            self.__ui_okButton = QPushButton("✕ Close")
            mainLayout.addWidget(self.__ui_okButton)
            self.__ui_okButton.clicked.connect(self.reject)
        else:
            self.setWindowTitle( "Server error" )
            label = QLabel("Sorry, there was a server error." )
            mainLayout.addWidget(label)

            self.__ui_okButton = QPushButton("✕ Close")
            mainLayout.addWidget(self.__ui_okButton)
            self.__ui_okButton.clicked.connect(self.reject)

    def download(self):
        """Opens the download URL"""
        QDesktopServices.openUrl ( QUrl( self.__downloadURL ) )
        self.close()

    def changelog(self):
        """Opens the changelog URL"""
        QDesktopServices.openUrl ( QUrl( self.__changelogURL ) )
        self.close()

    def donate(self):
        """Opens the donate URL"""
        QDesktopServices.openUrl ( QUrl( self.__donateURL ) )
        self.close()
