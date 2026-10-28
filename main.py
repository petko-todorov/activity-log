import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from ui.main_window import Ui_MainWindow


def main():
    app = QApplication(sys.argv)

    window = QMainWindow()  # the real window
    ui = Ui_MainWindow()  # the generated "blueprint"
    ui.setupUi(window)  # put the buttons etc. onto the window

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
