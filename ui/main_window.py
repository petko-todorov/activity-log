from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QAbstractItemView, QMainWindow

import storage
import utils
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

    def on_ok(self):
        pass

    def refresh_list(self):
        pass
