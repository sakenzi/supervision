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

        self.start_button.clicked.connect(self.start_process)

    def open_monitoring_window(self):
        self.monitoring_window = MonitoringWindow(self.task_data, self.image_path, self.user_monitor.stop)
        self.monitoring_window.show()
        self.user_monitor.start()
        self.hide()

    def closeEvent(self, event):
        event.ignore()
        self.hide()