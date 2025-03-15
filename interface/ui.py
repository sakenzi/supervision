from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from information.system_info import SystemInfo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информация о системе")
        self.setGeometry(100, 100, 400, 200)

        self.sys_info = SystemInfo()

        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.start_button = QPushButton("Начать")
        self.start_button.clicked.connect(self.show_system_info)
        self.layout.addWidget(self.start_button)

        self.mac_label = QLabel("MAC-адрес: ")
        self.ip_label = QLabel("IP-адрес: ")
        self.pc_name_label = QLabel("Имя ПК: ")

        self.layout.addWidget(self.mac_label)
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.pc_name_label)

    def show_system_info(self):
        mac = self.sys_info.get_mac_address()
        ip = self.sys_info.get_ip_address()
        pc_name = self.sys_info.get_pc_name()

        self.mac_label.setText(f"MAC-адрес: {mac}")
        self.ip_label.setText(f"IP-адрес: {ip}")
        self.pc_name_label.setText(f"Имя ПК: {pc_name}")