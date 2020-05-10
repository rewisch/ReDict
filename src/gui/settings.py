import os

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

from src.gui.all_windows import AllWindows



class Settings_(QDialog, AllWindows):
    def __init__(self):
        QDialog.__init__(self)
        self.init_ui()
        self.load_form_pers(self)

    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath('_gui/settings.ui'), self)
        self.load_form()
        self.ui.show()

    def load_form(self):

        self.clipboard_enabled_load = self.db.get_property(5)
        self.clipboard_seconds_load = self.db.get_property(6)

        if self.clipboard_enabled_load == 'True':
            self.ui.clipboardEnable.setChecked(True)
        self.ui.txtSeconds.setText(self.clipboard_seconds_load)

    def closeEvent(self, event):
        if self.ui.clipboardEnable.isChecked():
            self.clipboard_enabled = 'True'
        else:
            self.clipboard_enabled = 'False'

        self.db.set_property(5, self.clipboard_enabled)
        self.db.set_property(6, self.ui.txtSeconds.text())

        self.save_form_pers(self)

        if (self.clipboard_enabled_load != self.clipboard_enabled or
            self.clipboard_seconds_load != self.ui.txtSeconds.text()):
            qb = QMessageBox
            qb.warning(self, 'Message', 'Please restart the application.')

