from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMenu, QLineEdit, QApplication
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSystemTrayIcon
from information.system_info import SystemInfo
from information.user_monitor import UserMonitor
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("kӨz")
        self.setGeometry(100, 100, 400, 300)

        self.sys_info = SystemInfo()
        self.user_monitor = UserMonitor()

        self.setup_ui()
        self.setup_tray()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        self.code_label = QLabel("Введите код:")
        self.code_input = QLineEdit()
        self.layout.addWidget(self.code_label)
        self.layout.addWidget(self.code_input)

        self.start_button = QPushButton("Начать")
        self.start_button.clicked.connect(self.start_monitoring)
        self.layout.addWidget(self.start_button)

        self.mac_label = QLabel()
        self.ip_label = QLabel()
        self.pc_name_label = QLabel()

        self.layout.addWidget(self.mac_label)
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.pc_name_label)

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon/eye-icon-4.png"))  

        tray_menu = QMenu()
        show_action = QAction("Показать", self)
        quit_action = QAction("Выход", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_clicked)

    def start_monitoring(self):
        username = self.username_input.text()
        code = self.code_input.text()
        print(f"{time.ctime()}: Имя пользователя: {username}")
        print(f"{time.ctime()}: Код: {code}")

        self.show_system_info()
        self.user_monitor.start()
        self.hide()

    def show_system_info(self):
        mac = self.sys_info.get_mac_address()
        ip = self.sys_info.get_ip_address()
        pc_name = self.sys_info.get_pc_name()

        self.mac_label.setText(f"MAC-адрес: {mac}")
        self.ip_label.setText(f"IP-адрес: {ip}")
        self.pc_name_label.setText(f"Имя ПК: {pc_name}")

    def tray_clicked(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()

    def quit_app(self):
        self.user_monitor.stop()
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()