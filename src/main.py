import sys

from PySide6.QtWidgets import QApplication

from api import start_api
from status_manager import StatusManager
from ui import MainWindow


def main():

    # Start embedded HTTP API
    start_api()

    # Start background status updater
    status_manager = StatusManager()
    status_manager.start()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()