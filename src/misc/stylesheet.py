from PyQt5.QtCore import QFile, QTextStream
from src.database.database import Database
def load_stylesheet():
    db = Database()
    stylesheet = db.get_property(3)
    db.db_connection.close()
    file = QFile(f"_gui/stylesheets/{stylesheet}")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    return stream.readAll()