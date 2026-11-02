import datetime
import json

from PySide6.QtCore import QStringListModel, Qt
from PySide6.QtWidgets import QAbstractItemView, QMainWindow, QCompleter

import storage
from ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = QStringListModel()
        self.ui.listView.setModel(self.model)
        self.ui.listView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.completer_model = QStringListModel()
        self.completer = QCompleter(self.completer_model, self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.ui.lineEdit.setCompleter(self.completer)

        self.ui.pushButton.clicked.connect(self.on_ok)
        self.ui.lineEdit.returnPressed.connect(self.on_ok)

        self.data = storage.storage()

        self.refresh_list()

    def on_ok(self):
        text = self.ui.lineEdit.text()
        if not text:
            return

        self.data[text] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.save_data()

        self.refresh_list()
        self.ui.lineEdit.clear()

    def save_data(self):
        with open("activities.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def refresh_list(self):
        items = []
        for key, value in sorted(
                self.data.items(),
                key=lambda x: datetime.datetime.strptime(x[1], "%d.%m.%Y %H:%M:%S"),
                reverse=True):
            items.append(f"{key}: {value}")
        self.model.setStringList(items)

        self.completer_model.setStringList(list(self.data.keys()))
