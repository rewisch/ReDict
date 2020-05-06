import sys
import os
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import QFile, QTextStream, Qt, QSettings, QThreadPool, QRunnable, pyqtSlot, QObject, pyqtSignal, QSize, QEvent
from PyQt5.QtWidgets import QAction, qApp, QScroller, QCompleter, QToolBar
from PyQt5.QtGui import QColor, QIcon
from DictionaryDatabase import Database
import pyperclip
import time
from bs4 import BeautifulSoup
from AutoCompleterDwg import AutoComplete
from DictionaryWaitingSpinner import QtWaitingSpinner
from math import ceil

subThread = True
autocomplete = None

class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)

class AllWindows():
    def __init__(self):
        self.db = Database()


    def load_form_pers(self, _class):

        Dialog = type(_class).__name__

        _class.settings = QSettings("Redict", Dialog)
        if not _class.settings.value("geometry") == None:
            _class.restoreGeometry(_class.settings.value("geometry"))
        if not _class.settings.value("windowState") == None:
            _class.restoreState(_class.settings.value("windowState"))

    def save_form_pers(self, _class):
        _class.settings.setValue("geometry", _class.saveGeometry())
        if isinstance(_class, SearchDialog):
            _class.settings.setValue("windowState", _class.saveState())

    def closeEvent(self, event):
        self.save_form_pers(self)

class Search(AllWindows):

    def search_word(self, wrd, like):
        data = self.db.search_word(wrd, like)
        result = ''
        if len(data) != 0:
            for d in data:
                wordid, word, definition, abstractive = d
                if abstractive:
                    result = result + self.get_abstraction(definition) + '<br>'
                result = result + definition.rstrip('<br />').replace('<br>', '') + '<br>---------------------------<br>'
            self.db.write_history(wordid)
        else:
            result = 'Not found'

        return result

    def get_abstraction(self, definition):
        font_size = int(self.db.get_property(2))
        font_size -= 5
        soup = BeautifulSoup(definition, 'html.parser')
        res = soup.findAll('b')
        #abstraction = '<i><b style="color: #548a3d"><p style="font-size:{0}px">'.format(font_size)
        abstraction = '<i><b style="color: #548a3d">'.format(font_size)
        for r in res:
            word = str(r).replace('<b style="color: #47A">', '').replace('</b>', '').rstrip().lstrip().rstrip(',')
            abstraction += word + ', '
        abstraction = abstraction.rstrip(' ').rstrip(',') + '</p></b></i><br>'
        return abstraction

class Completer(QtWidgets.QDialog, AllWindows):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        AllWindows.__init__(self)
        self.load_form_pers(self)
        self.changed = False
        self.init_ui()



    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath('gui/completer.ui'), self)
        QScroller.grabGesture(self.textEdit.viewport(), QScroller.LeftMouseButtonGesture)

        self.prop = self.db.get_property(4)
        if self.prop == self.ui.rbtnLemmata.text():
            self.ui.rbtnLemmata.setChecked(True)
        else:
            self.ui.rbtnDeclinedWords.setChecked(True)

        self.ui.show()

    def closeEvent(self, event):
        if self.ui.rbtnLemmata.isChecked():
             new = self.ui.rbtnLemmata.text()
        else:
            new = self.ui.rbtnDeclinedWords.text()

        if self.prop != new:
            self.db.set_property(4, new)
            self.changed = True

        self.save_form_pers(self)


class Dicts(QtWidgets.QDialog, AllWindows):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        AllWindows.__init__(self)
        self.checkboxCounter = 1
        self.init_ui()
        self.load_form_pers(self)

    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath('gui/dicts.ui'), self)

        ret = self.db.get_dictionaries()
        self.values = self.db.get_property(1)
        self.values = self.values.split(',')

        for r in ret:
            dictionary_id = r[0]
            dictionary_name = r[1]
            self.add_checkbox(dictionary_id, str(dictionary_id) + ': ' + dictionary_name)

    def add_checkbox(self, id, name):
        b = QtWidgets.QCheckBox(name, self, objectName= 'test')
        font = QtGui.QFont()
        font.setPointSize(14)
        b.setFont(font)
        if str(id) in self.values:
            b.setChecked(True)
        b.stateChanged.connect(self.handle_checkboxes)
        self.ui.gridLayout.addWidget(b, self.checkboxCounter, self.checkboxCounter % 1)
        self.checkboxCounter += 1

    def handle_checkboxes(self, state):
        sender = self.sender()
        db_id = sender.text().split(':')[0]

        if state == 2:
            if db_id not in self.values:
                self.values.append(db_id)
        elif state == 0:
            if len(self.values) == 1:
                sender.setChecked(True)
            elif db_id in self.values:
                self.values.remove(db_id)
        self.db.set_property(1, ','.join(self.values))


