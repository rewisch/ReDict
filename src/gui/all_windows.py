from PyQt5.QtCore import QSettings
from src.database.database import Database



class AllWindows():
    def __init__(self):
        self.db = Database()
        self.load_form_pers(self)

    def load_form_pers(self, _class):

        Dialog = type(_class).__name__

        _class.settings = QSettings("Redict", Dialog)
        if _class.settings.value("geometry") != None:
            _class.restoreGeometry(_class.settings.value("geometry"))
        if _class.settings.value("windowState") != None:
            _class.restoreState(_class.settings.value("windowState"))

    def save_form_pers(self, _class):
        _class.settings.setValue("geometry", _class.saveGeometry())
        if type(_class).__name__ == 'MainWindow':
            _class.settings.setValue("windowState", _class.saveState())

    def closeEvent(self, event):
        self.save_form_pers(self)
