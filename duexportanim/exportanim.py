# This script was made from export layers / GNU GPL v3

import krita
from . import uiexportanim


class ExportAnimExtension(krita.Extension):

    def __init__(self, parent):
        super(ExportAnimExtension, self).__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("export_anim", i18n("Export Animation"))
        action.setToolTip(i18n("Export animation keyframes from a document."))
        action.triggered.connect(self.initialize)

    def initialize(self):
        self.uiexportanim = uiexportanim.UIExportAnim()
        self.uiexportanim.initialize()
