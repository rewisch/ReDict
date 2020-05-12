import os

from PyQt5.QtWidgets import QDialog, QScroller, QScrollArea
from PyQt5 import uic

from src.gui.all_windows import AllWindows



class History(QDialog, AllWindows):
    def __init__(self, searchFunc):
        QDialog.__init__(self)
        self.init_ui()
        self.searchFunc = searchFunc
        self.load_form_pers(self)

    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath('_gui/history.ui'), self)

        self.ui.listWidget.itemDoubleClicked.connect(self.double_click)
        self.ui.btnClearHistory.clicked.connect(self.clear)
        self.loadList()
        self.ui.show()

    def double_click(self):
        word = self.ui.listWidget.currentItem().text()
        self.searchFunc(word)

    def loadList(self):
        history = self.db.get_history()
        self.ui.listWidget.clear()
        for i, word in enumerate(history):
            self.ui.listWidget.insertItem(i, word[0])

    def clear(self):
        self.db.clear_history()
        self.loadList()