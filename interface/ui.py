import time
from PyQt6.QtCore import Qt
from interface.main_window import MainWindow
from interface.tray_manager import TrayManager
from interface.system_info_display import SystemInfoDisplay
from interface.loading_screen import LoadingScreen
from information.system_info import SystemInfo
from information.user_monitor import UserMonitor


class UI(MainWindow):
    def __init__(self):
        super().__init__()

        self.sys_info = SystemInfo()
        self.user_monitor = UserMonitor()
        self.tray_manager = TrayManager(self)
        self.info_display = SystemInfoDisplay(self.mac_label, self.ip_label, self.pc_name_label, self.sys_info)
        self.loading_screen = LoadingScreen(self)

        self.start_button.clicked.connect(self.start_monitoring)

    def start_monitoring(self):
        username, code = self.get_inputs()
        print(f"{time.ctime()}: Имя пользователя: {username}")
        print(f"{time.ctime()}: Код: {code}")

        self.info_display.show_system_info()
        self.loading_screen.show(2000, self.finish_monitoring)  

    def finish_monitoring(self):
        self.user_monitor.start()
        self.hide()

    def closeEvent(self, event):
        event.ignore()
        self.hide()