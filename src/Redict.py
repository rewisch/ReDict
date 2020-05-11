import sys

from PyQt5 import QtWidgets

from src.gui.mainwindow import MainWindow
import src.misc.stylesheet as s
from src.construction.Initialize import Initialize

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(s.load_stylesheet())

    init = Initialize()
    init.create_Database()

    sd = MainWindow()
    sd.show()

    sys.exit(app.exec())