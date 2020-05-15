import sys

from PyQt5 import QtWidgets

from src.gui.mainwindow import MainWindow
import src.misc.stylesheet as s
try:
    from src.construction.Initialize import Initialize
    init = Initialize()
    init.create_Database()
except:
    print('Failed to import Initialize. The database can not be created')


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(s.load_stylesheet())

    sd = MainWindow()
    sd.show()

    sys.exit(app.exec())