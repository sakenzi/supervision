from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from plyer import notification
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("kӨz")
        self.setGeometry(100, 100, 400, 500)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel("Сынақ алаңына өту")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.title_label)

        self.username_label = QLabel("Қолданушы аты-жөні:")
        self.username_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #555555;
                padding-bottom: 5px;
            }
        """)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Аты-жөніңізді жазыңыз:")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 1px solid #1E90FF;
                box-shadow: 0 0 5px rgba(30, 144, 255, 0.3);
            }
        """)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        self.code_label = QLabel("Код:")
        self.code_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #555555;
                padding-bottom: 5px;
            }
        """)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Кодты жазыңыз:")
        self.code_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 1px solid #1E90FF;
                box-shadow: 0 0 5px rgba(30, 144, 255, 0.3);
            }
        """)
        self.layout.addWidget(self.code_label)
        self.layout.addWidget(self.code_input)

        self.start_button = QPushButton("Бастау")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #104E8B;
            }
            QPushButton:pressed {
                background-color: #0A3D62;
            }
        """)
        self.start_button.clicked.connect(self.show_notification)  
        self.layout.addWidget(self.start_button)

        self.mac_label = QLabel()
        self.ip_label = QLabel()
        self.pc_name_label = QLabel()

        self.layout.addWidget(self.mac_label)
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.pc_name_label)

        self.loading_label = QLabel("Күтіңіз...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #1E90FF;
                background-color: #E8F0FE;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.loading_label.setVisible(False)
        self.layout.addWidget(self.loading_label)

    def get_inputs(self):
        return self.username_input.text(), self.code_input.text()

    def show_loading(self):
        self.loading_label.setVisible(True)
        self.central_widget.setEnabled(False)  

    def hide_loading(self):
        self.loading_label.setVisible(False)
        self.central_widget.setEnabled(True)   

    def show_notification(self):
        # icon_path = os.path.join(os.path.dirname(__file__), "icon", "icon/eye-icon-4.ico")
        username, code = self.get_inputs()
        if not username or not code:
            notification.notify(
                title="Қате",
                message="Қолданушы аты-жөні және код толтырылуы керек!",
                app_name="kӨz",
                timeout=7,
                app_icon=r"icon/eye-icon-4.ico"
            )
        else:
            notification.notify(
                title="Студент сынақ басталды",
                message="Ойланып, асықпай орындап шық!",
                app_name="kӨz",
                timeout=7,
                app_icon=r'icon/eye-icon-4.ico'
            )
            self.show_loading()  