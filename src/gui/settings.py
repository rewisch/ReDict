import os

from PyQt5.QtWidgets import QDialog, QMessageBox, QCheckBox, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5 import uic

from src.gui.all_windows import AllWindows


class Settings_(QDialog, AllWindows):
    def __init__(self):
        QDialog.__init__(self)
        self.load_form_pers(self)
        self.init_ui()


    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath('_gui/settings.ui'), self)
        self.load_clipboard()
        self.load_dictionaries()
        self.load_completer()
        self.load_search()
        self.ui.show()

    def load_clipboard(self):
        self.clipboard_enabled_load = self.db.get_property(5)
        self.clipboard_seconds_load = self.db.get_property(6)
        self.clipboard_times_load = self.db.get_property(7)

        if self.clipboard_enabled_load == '1':
            self.ui.clipboardEnable.setChecked(True)
        self.ui.txtSeconds.setText(self.clipboard_seconds_load)
        self.ui.txtTimes.setText(self.clipboard_times_load)

    def load_dictionaries(self):
        self.checkboxCounter = 1
        ret = self.db.get_dictionaries()
        self.values = self.db.get_property(1)
        self.values = self.values.split(',')
        self.layout = QGridLayout()
        for r in ret:
            dictionary_id = r[0]
            dictionary_name = r[1]
            self.add_checkbox(dictionary_id, str(dictionary_id) + ': ' + dictionary_name)
        self.tabWidget.widget(0).setLayout(self.layout)

    def load_completer(self):
        prop = self.db.get_property(4)
        if prop == self.ui.rbtnLemmata.text():
            self.ui.rbtnLemmata.setChecked(True)
        else:
            self.ui.rbtnDeclinedWords.setChecked(True)

    def load_search(self):
        prop = int(self.db.get_property(8))
        if prop:
            self.ui.abstractEnabled.setChecked(True)

    def add_checkbox(self, id, name):
        b = QCheckBox(name, self, objectName='checkbox')
        font = QFont()
        font.setPointSize(14)
        b.setFont(font)
        if str(id) in self.values:
            b.setChecked(True)
        b.stateChanged.connect(self.handle_checkboxes)
        self.layout.addWidget(b, self.checkboxCounter, self.checkboxCounter % 1)
        self.checkboxCounter += 1

    def handle_checkboxes(self, state):
        sender = self.sender()
        db_id = sender.text().split(':')[0]

        if state == 2:
            if db_id not in self.values:
                self.values.append(db_id)
        elif state == 0:
            if len(self.values) == 1:
                sender.setChecked(True)
            elif db_id in self.values:
                self.values.remove(db_id)
        self.db.set_property(1, ','.join(self.values))

    def something_changed(self):
        if self.clipboard_enabled_load != self.clipboard_enabled:
            return True
        elif self.clipboard_seconds_load != self.ui.txtSeconds.text():
            return True
        return False

    def closeEvent(self, event):
        self.save_completer()
        self.save_clipboard()
        self.save_search()
        self.save_form_pers(self)

        if self.something_changed():
            qb = QMessageBox
            qb.warning(self, 'Message', 'Please restart the application.')

    def save_completer(self):
        if self.ui.rbtnLemmata.isChecked():
            new = self.ui.rbtnLemmata.text()
        else:
            new = self.ui.rbtnDeclinedWords.text()
        self.db.set_property(4, new)

    def save_clipboard(self):
        if self.ui.clipboardEnable.isChecked():
            self.clipboard_enabled = '1'
        else:
            self.clipboard_enabled = '0'

        self.db.set_property(5, self.clipboard_enabled)
        self.db.set_property(6, self.ui.txtSeconds.text())
        self.db.set_property(7, self.ui.txtTimes.text())

    def save_search(self):
        if self.ui.abstractEnabled.isChecked():
            abstract_enabled = '1'
        else:
            abstract_enabled = '0'
        self.db.set_property(8, abstract_enabled)



