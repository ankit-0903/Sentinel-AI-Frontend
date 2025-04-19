from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import re
from db.mongo_client import users_collection


class SignupPage(QWidget):
    def __init__(self, switch_to_login=None):
        super().__init__()

        # Use HBox layout for left-right division
        layout = QHBoxLayout(self)
        layout.setContentsMargins(80, 40, 80, 40)
        layout.setSpacing(20)

        # Left side - image section inside a box
        image_box = QFrame(self)
        image_box.setFrameShape(QFrame.StyledPanel)
        image_box.setLineWidth(2)
        image_box.setStyleSheet("border-radius: 10px; border: 1px solid #7d5fff;")

        image_label = QLabel(image_box)
        pixmap = QPixmap("ui//image.png")  # Provide the path to your image
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setScaledContents(True)  # To scale the image to fit the box
        image_box.setLayout(QVBoxLayout())  # To ensure the layout works for the QLabel
        image_box.layout().addWidget(image_label)

        layout.addWidget(image_box, 1)  # Stretch factor to take up remaining space

        # Right side - signup form section
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(15)

        self.titleLabel = QLabel("Create your account")
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Full Name")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm Password")

        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setObjectName("signupBtn")
        self.signup_btn.clicked.connect(self.validate_signup)

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

        self.login_btn = QPushButton("Already have an account?")
        self.login_btn.setObjectName("loginBtn")
        if switch_to_login:
            self.login_btn.clicked.connect(switch_to_login)

        # Add widgets to form layout
        form_layout.addWidget(self.titleLabel)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.fullname_input)
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.confirm_password_input)
        form_layout.addWidget(self.signup_btn)
        form_layout.addLayout(or_divider)
        form_layout.addWidget(self.login_btn)

        # Add form layout to the right side of the main layout
        layout.addLayout(form_layout, 2)  # Stretch factor to take more space on the right

    def validate_signup(self):
        username = self.username_input.text().strip()
        fullname = self.fullname_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not all([username, fullname, phone, email, password, confirm_password]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            QMessageBox.warning(self, "Input Error", "Invalid email address.")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Input Error", "Password must be at least 6 characters long.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Input Error", "Passwords do not match.")
            return

        QMessageBox.information(self, "Success", "Account created successfully!")
        # Insert into DB logic here if needed

