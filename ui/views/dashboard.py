from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QMessageBox, QFileDialog, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QIcon
import os
from auth.session_manager import SessionManager


class DashboardPage(QWidget):
    def __init__(self, main_app=None, username=None):
        super().__init__()

        self.main_app = main_app
        self.username = username

        # Check if user is logged in using SessionManager
        if not self.username or not SessionManager.is_logged_in(self.username):
            QMessageBox.critical(self, "Access Denied", "Your session has expired or you're not logged in.")
            if self.main_app:
                self.main_app.show_login()  
            return

        self.setObjectName("dashboard")
        qss_path = os.path.join(os.path.dirname(__file__), "..", "qss", "dashboard.qss")
        with open(qss_path, "r") as f:
            self.setStyleSheet(f.read())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ----- Top Section -----
        top_section = QHBoxLayout()
        top_section.setContentsMargins(0, 0, 0, 0)

        # Enhanced Sidebar
        sidebar = self.create_enhanced_sidebar()

        top_section.addWidget(sidebar)

        # ----- Main Content -----
        content_wrapper = QVBoxLayout()
        content_wrapper.setContentsMargins(20, 20, 20, 10)
        content_wrapper.setSpacing(20)

        # Optional Top Bar (empty)
        top_bar = QHBoxLayout()
        content_wrapper.addLayout(top_bar)

        # Connection Panel (6 Cards)
        connect_card = QFrame()
        connect_card.setObjectName("panel")
        connect_layout = QHBoxLayout(connect_card)
        connect_layout.setSpacing(20)
        connect_layout.setContentsMargins(20, 10, 20, 10)
        connect_layout.setAlignment(Qt.AlignCenter)

        services = [
            ("Zoom", "ui/assests/zoom.webp"),
            ("Gmail", "ui/assests/gmail.webp"),
            ("GMeet", "ui/assests/gmeet.webp"),
            ("Spotify", "ui/assests/spotify.webp"),
            ("YouTube", "ui/assests/youtube.webp"),
            ("Discord", "ui/assests/discord.webp"),
        ]

        for service, icon_path in services:
            icon_label = QLabel()
            if os.path.exists(icon_path):
                icon_pixmap = QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(icon_pixmap)
            else:
                icon_label.setText("📱")
                icon_label.setStyleSheet("font-size: 24px;")
            icon_label.setAlignment(Qt.AlignCenter)

            connect_btn = QPushButton("Connect")
            connect_btn.setCursor(Qt.PointingHandCursor)

            disconnect_btn = QPushButton("Disconnect")
            disconnect_btn.setCursor(Qt.PointingHandCursor)

            btn_layout = QVBoxLayout()
            btn_layout.setAlignment(Qt.AlignCenter)
            btn_layout.addWidget(icon_label)
            btn_layout.addWidget(QLabel(service, alignment=Qt.AlignCenter))
            btn_layout.addWidget(connect_btn)
            btn_layout.addWidget(disconnect_btn)

            sub_card = QFrame()
            sub_card.setObjectName("panel")
            sub_card.setLayout(btn_layout)
            connect_layout.addWidget(sub_card)

        content_wrapper.addWidget(connect_card)
        top_section.addLayout(content_wrapper)
        main_layout.addLayout(top_section)

        # ----- Status Bar -----
        status = QLabel("Status: Ready")
        status.setAlignment(Qt.AlignCenter)
        status.setObjectName("statusBar")
        main_layout.addWidget(status)

    def create_enhanced_sidebar(self):
        """Create an enhanced sidebar with icons and better styling"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(260)  # Slightly wider for better spacing

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setContentsMargins(25, 35, 25, 30)
        sidebar_layout.setSpacing(15)

        # App Title with improved styling
        app_title = QLabel("🤖 Sentinel AI")
        app_title.setObjectName("appTitle")
        app_title.setAlignment(Qt.AlignCenter)

        # Add subtitle
        subtitle = QLabel("AI Security Dashboard")
        subtitle.setObjectName("appSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        sidebar_layout.addWidget(app_title)
        sidebar_layout.addWidget(subtitle)

        # Add spacing after title
        sidebar_layout.addSpacing(25)

        # Navigation section
        nav_label = QLabel("NAVIGATION")
        nav_label.setObjectName("sectionLabel")
        sidebar_layout.addWidget(nav_label)

        # Enhanced sidebar buttons with icons
        nav_items = [
            ("🏠", "Home", "homeBtn"),
            ("📋", "Tasks", "tasksBtn"),
            ("🤖", "Agents", "agentsBtn"),
            ("⚙️", "Settings", "settingsBtn")
        ]

        self.nav_buttons = {}
        for icon, text, obj_name in nav_items:
            btn = self.create_sidebar_button(icon, text, obj_name)
            self.nav_buttons[text.lower()] = btn
            sidebar_layout.addWidget(btn)

        # Set Home as initially active
        if "home" in self.nav_buttons:
            self.nav_buttons["home"].setProperty("active", True)

        # Flexible spacer to push bottom items down
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        sidebar_layout.addItem(spacer)

        # User section
        user_label = QLabel("USER")
        user_label.setObjectName("sectionLabel")
        sidebar_layout.addWidget(user_label)

        # User info display
        user_info = QLabel(f"👤 {self.username.title()}")
        user_info.setObjectName("userInfo")
        sidebar_layout.addWidget(user_info)

        # Bottom buttons
        profile_btn = self.create_sidebar_button("👤", "My Profile", "profileBtn")
        logout_btn = self.create_sidebar_button("🚪", "Logout", "logoutBtn", is_logout=True)

        sidebar_layout.addWidget(profile_btn)
        sidebar_layout.addWidget(logout_btn)

        return sidebar

    def create_sidebar_button(self, icon, text, object_name, is_logout=False):
        """Create a styled sidebar button with icon and text"""
        btn = QPushButton(f"{icon}  {text}")
        btn.setObjectName(object_name)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(45)

        # Connect logout functionality
        if is_logout:
            btn.clicked.connect(self.logout_user)
        else:
            # Connect other button functions (can be expanded later)
            btn.clicked.connect(lambda: self.handle_sidebar_click(text.lower()))

        return btn

    def handle_sidebar_click(self, button_name):
        """Handle sidebar button clicks"""
        # Reset all button states first
        for btn in self.nav_buttons.values():
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # Set clicked button as active
        if button_name in self.nav_buttons:
            self.nav_buttons[button_name].setProperty("active", True)
            self.nav_buttons[button_name].style().unpolish(self.nav_buttons[button_name])
            self.nav_buttons[button_name].style().polish(self.nav_buttons[button_name])

        # Handle different navigation actions
        if button_name == "home":
            print("🏠 Home clicked")
        elif button_name == "tasks":
            print("📋 Tasks clicked")
        elif button_name == "agents":
            print("🤖 Agents clicked")
        elif button_name == "settings":
            print("⚙️ Settings clicked")

    def logout_user(self):
        if self.username:
            SessionManager.delete_session(self.username)  
        if self.main_app:
            self.main_app.show_login()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            print("Training agent on file:", file_name)


    
