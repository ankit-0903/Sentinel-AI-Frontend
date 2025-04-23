import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QIcon
from ui.signup_page import SignupPage
from ui.login_page import LoginPage
from ui.dashboard import DashboardPage


class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Initialize pages with callback references
        self.signup_page = SignupPage(self.show_login)  
        self.login_page = LoginPage(self.show_signup, self.show_dashboard)
        self.dashboard = DashboardPage()

        # Add all pages to the stacked widget
        self.addWidget(self.login_page)
        self.addWidget(self.signup_page)
        self.addWidget(self.dashboard)

        # Start with the login page
        self.setCurrentWidget(self.login_page)

    def show_login(self):
        self.setCurrentWidget(self.login_page)

    def show_signup(self):
        self.setCurrentWidget(self.signup_page)

    def show_dashboard(self):
        self.setCurrentWidget(self.dashboard)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Sentinel AI")

    # ✅ Load external stylesheet
    try:
        with open("ui/style.qss", "r") as file:
            style = file.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("⚠️  Warning: style.qss not found. Running without styles.")

    # ✅ Create and configure main window
    window = MainApp()
    window.setWindowTitle("Sentinel AI")
    window.setFixedSize(1000, 700)  # Set your desired window size

    # ✅ Set window icon (if it exists)
    try:
        window.setWindowIcon(QIcon("assets/icon.png"))
    except Exception as e:
        print("⚠️  Could not load icon:", e)

    # ✅ Center the window on screen
    screen = app.primaryScreen().availableGeometry()
    x = (screen.width() - window.width()) // 2
    y = (screen.height() - window.height()) // 2
    window.move(x, y)

    window.show()
    sys.exit(app.exec_())
