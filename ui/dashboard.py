from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QLineEdit, QSizePolicy, QComboBox, QTableWidget,
    QTableWidgetItem, QProgressBar, QFileDialog, QMenu
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import os


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("dashboard")
        qss_path = os.path.join(os.path.dirname(__file__), "dashboard.qss")
        with open(qss_path, "r") as f:
            self.setStyleSheet(f.read())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ----- Top Section -----
        top_section = QHBoxLayout()
        top_section.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(20)

        app_title = QLabel("Sentinel AI")
        app_title.setObjectName("appTitle")
        sidebar_layout.addWidget(app_title)

        for item in ["Home", "Tasks", "Agents", "Settings"]:
            btn = QPushButton(f"  {item}")
            btn.setObjectName("sidebarBtn")
            btn.setCursor(Qt.PointingHandCursor)
            sidebar_layout.addWidget(btn)

        top_section.addWidget(sidebar)

        # Content Wrapper
        content_wrapper = QVBoxLayout()
        content_wrapper.setContentsMargins(20, 20, 20, 10)
        content_wrapper.setSpacing(20)

        # Top Bar
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        profile_button = QPushButton()
        profile_button.setIcon(QIcon("assets/user.png"))
        profile_button.setIconSize(QSize(40, 40))
        profile_button.setCursor(Qt.PointingHandCursor)
        profile_button.setObjectName("profileDropdown")
        self.profile_menu = QMenu()
        self.profile_menu.addAction("My Profile")
        self.profile_menu.addAction("Logout")
        profile_button.setMenu(self.profile_menu)
        top_bar.addWidget(profile_button)

        content_wrapper.addLayout(top_bar)

        # Connection Buttons Card
        connect_card = QFrame()
        connect_card.setObjectName("panel")
        connect_layout = QHBoxLayout(connect_card)
        connect_layout.setSpacing(20)
        connect_layout.setContentsMargins(20, 10, 20, 10)
        connect_layout.setAlignment(Qt.AlignCenter)

        for service, icon_path in [
            ("Zoom", "ui//zoom.png"),
            ("GMeet", "ui//gmeet.png"),
            ("Gmail", "ui//gmail.png")
        ]:
            card = QVBoxLayout()
            icon_label = QLabel()
            icon_pixmap = QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
            icon_label.setAlignment(Qt.AlignCenter)

            connect_btn = QPushButton(f"Connect with {service}")
            connect_btn.setCursor(Qt.PointingHandCursor)

            wrapper = QVBoxLayout()
            wrapper.setAlignment(Qt.AlignCenter)
            wrapper.addWidget(icon_label)
            wrapper.addWidget(connect_btn)

            sub_card = QFrame()
            sub_card.setObjectName("panel")
            sub_card.setLayout(wrapper)
            connect_layout.addWidget(sub_card)

        content_wrapper.addWidget(connect_card)

        top_section.addLayout(content_wrapper)
        main_layout.addLayout(top_section)

        # Status Bar
        status = QLabel("Status: Ready")
        status.setAlignment(Qt.AlignCenter)
        status.setObjectName("statusBar")
        main_layout.addWidget(status)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            print("Training agent on file:", file_name)





