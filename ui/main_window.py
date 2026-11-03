import json
from datetime import datetime

from PySide6.QtCore import QStringListModel, Qt
from PySide6.QtWidgets import QAbstractItemView, QMainWindow, QCompleter

import storage
from ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    DATE_FORMAT = "%H:%M:%S %d.%m.%Y"

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

        self.ui.listView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.listView.customContextMenuRequested.connect(self.show_context_menu)

        self.refresh_list()

    def on_ok(self):
        text = self.ui.lineEdit.text()
        if not text:
            return

        self.data[text] = datetime.now().strftime(self.DATE_FORMAT)
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
                key=lambda x: datetime.strptime(x[1], self.DATE_FORMAT),
                reverse=True):
            days = self.calculate_days_passed(value)
            if days == 0:
                items.append(f"{key} - today")
            else:
                items.append(f"{key} - {self.calculate_days_passed(value)} day{'' if days == 1 else 's'} ago")
        self.model.setStringList(items)

        self.completer_model.setStringList(list(self.data.keys()))

    def show_context_menu(self, pos):
        index = self.ui.listView.indexAt(pos)
        if not index.isValid():
            return

        self.ui.listView.setCurrentIndex(index)

    @staticmethod
    def calculate_days_passed(date_str):
        last_date = datetime.strptime(date_str, "%H:%M:%S %d.%m.%Y").date()
        today = datetime.now().date()
        diff = today - last_date
        return diff.days
