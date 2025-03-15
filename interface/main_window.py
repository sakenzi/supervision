from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информация о системе")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        self.code_label = QLabel("Код:")
        self.code_input = QLineEdit()
        self.layout.addWidget(self.code_label)
        self.layout.addWidget(self.code_input)

        self.start_button = QPushButton("Начать")
        self.layout.addWidget(self.start_button)

        self.mac_label = QLabel()
        self.ip_label = QLabel()
        self.pc_name_label = QLabel()

        self.layout.addWidget(self.mac_label)
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.pc_name_label)

        self.loading_label = QLabel("Загрузка...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet("font-size: 20px; color: blue;")
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