class SearchDialog(QtWidgets.QMainWindow, AllWindows):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        AllWindows.__init__(self)

        self.init_ui()


    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath("gui/main.ui"), self)
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

        lookup = QAction(QIcon('gui/tbLookup.png'), "look-up", self)
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
            print(f)
            print(g)
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
            lookup_dialog(word)

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

class lookup_dialog(QtWidgets.QDialog, AllWindows):
    def __init__(self, word):
        QtWidgets.QDialog.__init__(self)
        AllWindows.__init__(self)
        self.init_ui()
        self.search = Search()
        self.search_word(word)
        self.load_form_pers(self)

    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath("gui/lookup.ui"), self)
        self.font = QtGui.QFont()
        self.font.setPointSize(int(self.db.get_property(2)))
        self.ui.txtResultLookup.setFont(self.font)
        self.create_contextmenu()
        QScroller.grabGesture(self.txtResultLookup.viewport(), QScroller.LeftMouseButtonGesture)
        self.show()

    def search_word(self, word):
        self.ui.txtResultLookup.clear()
        wrd = word.lower()
        result = self.search.search_word(wrd, False)
        self.set_result(result)

    def set_result(self, result):
        self.ui.txtResultLookup.append(result)
        self.ui.txtResultLookup.moveCursor(QtGui.QTextCursor.Start)

    def create_contextmenu(self):
        self.ui.txtResultLookup.setContextMenuPolicy(Qt.ActionsContextMenu)
        lookup = QAction("look-up", self)
        lookup.triggered.connect(self.look_up)
        self.ui.txtResultLookup.addAction(lookup)

    def look_up(self):
        cursor = self.txtResultLookup.textCursor()
        word = cursor.selectedText()
        if word == '':
            return
        else:
            lookup_dialog(word)

class History(QtWidgets.QDialog, AllWindows):
    def __init__(self, searchFunc):
        QtWidgets.QDialog.__init__(self)
        self.init_ui()
        self.searchFunc = searchFunc
        self.load_form_pers(self)

    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath('gui/History.ui'), self)

        self.ui.listWidget.itemDoubleClicked.connect(self.test)
        self.ui.btnClearHistory.clicked.connect(self.clear)

        self.loadList()
        self.ui.show()

    def test(self):
        word = self.ui.listWidget.currentItem().text()
        self.searchFunc(word)

    def loadList(self):
        history = self.db.get_history()
        self.ui.listWidget.clear()
        for i, word in enumerate(history):
            self.ui.listWidget.insertItem(i, word[0])

    def clear(self):
        self.db.clear_history()
        self.loadList()

class About(QtWidgets.QDialog, AllWindows):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.init_ui()
        self.load_form_pers(self)

    def init_ui(self):
        self.ui = uic.loadUi(os.path.abspath('gui/About.ui'), self)
        QScroller.grabGesture(self.textBrowser.viewport(), QScroller.LeftMouseButtonGesture)
        self.ui.show()

class MySignal(QObject):
    sig_no_args = pyqtSignal()
    sig_with_str = pyqtSignal(str)
    stopLoading = pyqtSignal()
    startLoading = pyqtSignal()


app = QtWidgets.QApplication(sys.argv)

file = QFile("gui/stylesheets/AMOLED.qss")
file.open(QFile.ReadOnly | QFile.Text)
stream = QTextStream(file)
app.setStyleSheet(stream.readAll())

sd = SearchDialog()
sd.show()

sys.exit(app.exec())