import time
from PyQt6.QtCore import Qt
from .window.main_window import MainWindow
from .system.tray_manager import TrayManager
from .system.system_info_display import SystemInfoDisplay
from .system.loading_screen import LoadingScreen
from .window.monitoring_window import MonitoringWindow
from information.system_info import SystemInfo
from information.user_monitor import UserMonitor
from api.api_client import ApiClient

class UI(MainWindow):
    def __init__(self):
        super().__init__()

        self.sys_info = SystemInfo()
        self.user_monitor = UserMonitor()
        self.tray_manager = TrayManager(self)
        self.info_display = SystemInfoDisplay(self.mac_label, self.ip_label, self.pc_name_label, self.sys_info)
        self.loading_screen = LoadingScreen(self)
        self.monitoring_window = None
        self.api_client = ApiClient("http://localhost:8000/auth/client/login")

        self.start_button.clicked.connect(self.start_monitoring)

    def start_monitoring(self):
        self.username, self.code = self.get_inputs()

        data = {
            "code": self.code,
            "ip_address": self.sys_info.get_ip_address(),
            "mac_address": self.sys_info.get_mac_address(),
            "username": self.username,
            "device_name": self.sys_info.get_pc_name()
        }

        print(data)
        if self.api_client.send_data(self, data):
            print(f"{time.ctime()}: Имя пользователя: {self.username}")
            print(f"{time.ctime()}: Код: {self.code}")

            self.info_display.show_system_info()
            self.loading_screen.show(2000, self.finish_monitoring)
        else:
            return

    def finish_monitoring(self):
        self.monitoring_window = MonitoringWindow(self.username, self.code, self.user_monitor.stop)
        self.monitoring_window.show()
        self.user_monitor.start()
        self.hide()

    def closeEvent(self, event):
        event.ignore()
        self.hide()