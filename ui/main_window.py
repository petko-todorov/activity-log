import datetime
from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QAbstractItemView, QMainWindow

import storage
from ui.ui_main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = QStringListModel()
        self.ui.listView.setModel(self.model)
        self.ui.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.ui.pushButton.clicked.connect(self.on_ok)
        self.ui.lineEdit.returnPressed.connect(self.on_ok)

        self.data = storage.storage()

        self.refresh_list()

    def on_ok(self):
        text = self.ui.lineEdit.text()
        self.data[text] = datetime.datetime.now()
        self.ui.lineEdit.setText("")
        self.refresh_list()
        self.ui.listView.scrollToBottom()
        self.ui.listView.setCurrentIndex(self.model.index(self.model.rowCount() - 1))
        self.ui.listView.scrollToBottom()


    def refresh_list(self):
        self.model.setStringList(list(self.data.items()))
        self.model.layoutChanged.emit()

        self.ui.listView.setCurrentIndex(self.model.index(self.model.rowCount() - 1))
