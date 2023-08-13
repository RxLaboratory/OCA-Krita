"""The settings dialog for the OCA Plugin"""

from PyQt5.QtWidgets import ( # pylint: disable=import-error disable=no-name-in-module
    QDialog,
    QVBoxLayout,
    QCheckBox,
    QPushButton,
    QFrame
)
from . import update
from . import config

class SettingsDialog( QDialog ):
    """The dialog to show the settings"""

    def __init__(self, parent=None):
        if parent is None:
            parent = Application.activeWindow().qwindow() # pylint: disable=undefined-variable
        super().__init__()

        self.__setupUi()
        self.__connectEvents()

    def __setupUi(self):

        self.setWindowTitle(i18n("OCA Settings")) # pylint: disable=undefined-variable

        layout = QVBoxLayout(self)

        self.dailyUpdateButton = QCheckBox(i18n("Daily check for updates")) # pylint: disable=undefined-variable
        self.dailyUpdateButton.setChecked( self.dailyUpdateCheck() )
        layout.addWidget(self.dailyUpdateButton)

        self.updateButton = QPushButton(i18n("Check for update now")) # pylint: disable=undefined-variable
        layout.addWidget(self.updateButton)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(self.line)

        self.closeButton = QPushButton(i18n("✕ Close")) # pylint: disable=undefined-variable
        layout.addWidget(self.closeButton)

    def __connectEvents(self):
        self.dailyUpdateButton.clicked.connect(self.__setDailyUpdateCheck)
        self.updateButton.clicked.connect(self.__checkUpdate)
        self.closeButton.clicked.connect(self.close)

    def dailyUpdateCheck(self):
        """True if we must check daily for updates"""
        c = Application.readSetting("OCA-Krita", "dailyUpdateCheck", "True") # pylint: disable=undefined-variable
        if c == "True":
            return True
        return False

    def __setDailyUpdateCheck(self, checked):
        c = "False"
        if checked:
            c = "True"

        Application.writeSetting("OCA-Krita", "dailyUpdateCheck", c) # pylint: disable=undefined-variable

    def __checkUpdate(self):
        update.checkUpdate( "OCA-Krita", config.VERSION, discreet=False)
