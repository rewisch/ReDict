from PyQt5.QtWidgets import  QStyledItemDelegate
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

class CompleterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(CompleterDelegate, self).initStyleOption(option, index)
        option.backgroundBrush = QColor("gray")
        option.palette.setBrush(QPalette.Text, QColor('black'))
        option.displayAlignment = Qt.AlignLeft