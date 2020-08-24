# This script was made from export layers / GNU GPL v3

from PyQt5.QtWidgets import QDialog

class ExportAnimDialog(QDialog):

    def __init__(self, parent=None):
        super(ExportAnimDialog, self).__init__(parent)

    def closeEvent(self, event):
        event.accept()
