import os

from PyQt5.QtWidgets import QDialog, QScroller

from src.gui.all_windows import AllWindows
from PyQt5 import uic


class About(QDialog, AllWindows):
    def __init__(self):
        QDialog.__init__(self)
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath('_gui/about.ui'), self)
        QScroller.grabGesture(self.textBrowser.viewport(), QScroller.LeftMouseButtonGesture)
        self.ui.show()