import os

from PyQt5.QtWidgets import QDialog, QScroller

from src.gui.all_windows import AllWindows
from PyQt5 import uic


class Completer(QDialog, AllWindows):
    def __init__(self):
        QDialog.__init__(self)
        AllWindows.__init__(self)
        self.load_form_pers(self)
        self.changed = False
        self.init_ui()



    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath('_gui/completer.ui'), self)
        QScroller.grabGesture(self.textEdit.viewport(), QScroller.LeftMouseButtonGesture)

        self.prop = self.db.get_property(4)
        if self.prop == self.ui.rbtnLemmata.text():
            self.ui.rbtnLemmata.setChecked(True)
        else:
            self.ui.rbtnDeclinedWords.setChecked(True)

        self.ui.show()

    def closeEvent(self, event):
        if self.ui.rbtnLemmata.isChecked():
             new = self.ui.rbtnLemmata.text()
        else:
            new = self.ui.rbtnDeclinedWords.text()

        if self.prop != new:
            self.db.set_property(4, new)
            self.changed = True

        self.save_form_pers(self)