import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QDialog, QScroller, QAction
from PyQt5 import uic, QtGui

from src.gui.all_windows import AllWindows
from src.database.search import Search


class LookupDialog(QDialog, AllWindows):
    def __init__(self, word):
        QDialog.__init__(self)
        AllWindows.__init__(self)
        self.init_ui()
        self.search = Search()
        self.search_word(word)
        self.load_form_pers(self)

    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath("_gui/lookup.ui"), self)
        self.font = QtGui.QFont()
        self.font.setPointSize(int(self.db.get_property(2)))
        self.ui.txtResultLookup.setFont(self.font)
        self.create_contextmenu()
        QScroller.grabGesture(self.txtResultLookup.viewport(), QScroller.LeftMouseButtonGesture)
        self.show()

    def search_word(self, word):
        self.ui.txtResultLookup.clear()
        wrd = word.lower()
        result = self.search.search_word(wrd, False)
        self.set_result(result)

    def set_result(self, result):
        self.ui.txtResultLookup.append(result)
        self.ui.txtResultLookup.moveCursor(QtGui.QTextCursor.Start)

    def create_contextmenu(self):
        self.ui.txtResultLookup.setContextMenuPolicy(Qt.ActionsContextMenu)
        lookup = QAction("look-up", self)
        lookup.triggered.connect(self.look_up)
        self.ui.txtResultLookup.addAction(lookup)

    def look_up(self):
        cursor = self.txtResultLookup.textCursor()
        word = cursor.selectedText()
        if word == '':
            return
        else:
            LookupDialog(word)