from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from db.mongo_client import users_collection


class LoginPage(QWidget):
    def __init__(self, switch_to_signup=None):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(80, 40, 80, 40)
        layout.setSpacing(20)

        # Left side - image section
        image_box = QFrame(self)
        image_box.setFrameShape(QFrame.StyledPanel)
        image_box.setLineWidth(2)
        image_box.setStyleSheet("border-radius: 10px; border: 1px solid #7d5fff;")

        image_label = QLabel(image_box)
        pixmap = QPixmap("ui//image.png") 
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setScaledContents(True)
        image_box.setLayout(QVBoxLayout())
        image_box.layout().addWidget(image_label)

        layout.addWidget(image_box, 1)

        # Right side - login form section
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(20)

        self.titleLabel = QLabel("Welcome back...")
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")

        # Remember Me and Forgot Password layout
        remember_forgot_row = QHBoxLayout()
        self.remember_checkbox = QCheckBox("Remember Me")
        self.remember_checkbox.setStyleSheet("color: white;")
        
        self.forgot_label = QLabel("<a href='#' style='color: white; text-decoration: none;'>Forgot Password</a>")
        self.forgot_label.setObjectName("forgotPassword")
        self.forgot_label.setTextFormat(Qt.RichText)
        self.forgot_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.forgot_label.setOpenExternalLinks(True)

        remember_forgot_row.addWidget(self.remember_checkbox, alignment=Qt.AlignLeft)
        remember_forgot_row.addWidget(self.forgot_label, alignment=Qt.AlignRight)

        self.login_btn = QPushButton("Login")
        self.login_btn.setObjectName("loginBtn")
        self.login_btn.clicked.connect(self.validate_login)

        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setObjectName("line")

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setObjectName("line")

        or_label = QLabel("OR")
        or_label.setObjectName("orLabel")

        or_divider = QHBoxLayout()
        or_divider.addWidget(line1)
        or_divider.addWidget(or_label)
        or_divider.addWidget(line2)

        self.signup_btn = QPushButton("Sign up for an account")
        self.signup_btn.setObjectName("signupBtn")
        if switch_to_signup:
            self.signup_btn.clicked.connect(switch_to_signup)

        # Add widgets to form layout
        form_layout.addWidget(self.titleLabel)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addLayout(remember_forgot_row)  # <- correct placement
        form_layout.addWidget(self.login_btn)
        form_layout.addLayout(or_divider)
        form_layout.addWidget(self.signup_btn)

        layout.addLayout(form_layout, 2)

    def validate_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        # Add actual auth logic here
        QMessageBox.information(self, "Login Success", f"Welcome {username}!")
