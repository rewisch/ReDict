from PyQt5.QtCore import QObject, pyqtSignal

class MySignal(QObject):
    sig_no_args = pyqtSignal()
    sig_with_str = pyqtSignal(str)
    stopLoading = pyqtSignal()
    startLoading = pyqtSignal()