import os
from math import ceil

from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QThreadPool, QEvent, QTimer, QStringListModel
from PyQt5.QtWidgets import QAction, qApp, QScroller, QCompleter, QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QColor, QTextCursor

from src.database.database import Database
from src.autocompleter.dwg import AutoComplete
from src.gui.waitingspinner import QtWaitingSpinner
from src.database.search import Search
from src.gui.all_windows import AllWindows
from src.misc.mysignal import MySignal
from src.gui.lookup import LookupDialog
from src.gui.history import History
from src.gui.about import About
from src.gui.settings import Settings_
from src.misc.worker import Worker
from src.misc.tools import clpboard_cleanse
from src.misc.completerdelegate import CompleterDelegate

subThread = True
autocomplete = None
clipboard_event = 0


class MainWindow(QMainWindow, AllWindows):
    def __init__(self):
        """
        The .ui File has the following objects:
        MainWindow --> QMainWindow
            centralwidget --> QWidget
                txtSearch --> QLineEdit
                txtResult --> QTextEdit
                chkLike --> QCheckBox
                btnSearch --> QPushButton
            menubar --> QMenuBar
                menuReDict --> QMenu
                    actionSettings --> QAction
                    actionQuit --> QAction
                menuView --> QMenu
                    actionZoomIn --> QAction
                    actionZoomOut --> QAction
                menuHistory --> QMenu
                    actionHistory --> QAction
                menuHelp --> QMenu
                    actionAbout --> QAction
            statusbar --> QStatusBar
        """
        super(QMainWindow, self).__init__()
        super(AllWindows, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath("_gui/main.ui"), self)
        self.search = Search()
        self.load_form_pers(self)
        self.signal = MySignal()

        self.ui.btnSearch.clicked.connect(self.search_word)

        # Read Font-Size from Settings and apply to Result
        self.font = QtGui.QFont()
        self.font.setPointSize(int(self.db.get_property(2)))
        self.ui.txtResult.setFont(self.font)

        # MenuBar
        self.ui.menubar.setNativeMenuBar(False)
        self.txtSearch.textEdited.connect(self.txt_search_changed)

        exitAct = self.ui.actionQuit
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.exit)

        zoominAct = self.ui.actionZoomIn
        zoominAct.setShortcut('Ctrl++')
        zoominAct.triggered.connect(self.zoom_in)

        zoomoutAct = self.ui.actionZoomOut
        zoomoutAct.setShortcut('Ctrl+-')
        zoomoutAct.triggered.connect(self.zoom_out)

        HistoryAct = self.ui.actionHistory
        HistoryAct.triggered.connect(self.history)

        AboutAct = self.ui.actionAbout
        AboutAct.triggered.connect(self.about)

        SettingsAct = self.ui.actionSettings
        SettingsAct.triggered.connect(self.settings_)

        self.signal.startLoading.connect(self.loading)
        self.signal.stopLoading.connect(self.stop_loading)

        self.threadpool = QThreadPool()
        self.open_thread()

        self.completer = QCompleter([])
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.activated.connect(self.search_word)
        model = QStringListModel()
        self.completer.setModel(model)
        delegate = CompleterDelegate(self.ui.txtSearch)
        self.completer.popup().setItemDelegate(delegate)
        self.completer.popup().setFont(self.font)
        self.txtSearch.setCompleter(self.completer)

        self.ui.txtResult.setContextMenuPolicy(Qt.ActionsContextMenu)

        lookup = QAction("look-up", self)
        lookup.triggered.connect(self.look_up)
        self.ui.txtResult.addAction(lookup)

        self.spinner = QtWaitingSpinner(self, True, True, Qt.ApplicationModal)
        self.spinner.setInnerRadius(150)
        self.spinner.setNumberOfLines(50)
        self.spinner.setColor(QColor(230, 126, 34))

        self.ui.txtSearch.setFocus()

        self.ui.txtResult.installEventFilter(self)
        self.ui.txtResult.grabGesture(Qt.PinchGesture)
        self.ui.txtResult.grabGesture(Qt.TapAndHoldGesture)

        QScroller.grabGesture(self.txtResult.viewport(), QScroller.LeftMouseButtonGesture)

        clipboard_enabled = self.db.get_property(5)
        if clipboard_enabled == '1':
            self.clip = QApplication.clipboard()
            # on Mac unfortunately this event will only be fired when the application
            # is active, i.e. not in background. On Windows it works fine. It might
            # have to come back to a timer with an endless for loop which checks with
            # paste whether something has changed. But how then to count Ctrl-C presses?
            self.clip.changed.connect(self.clipboard_changed)

            self.timer = QTimer()
            self.timer.timeout.connect(self.watch_clipboard)
            seconds = int(self.db.get_property(6))
            self.timer.start(seconds * 1000)

    def watch_clipboard(self):
        global clipboard_event
        clipboard_event = 0

    def clipboard_changed(self):
        global clipboard_event
        clipboard_event += 1
        setting = int(self.db.get_property(7))
        if clipboard_event == setting:
            word = clpboard_cleanse(self.clip.text())
            cursor = self.txtResult.textCursor()
            sel = cursor.selectedText()
            if word != sel:
                self.search_word(word)
            self.bring_to_front()

    def eventFilter(self, o, event):
        # handle gesture event from txtResult
        if event.type() != QEvent.Gesture:
            return False
        fontsize = int(self.db.get_property(2))
        g = event.gesture(Qt.PinchGesture)
        f = event.gesture(Qt.TapAndHoldGesture)
        # handle pinch
        if g != None:
            scale = g.scaleFactor()
            fontsize = ceil(fontsize * scale)
            self.zoom_fix(fontsize)
            self.ui.update()
        # handle tap
        elif f != None:
            c = self.ui.txtResult.textCursor()
            if c.selectedText() == '':
                c.movePosition(QTextCursor.StartOfWord, QTextCursor.MoveAnchor)
                c.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
                self.ui.txtResult.setTextCursor(c)
        return True

    def loading(self):
        self.spinner.start()

    def stop_loading(self):
        self.spinner.stop()
        self.txtSearch.setPlaceholderText("Enter word...")
        self.txtSearch.setFocus()

    def txt_search_changed(self, changeValue):
        global autocomplete
        entries = []
        names = autocomplete.search(word=changeValue, max_cost=3, size=10)
        for name in names:
            entries.append(name[0])
        model = self.completer.model()
        model.setStringList(entries)

    def open_thread(self):
        worker = Worker(self.initialize_things)
        self.threadpool.start(worker)

    def initialize_things(self):
        self.signal.startLoading.emit()

        db = Database()
        prop = db.get_property(4)
        global autocomplete

        sql = ('SELECT DISTINCT Word  FROM Word' if prop == 'Lemmata' else 'SELECT Flection FROM Flection')
        cmwords = db.read_database(sql)

        words = {}
        for r in cmwords:
            words.setdefault(r[0], {})
        del cmwords
        autocomplete = AutoComplete(words=words)
        self.signal.stopLoading.emit()

    def bring_to_front(self):
        """ Brings the window to the front and places the cursor in the textbox """
        self.txtSearch.setFocus()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.raise_()
        self.activateWindow()
        self.show()

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Return:
            self.search_word(self.ui.txtSearch.text().lower())
        else:
            super().keyPressEvent(qKeyEvent)

    def exit(self):
        global subThread
        subThread = False
        qApp.quit()

    def about(self):
        About()

    def settings_(self):
        Settings_()

    def search_word(self, word=False):
        self.ui.txtResult.clear()
        if not word:
            wrd = self.ui.txtSearch.text().lower()
            result = self.search.search_word(wrd, self.ui.chkLike.checkState())
        else:
            self.ui.txtSearch.setText(word.lower())
            result = self.search.search_word(word, self.ui.chkLike.checkState())
        self.set_result(result)
        self.ui.txtSearch.selectAll()

    def set_result(self, result):
        self.ui.txtResult.append(result)
        self.ui.txtResult.moveCursor(QtGui.QTextCursor.Start)

    def look_up(self):
        cursor = self.txtResult.textCursor()
        LookupDialog(cursor.selectedText()).search_word()

    def set_result(self, result: object):
        self.ui.txtResult.append(result)
        self.ui.txtResult.moveCursor(QtGui.QTextCursor.Start)

    def zoom_out(self):
        size = int(self.db.get_property(2)) - 1
        self.font.setPointSize(size)
        self.ui.txtResult.setFont(self.font)
        self.db.set_property(2, size)

    def zoom_in(self):
        size = int(self.db.get_property(2)) + 1
        self.font.setPointSize(size)
        self.ui.txtResult.setFont(self.font)
        self.db.set_property(2, size)

    def zoom_fix(self, size: int) -> None:
        self.font.setPointSize(size)
        self.ui.txtResult.setFont(self.font)
        self.db.set_property(2, size)
        return None

    def history(self):
        History(self.search_word)

    def closeEvent(self, event):
        global subThread
        subThread = False
        self.save_form_pers(self)
        QtWidgets.QMainWindow.closeEvent(self, event)
