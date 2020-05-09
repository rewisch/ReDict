import os

from PyQt5.QtWidgets import QDialog, QCheckBox
from PyQt5 import QtGui

from src.gui.all_windows import AllWindows
from PyQt5 import uic

class Dicts(QDialog, AllWindows):
    def __init__(self):
        QDialog.__init__(self)
        AllWindows.__init__(self)
        self.checkboxCounter = 1
        self.init_ui()
        self.load_form_pers(self)

    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath('_gui/dicts.ui'), self)

        ret = self.db.get_dictionaries()
        self.values = self.db.get_property(1)
        self.values = self.values.split(',')

        for r in ret:
            dictionary_id = r[0]
            dictionary_name = r[1]
            self.add_checkbox(dictionary_id, str(dictionary_id) + ': ' + dictionary_name)

    def add_checkbox(self, id, name):
        b = QCheckBox(name, self, objectName= 'test')
        font = QtGui.QFont()
        font.setPointSize(14)
        b.setFont(font)
        if str(id) in self.values:
            b.setChecked(True)
        b.stateChanged.connect(self.handle_checkboxes)
        self.ui.gridLayout.addWidget(b, self.checkboxCounter, self.checkboxCounter % 1)
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