from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QMessageBox,
)
from PySide6.QtCore import Qt

from config import Config
from host import HostDetector


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Load configuration
        self.cfg = Config()

        # Host detector
        self.detector = HostDetector(self.cfg.players)

        # Detect current host
        current_host = self.detector.get_online_host()

        if current_host:
            status_text = "Online"
            host_text = current_host
        else:
            status_text = "Offline"
            host_text = "Nobody"

        # Window
        self.setWindowTitle("PalSync")
        self.setMinimumSize(520, 420)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        # Title
        title = QLabel("PALSYNC")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        layout.addWidget(title)

        # Grid
        grid = QGridLayout()

        # World
        grid.addWidget(QLabel("World:"), 0, 0)
        self.world = QLabel(self.cfg.world_name)
        grid.addWidget(self.world, 0, 1)

        # Status
        grid.addWidget(QLabel("Status:"), 1, 0)
        self.status = QLabel(status_text)
        grid.addWidget(self.status, 1, 1)

        # Host
        grid.addWidget(QLabel("Host:"), 2, 0)
        self.host = QLabel(host_text)
        grid.addWidget(self.host, 2, 1)

        # Sync
        grid.addWidget(QLabel("Sync:"), 3, 0)
        self.sync = QLabel("Unchecked")
        grid.addWidget(self.sync, 3, 1)

        layout.addLayout(grid)

        # PLAY
        self.play = QPushButton("PLAY")
        self.play.setMinimumHeight(55)
        self.play.clicked.connect(self.play_clicked)
        layout.addWidget(self.play)

        # START SERVER
        self.server = QPushButton("Start Server")
        self.server.clicked.connect(self.server_clicked)
        layout.addWidget(self.server)

        # SETTINGS
        self.settings = QPushButton("Settings")
        self.settings.clicked.connect(self.settings_clicked)
        layout.addWidget(self.settings)

        layout.addStretch()

    def play_clicked(self):
        QMessageBox.information(
            self,
            "PalSync",
            "Soon this button will:\n"
            "• Detect the active host\n"
            "• Start the server if needed\n"
            "• Launch Palworld\n"
            "• Connect automatically"
        )

    def server_clicked(self):
        QMessageBox.information(
            self,
            "PalSync",
            "Dedicated server support is coming next."
        )

    def settings_clicked(self):
        QMessageBox.information(
            self,
            "PalSync",
            "Settings window coming soon."
        )