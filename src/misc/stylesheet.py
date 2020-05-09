from PyQt5.QtCore import QFile, QTextStream
def load_stylesheet():
    file = QFile("_gui/stylesheets/AMOLED.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    return stream.readAll()