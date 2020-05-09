import os
from math import ceil
import time

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QThreadPool, QEvent
from PyQt5.QtWidgets import QAction, qApp, QScroller, QCompleter
from PyQt5.QtGui import QColor, QIcon
import pyperclip

from src.database.database import Database
from src.autocompleter.dwg import AutoComplete
from src.gui.WaitingSpinner import QtWaitingSpinner
from src.database.search import Search
from src.gui.all_windows import AllWindows
from src.misc.mysignal import MySignal
from src.gui.lookup import LookupDialog
from src.gui.history import History
from src.gui.dicts import Dicts
from src.gui.about import About
from src.misc.worker import Worker
from src.misc.completer import Completer

subThread = True
autocomplete = None

class MainWindow(QMainWindow, AllWindows):
    def __init__(self):
        QMainWindow.__init__(self)
        AllWindows.__init__(self)

        self.init_ui()


    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath("_gui/main.ui"), self)
        self.search = Search()
        self.SetComp = True
        self.load_form_pers(self)
        self.signal = MySignal()

        self.ui.btnGo.clicked.connect(self.search_word)


        #Read Font-Size from Settings and apply to Result
        self.font = QtGui.QFont()
        self.font.setPointSize(int(self.db.get_property(2)))
        self.ui.txtResult.setFont(self.font)


        #MenuBar
        self.ui.menubar.setNativeMenuBar(False)

        self.txtSearch.textEdited.connect(self.txt_search_changed)

        exitAct = self.ui.actionQuit
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.exit)

        exitAct = self.ui.actionCompleter
        exitAct.triggered.connect(self.completer)

        zoominAct = self.ui.actionZoom_In
        zoominAct.setShortcut('Ctrl++')
        zoominAct.triggered.connect(self.zoom_in)

        zoomoutAct = self.ui.actionZoom_Out
        zoomoutAct.setShortcut('Ctrl+-')
        zoomoutAct.triggered.connect(self.zoom_out)

        DictionariesAct = self.ui.actionDictionaries
        DictionariesAct.triggered.connect(self.dlg_dicts)

        HistoryAct = self.ui.actionManage_History
        HistoryAct.triggered.connect(self.history)

        AboutAct = self.ui.actionAbout_redict
        AboutAct.triggered.connect(self.about)

        #Create Signal and Threads for ClipboardChecker

        self.signal.sig_with_str.connect(self.handle_signal)
        self.signal.startLoading.connect(self.loading)
        self.signal.stopLoading.connect(self.stop_loading)

        self.threadpool = QThreadPool()
        self.open_thread()
        self.open_thread2()

        self.completer = QCompleter([])
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.activated.connect(self.search_word)
        self.txtSearch.setCompleter(self.completer)


        self.ui.txtResult.setContextMenuPolicy(Qt.ActionsContextMenu)

        lookup = QAction(QIcon('_gui/tbLookup.png'), "look-up", self)
        lookup.triggered.connect(self.look_up)
        self.ui.txtResult.addAction(lookup)

        self.spinner = QtWaitingSpinner(self, True, True, Qt.ApplicationModal)
        self.spinner.setColor(QColor(200, 200, 71))

        self.ui.txtSearch.setFocus()

        self.ui.txtResult.installEventFilter(self)
        self.ui.txtResult.grabGesture(Qt.PinchGesture)
        #self.ui.txtResult.grabGesture(Qt.TapAndHoldGesture)

        QScroller.grabGesture(self.txtResult.viewport(), QScroller.LeftMouseButtonGesture)

    def eventFilter(self, o, event):
        #handle pinch event from txtResult
        if event.type() == QEvent.Gesture:
            fontsize = int(self.db.get_property(2))
            g = event.gesture(Qt.PinchGesture)
            f = event.gesture(Qt.TapAndHoldGesture)
            scale = g.scaleFactor()
            fontsize = ceil(fontsize * scale)
            self.zoom_fix(fontsize)
            self.ui.update()
            return True
        elif 0 == 0:
            pass
        return False

    def loading(self):
        self.spinner.start()
    def stop_loading(self):
        self.spinner.stop()
        self.txtSearch.setPlaceholderText("Enter the word you want to look-up")
        self.txtSearch.setFocus()

    def check_clipboard(self):
        global subThread
        recent_value = pyperclip.paste()
        while subThread:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                self.signal.sig_with_str.emit(recent_value.lstrip().rstrip().replace(',', '').replace('.', ''))
            time.sleep(0.1)

    def txt_search_changed(self, changeValue):
        global autocomplete
        entries = list()
        names = autocomplete.search(word=changeValue, max_cost=3, size=10)
        for name in names:
            entries.append(name[0])
        model = self.completer.model()
        model.setStringList(entries)

    def open_thread(self):
        worker = Worker(self.check_clipboard)
        self.threadpool.start(worker)

    def open_thread2(self):
        worker2 = Worker(self.initialize_things)
        self.threadpool.start(worker2)

    def initialize_things(self):
        self.signal.startLoading.emit()
        db = Database()
        prop = db.get_property(4)
        global autocomplete

        if prop == 'Lemmata':
            cmwords = db.read_database('Select distinct Word  From Word')
        else:
            cmwords = db.read_database('Select Flection From Flection')

        words = dict()
        for r in cmwords:
            words.setdefault(r[0], {})
        del cmwords
        autocomplete = AutoComplete(words=words)
        self.signal.stopLoading.emit()

    def handle_signal(self, word):
        cursor = self.txtResult.textCursor()
        sel = cursor.selectedText()
        if word != sel:
            self.search_word(word)
        self.bring_to_front()

    def bring_to_front(self):
            """ Brings the terminal window to the front and places the cursor in the textbox """
            self.txtSearch.setFocus()
            self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
            self.raise_()
            self.activateWindow()

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

    def search_word(self, word = False):
        self.ui.txtResult.clear()
        if not word:
            wrd = self.ui.txtSearch.text().lower()
            result = self.search.search_word(wrd, self.ui.ckboxLike.checkState())
        else:
            self.ui.txtSearch.setText(word.lower())
            result = self.search.search_word(word, self.ui.ckboxLike.checkState())
        self.set_result(result)

    def set_result(self, result):
        self.ui.txtResult.append(result)
        self.ui.txtResult.moveCursor(QtGui.QTextCursor.Start)

    def look_up(self):
        cursor = self.txtResult.textCursor()
        word = cursor.selectedText()
        if word == '':
            return
        else:
            LookupDialog(word)

    def set_result(self, result):
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


    def zoom_fix(self, size):
        self.font.setPointSize(size)
        self.ui.txtResult.setFont(self.font)
        self.db.set_property(2, size)

    def dlg_dicts(self):
        self.dlgDict = Dicts()
        self.dlgDict.show()

    def history(self):
        History(self.search_word)

    def completer(self):
        Completer()
    def closeEvent(self, event):
        global subThread
        subThread = False
        self.save_form_pers(self)
        QtWidgets.QMainWindow.closeEvent(self, event)