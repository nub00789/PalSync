from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QMessageBox,
    QProgressBar,
)

from PySide6.QtCore import (
    Qt,
    QTimer,
    QThread,
)

from config import Config
from host import HostDetector
from server import ServerManager
from launcher import Launcher
from worker import ServerWorker, StatusWorker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.cfg = Config()

        self.server_manager = ServerManager(
            self.cfg.server_path,
            self.cfg.port
        )

        self.detector = HostDetector(
            self.cfg.players,
            self.cfg.port
        )

        self.launcher = Launcher(self.cfg)

        self.thread = None
        self.worker = None

        self.status_thread = None
        self.status_worker = None

        self.setWindowTitle("PalSync")
        self.resize(600, 450)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("PALSYNC")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size:30px;font-weight:bold;"
        )
        layout.addWidget(title)

        grid = QGridLayout()

        grid.addWidget(QLabel("World:"), 0, 0)
        self.world = QLabel(self.cfg.world_name)
        grid.addWidget(self.world, 0, 1)

        grid.addWidget(QLabel("Status:"), 1, 0)
        self.status = QLabel("Checking...")
        grid.addWidget(self.status, 1, 1)

        grid.addWidget(QLabel("Host:"), 2, 0)
        self.host = QLabel("-")
        grid.addWidget(self.host, 2, 1)

        grid.addWidget(QLabel("Ping:"), 3, 0)
        self.ping = QLabel("-")
        grid.addWidget(self.ping, 3, 1)

        grid.addWidget(QLabel("Sync:"), 4, 0)
        self.sync = QLabel("100%")
        grid.addWidget(self.sync, 4, 1)

        layout.addLayout(grid)

        self.sync_bar = QProgressBar()
        self.sync_bar.setRange(0, 100)
        self.sync_bar.setValue(100)
        layout.addWidget(self.sync_bar)

        self.play_button = QPushButton("PLAY")
        self.play_button.clicked.connect(self.play_clicked)
        layout.addWidget(self.play_button)

        self.server_button = QPushButton("Start Server")
        self.server_button.clicked.connect(self.server_clicked)
        layout.addWidget(self.server_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.settings_clicked)
        layout.addWidget(self.settings_button)

        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_status_worker)
        self.timer.start(1000)

        self.start_status_worker()

    # ----------------------------------------------------
    # STATUS
    # ----------------------------------------------------

    def start_status_worker(self):

        if self.status_thread is not None:

            try:
                if self.status_thread.isRunning():
                    return
            except RuntimeError:
                self.status_thread = None

        self.status_thread = QThread()

        self.status_worker = StatusWorker(
            self.detector,
            self.server_manager
        )

        self.status_worker.moveToThread(
            self.status_thread
        )

        self.status_thread.started.connect(
            self.status_worker.run
        )

        self.status_worker.finished.connect(
            self.update_status
        )

        self.status_worker.finished.connect(
            self.status_thread.quit
        )

        self.status_thread.finished.connect(
            self.cleanup_status_thread
        )

        self.status_thread.start()

    def cleanup_status_thread(self):

        try:
            self.status_thread.deleteLater()
        except RuntimeError:
            pass

        self.status_thread = None
        self.status_worker = None

    def update_status(self, result):

        if result["running"]:
            self.status.setText("🟢 Online")
        else:
            self.status.setText("🔴 Offline")

        if result["host"]:

            self.host.setText(result["host"]["name"])
            self.ping.setText(
                f'{result["host"]["ping"]} ms'
            )

        else:

            self.host.setText("-")
            self.ping.setText("-")

    # ----------------------------------------------------
    # PLAY
    # ----------------------------------------------------

    def play_clicked(self):

        if self.thread is not None:

            try:
                if self.thread.isRunning():
                    return
            except RuntimeError:
                self.thread = None

        self.play_button.setEnabled(False)

        self.thread = QThread()

        self.worker = ServerWorker(
            self.launcher
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.status.connect(
            self.status.setText
        )

        self.worker.finished.connect(
            self.play_finished
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.thread.finished.connect(
            self.cleanup_play_thread
        )

        self.thread.start()

    def cleanup_play_thread(self):

        try:
            self.thread.deleteLater()
        except RuntimeError:
            pass

        self.thread = None
        self.worker = None

    def play_finished(self, success):

        self.play_button.setEnabled(True)

        self.start_status_worker()

        if not success:

            QMessageBox.warning(
                self,
                "PalSync",
                "Launcher failed."
            )

    # ----------------------------------------------------
    # SERVER
    # ----------------------------------------------------

    def server_clicked(self):

        try:

            if self.server_manager.running():

                self.server_manager.stop()
                self.server_button.setText("Start Server")

            else:

                self.server_manager.start()
                self.server_button.setText("Stop Server")

            self.start_status_worker()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Server",
                str(e)
            )

    # ----------------------------------------------------
    # SETTINGS
    # ----------------------------------------------------

    def settings_clicked(self):

        QMessageBox.information(
            self,
            "Settings",
            "Coming Soon"
        )