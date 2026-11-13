from datetime import datetime, timedelta

from PySide6.QtCore import QStringListModel, Qt, QTimer
from PySide6.QtWidgets import QAbstractItemView, QMainWindow, QCompleter, QMenu, QMessageBox, QInputDialog

import storage
from ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    DATE_FORMAT = "%H:%M:%S %d.%m.%Y"
    COMBOBOX_OPTIONS = [
        {"text": "Now", "days_back": 0},
        {"text": "Yesterday", "days_back": 1},
        {"text": "2 days ago", "days_back": 2},
        {"text": "3 days ago", "days_back": 3},
    ]

    def __init__(self):
        super().__init__()
        self.keys = None
        self.data = storage.storage()

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

        self.ui.listView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.listView.customContextMenuRequested.connect(self.show_context_menu)

        self.refresh_list()

        for combo in self.COMBOBOX_OPTIONS:
            self.ui.comboBox.addItem(combo["text"], combo["days_back"])

    def on_ok(self):
        text = self.ui.lineEdit.text()
        if not text:
            return

        days_back = self.ui.comboBox.currentData()
        if days_back == 0:
            self.data[text.strip()] = datetime.now().strftime(self.DATE_FORMAT)
        else:
            timestamp = datetime.replace(datetime.now(), hour=0, minute=0, second=0, microsecond=0) - timedelta(
                days=days_back)
            self.data[text.strip()] = timestamp.strftime(self.DATE_FORMAT)

        self.save_data()

        self.refresh_list()
        QTimer.singleShot(0, self.ui.lineEdit.clear)

    def save_data(self):
        storage.save(self.data)

    def refresh_list(self):
        sorted_items = sorted(
            self.data.items(),
            key=lambda x: datetime.strptime(x[1], self.DATE_FORMAT),
            reverse=True,
        )
        self.keys = [key for key, _ in sorted_items]

        items = []
        for key, value in sorted_items:
            days = self.calculate_days_passed(value)
            if days == 0:
                items.append(f"{key} - today")
            elif days == 1:
                items.append(f"{key} - yesterday")
            else:
                items.append(f"{key} - {days} days ago")
        self.model.setStringList(items)

        self.completer_model.setStringList(self.keys)

    def show_context_menu(self, pos):
        index = self.ui.listView.indexAt(pos)
        if not index.isValid():
            return

        self.ui.listView.setCurrentIndex(index)

        menu = QMenu(self)
        menu.setFont(self.ui.listView.font())
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")

        chosen = menu.exec(self.ui.listView.viewport().mapToGlobal(pos))
        if chosen == edit_action:
            self.edit_key(index.row())

        elif chosen == delete_action:
            del self.data[self.keys[index.row()]]
            self.save_data()
            self.refresh_list()

    def calculate_days_passed(self, date_str):
        last_date = datetime.strptime(date_str, self.DATE_FORMAT).date()
        today = datetime.now().date()
        diff = today - last_date
        return diff.days

    def edit_key(self, row):
        old_key = self.keys[row]

        new_key, ok = QInputDialog.getText(
            self,
            "Edit activity",
            "Name:",
            text=old_key
        )

        if not ok:
            return None

        new_key = new_key.strip()
        if not new_key or new_key == old_key:
            return None

        if new_key in self.data:
            QMessageBox.warning(
                self, "Duplicate", f'"{new_key}" already exists.'
            )
            return self.edit_key(row)

        self.data[new_key] = self.data.pop(old_key)
        self.save_data()
        return self.refresh_list()
