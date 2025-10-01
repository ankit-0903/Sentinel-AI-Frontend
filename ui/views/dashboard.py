from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QMessageBox, QFileDialog, QSpacerItem, QSizePolicy,
    QGridLayout
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

        # Initialize responsive variables
        self.is_compact_mode = False
        self.setup_layout()

    def setup_layout(self):
        """Setup the main layout"""
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
        content_wrapper.setContentsMargins(25, 25, 25, 15)
        content_wrapper.setSpacing(25)

        # Dashboard Header
        header_section = self.create_dashboard_header()
        content_wrapper.addWidget(header_section)

        # Statistics Cards Row
        stats_section = self.create_statistics_section()
        content_wrapper.addWidget(stats_section)

        # Quick Actions Section
        quick_actions = self.create_quick_actions_section()
        content_wrapper.addWidget(quick_actions)

        # Enhanced Connection Panel
        connection_section = self.create_responsive_connection_section()
        content_wrapper.addWidget(connection_section)

        # Recent Activity Section
        activity_section = self.create_recent_activity_section()
        content_wrapper.addWidget(activity_section)

        top_section.addLayout(content_wrapper)
        main_layout.addLayout(top_section)

        # ----- Status Bar -----
        status = QLabel("Status: Ready")
        status.setAlignment(Qt.AlignCenter)
        status.setObjectName("statusBar")
        main_layout.addWidget(status)

    def resizeEvent(self, event):
        """Handle window resize events for responsive design"""
        super().resizeEvent(event)
        current_width = self.width()
        should_be_compact = current_width < 1200

        if should_be_compact != self.is_compact_mode:
            self.is_compact_mode = should_be_compact
            # Just adjust some basic responsive elements without full rebuild
            self.adjust_responsive_elements()

    def adjust_responsive_elements(self):
        """Adjust elements for responsive behavior without rebuilding"""
        # Find and adjust sidebar width if it exists
        sidebar = self.findChild(QFrame, "sidebar")
        if sidebar:
            sidebar_width = 200 if self.is_compact_mode else 250
            sidebar.setFixedWidth(sidebar_width)

    def create_enhanced_sidebar(self):
        """Create an enhanced sidebar with icons and better styling"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)

        main_layout = QVBoxLayout(sidebar)
        main_layout.setContentsMargins(15, 20, 15, 20)
        main_layout.setSpacing(15)

        # Header Section
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        # Try to load logo, fallback to shield emoji if not found
        logo_path = "icons/sentinel_logo.png"
        if os.path.exists(logo_path):
            logo_label.setPixmap(QPixmap(logo_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo_label.setText("🛡️")
            logo_label.setStyleSheet("font-size: 24px;")
        logo_label.setObjectName("logo_label")

        title_label = QLabel("Sentinel AI")
        title_label.setObjectName("title_label")

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)

        # Dashboard Title
        dashboard_title = QLabel("AI SECURITY DASHBOARD")
        dashboard_title.setObjectName("dashboard_title")
        dashboard_title.setAlignment(Qt.AlignLeft)
        dashboard_title.setContentsMargins(0, 10, 0, 5)

        # Navigation Section
        navigation_frame = QFrame()
        navigation_frame.setObjectName("navigation_frame")
        navigation_layout = QVBoxLayout(navigation_frame)
        navigation_layout.setContentsMargins(0, 0, 0, 0)
        navigation_layout.setSpacing(10)

        # Navigation Buttons
        self.home_button = QPushButton("Home")
        self.home_button.setObjectName("home_button")
        icon_path = "icons/home_icon.png"
        if os.path.exists(icon_path):
            self.home_button.setIcon(QIcon(icon_path))
        self.home_button.setCheckable(True)
        self.home_button.setChecked(True)
        self.home_button.clicked.connect(lambda: self.handle_sidebar_click("home"))

        self.tasks_button = QPushButton("Tasks")
        self.tasks_button.setObjectName("tasks_button")
        icon_path = "icons/tasks_icon.png"
        if os.path.exists(icon_path):
            self.tasks_button.setIcon(QIcon(icon_path))
        self.tasks_button.clicked.connect(lambda: self.handle_sidebar_click("tasks"))

        self.agents_button = QPushButton("Agents")
        self.agents_button.setObjectName("agents_button")
        icon_path = "icons/agents_icon.png"
        if os.path.exists(icon_path):
            self.agents_button.setIcon(QIcon(icon_path))
        self.agents_button.clicked.connect(lambda: self.handle_sidebar_click("agents"))

        self.settings_button = QPushButton("Settings")
        self.settings_button.setObjectName("settings_button")
        icon_path = "icons/settings_icon.png"
        if os.path.exists(icon_path):
            self.settings_button.setIcon(QIcon(icon_path))
        self.settings_button.clicked.connect(lambda: self.handle_sidebar_click("settings"))

        navigation_layout.addWidget(self.home_button)
        navigation_layout.addWidget(self.tasks_button)
        navigation_layout.addWidget(self.agents_button)
        navigation_layout.addWidget(self.settings_button)

        # User Section
        user_frame = QFrame()
        user_frame.setObjectName("user_frame")
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(10)

        user_name_button = QPushButton(self.username.title() if self.username else "User")
        user_name_button.setObjectName("user_name_button")
        icon_path = "icons/user_icon.png"
        if os.path.exists(icon_path):
            user_name_button.setIcon(QIcon(icon_path))
        user_name_button.setDisabled(True)

        my_profile_button = QPushButton("My Profile")
        my_profile_button.setObjectName("my_profile_button")
        if os.path.exists(icon_path):
            my_profile_button.setIcon(QIcon(icon_path))

        user_layout.addWidget(user_name_button)
        user_layout.addWidget(my_profile_button)

        # Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setObjectName("logout_button")
        icon_path = "icons/logout_icon.png"
        if os.path.exists(icon_path):
            logout_button.setIcon(QIcon(icon_path))
        logout_button.clicked.connect(self.logout_user)

        # Add all sections to the main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(dashboard_title)
        main_layout.addWidget(navigation_frame)
        main_layout.addStretch(1)
        main_layout.addWidget(user_frame)
        main_layout.addWidget(logout_button)

        return sidebar

    def create_dashboard_header(self):
        """Create the dashboard header with welcome message and system status"""
        header_frame = QFrame()
        header_frame.setObjectName("dashboard_header")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)

        # Welcome section
        welcome_layout = QVBoxLayout()
        welcome_title = QLabel(f"Welcome back, {self.username.title()}!")
        welcome_title.setObjectName("welcome_title")
        welcome_subtitle = QLabel("Monitor and manage your AI security systems")
        welcome_subtitle.setObjectName("welcome_subtitle")

        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_subtitle)
        welcome_layout.addStretch()

        # System status indicator
        status_layout = QVBoxLayout()
        status_layout.setAlignment(Qt.AlignRight | Qt.AlignCenter)

        system_status = QLabel("🟢 All Systems Operational")
        system_status.setObjectName("system_status")
        system_status.setAlignment(Qt.AlignRight)

        status_layout.addWidget(system_status)

        header_layout.addLayout(welcome_layout)
        header_layout.addStretch()
        header_layout.addLayout(status_layout)

        return header_frame

    def create_statistics_section(self):
        """Create statistics cards showing key metrics"""
        stats_frame = QFrame()
        stats_frame.setObjectName("stats_section")

        # Use grid layout for responsive design
        if self.is_compact_mode:
            # 2x2 grid for compact mode
            stats_layout = QGridLayout(stats_frame)
            stats_layout.setSpacing(15)
            cols = 2
        else:
            # Horizontal layout for normal mode
            stats_layout = QHBoxLayout(stats_frame)
            stats_layout.setSpacing(20)
            cols = 4

        stats_layout.setContentsMargins(0, 0, 0, 0) 

    def create_quick_actions_section(self):
        """Create quick action buttons for common tasks"""
        actions_frame = QFrame()
        actions_frame.setObjectName("quick_actions")
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(20, 15, 20, 15)
        actions_layout.setSpacing(15)

        # Section title
        title = QLabel("Quick Actions")
        title.setObjectName("section_title")
        actions_layout.addWidget(title)

        # Action buttons row
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        action_buttons = [
            ("🚀", "Run Full Scan", "scan_btn"),
            ("📁", "Upload File", "upload_btn"),
            ("📊", "Generate Report", "report_btn"),
            ("⚙️", "System Settings", "settings_btn")
        ]

        for icon, text, btn_id in action_buttons:
            btn = QPushButton(f"{icon}  {text}")
            btn.setObjectName(btn_id)
            btn.setCursor(Qt.PointingHandCursor)
            if btn_id == "upload_btn":
                btn.clicked.connect(self.open_file)
            buttons_layout.addWidget(btn)

        actions_layout.addLayout(buttons_layout)
        return actions_frame


    def create_responsive_connection_section(self):
        """Create responsive connection panel with better styling"""
        connection_frame = QFrame()
        connection_frame.setObjectName("connection_section")
        connection_layout = QVBoxLayout(connection_frame)
        padding = 15 if self.is_compact_mode else 20
        connection_layout.setContentsMargins(padding, 12, padding, 12)
        connection_layout.setSpacing(15 if self.is_compact_mode else 20)

        # Section title
        title = QLabel("Application Monitoring")
        title.setObjectName("section_title")
        connection_layout.addWidget(title)

        # Services in responsive grid
        services_frame = QWidget()
        if self.is_compact_mode:
            # 2 columns for compact mode
            services_layout = QGridLayout(services_frame)
            services_layout.setSpacing(15)
            cols = 2
        else:
            # 3 columns for normal mode
            services_layout = QGridLayout(services_frame)
            services_layout.setSpacing(20)
            cols = 3

        services = [
            ("Zoom", "ui/assests/zoom.webp", "🎥"),
            ("Gmail", "ui/assests/gmail.webp", "📧"),
            ("GMeet", "ui/assests/gmeet.webp", "👥"),
            ("Spotify", "ui/assests/spotify.webp", "🎵"),
            ("YouTube", "ui/assests/youtube.webp", "📺"),
            ("Discord", "ui/assests/discord.webp", "💬"),
        ]

        for i, (service, icon_path, fallback_icon) in enumerate(services):
            service_card = QFrame()
            service_card.setObjectName("service_card")
            card_layout = QVBoxLayout(service_card)
            card_padding = 12 if self.is_compact_mode else 15
            card_layout.setContentsMargins(card_padding, 15, card_padding, 15)
            card_layout.setSpacing(10 if self.is_compact_mode else 12)
            card_layout.setAlignment(Qt.AlignCenter)

            # Service icon
            icon_label = QLabel()
            icon_size = 40 if self.is_compact_mode else 48
            if os.path.exists(icon_path):
                icon_pixmap = QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(icon_pixmap)
            else:
                icon_label.setText(fallback_icon)
                icon_label.setStyleSheet(f"font-size: {icon_size-8}px;")
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setObjectName("service_icon")

            # Service name
            name_label = QLabel(service)
            name_label.setObjectName("service_name")
            name_label.setAlignment(Qt.AlignCenter)

            # Status indicator
            status_label = QLabel("🟢 Connected")
            status_label.setObjectName("service_status")
            status_label.setAlignment(Qt.AlignCenter)

            # Action buttons
            button_layout = QHBoxLayout()
            button_spacing = 6 if self.is_compact_mode else 8
            button_layout.setSpacing(button_spacing)

            connect_btn = QPushButton("Monitor")
            connect_btn.setObjectName("connect_btn")
            connect_btn.setCursor(Qt.PointingHandCursor)

            disconnect_btn = QPushButton("Stop")
            disconnect_btn.setObjectName("disconnect_btn")
            disconnect_btn.setCursor(Qt.PointingHandCursor)

            button_layout.addWidget(connect_btn)
            button_layout.addWidget(disconnect_btn)

            card_layout.addWidget(icon_label)
            card_layout.addWidget(name_label)
            card_layout.addWidget(status_label)
            card_layout.addLayout(button_layout)

            # Add to grid
            row = i // cols
            col = i % cols
            services_layout.addWidget(service_card, row, col)

        connection_layout.addWidget(services_frame)
        return connection_frame

    def create_recent_activity_section(self):
        """Create recent activity log section"""
        activity_frame = QFrame()
        activity_frame.setObjectName("activity_section")
        activity_layout = QVBoxLayout(activity_frame)
        activity_layout.setContentsMargins(20, 15, 20, 15)
        activity_layout.setSpacing(15)

        # Section title
        title = QLabel("Recent Activity")
        title.setObjectName("section_title")
        activity_layout.addWidget(title)

        # Activity placeholder
        activity_text = QLabel("No recent activity to display.")
        activity_text.setStyleSheet("color: #888888; font-style: italic; padding: 20px;")
        activity_text.setAlignment(Qt.AlignCenter)
        activity_layout.addWidget(activity_text)

        return activity_frame

    def handle_sidebar_click(self, button_name):
        """Handle sidebar button clicks"""
        # Reset all button states first
        self.home_button.setChecked(False)
        self.tasks_button.setChecked(False)
        self.agents_button.setChecked(False)
        self.settings_button.setChecked(False)

        # Set clicked button as active
        if button_name == "home":
            self.home_button.setChecked(True)
            print("🏠 Home clicked")
        elif button_name == "tasks":
            self.tasks_button.setChecked(True)
            print("📋 Tasks clicked")
        elif button_name == "agents":
            self.agents_button.setChecked(True)
            print("🤖 Agents clicked")
        elif button_name == "settings":
            self.settings_button.setChecked(True)
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


    
