import base64
import json
import os
import threading
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
import websocket
import requests
from interface.system.notification_manager import NotificationManager
from information.system_info import SystemInfo
import time

class MainWindow(QMainWindow):
    task_received = pyqtSignal(dict, list)

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

        self.notification_manager = NotificationManager()
        self.sys_info = SystemInfo()
        self.task_data = None
        self.image_path = []
        self.is_processing = False

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
        self.start_button.clicked.connect(self.start_process)
        self.layout.addWidget(self.start_button)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.image_label)

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

        self.task_received.connect(self.handle_task_received)

    def get_inputs(self):
        return self.username_input.text(), self.code_input.text()

    def show_loading(self):
        self.loading_label.setVisible(True)
        self.central_widget.setEnabled(False)

    def hide_loading(self):
        self.loading_label.setVisible(False)
        self.central_widget.setEnabled(True)

    def show_notification(self, title, message):
        self.notification_manager.show_notification(title, message)

    def send_to_api(self, data):
        try:
            print(f"Отправляемые данные: {data}")
            response = requests.post("http://localhost:8000/auth/client/login", json=data, timeout=5)
            if response.status_code == 200:
                print(f"Данные успешно отправлены на API: {response.status_code}")
                self.show_notification("Сәтті", "Деректер API-ға сәтті жіберілді!")
                return True
            else:
                print(f"Ошибка отправки данных на API: {response.status_code} - {response.text}")
                self.show_notification("Қате", f"API-ға жіберу қатесі: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Ошибка отправки данных на API: {e}")
            self.show_notification("Қате", "API-ға қосылу кезінде қате пайда болды!")
            return False

    def on_message(self, ws, message):
        print(f"Получено сообщение от WebSocket: {message}")
        try:
            data = json.loads(message)
            image_paths = []
            for key, value in data.items():
                filename = value.get("filename")
                base64_data = value.get("data")

                if filename and base64_data:
                    image_data = base64.b64decode(base64_data)

                    image_dir = os.path.join(os.path.dirname(__file__), "image")
                    os.makedirs(image_dir, exist_ok=True)
                    image_path = os.path.join(image_dir, filename)

                    with open(image_path, "wb") as f:
                        f.write(image_data)
                    print(f"Изображение сохранено: {image_path}")
                    image_paths.append(image_path)

            self.task_received.emit(data, image_paths)
        except json.JSONDecodeError as e:
            print(f"Сообщение не является JSON: {message}")
        except Exception as e:
            print(f"Ошибка при обработке сообщения WebSocket: {e}")
            self.show_notification("Қате", "Тапсырманы қабылдау кезінде қате пайда болды!")
            self.hide_loading()

    def on_error(self, ws, error):
        print(f"Ошибка WebSocket: {error}")
        self.show_notification("Қате", "WebSocket қосылу кезінде қате пайда болды!")
        self.hide_loading()
        self.is_processing = False

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket жабылды: {close_status_code} - {close_msg}")
        self.hide_loading()
        self.is_processing = False

    def on_open(self, ws):
        print("WebSocket қосылды")
        self.show_notification("Сәтті", "WebSocket-қа сәтті қосылды!")

    def start_process(self):
        if self.is_processing:
            print("Процесс уже выполняется, игнорируем повторный вызов")
            return

        self.is_processing = True  
        print("Метод start_process вызван")
        username, code = self.get_inputs()
        if not username or not code:
            self.show_notification("Қате", "Қолданушы аты-жөні және код толтырылуы керек!")
            self.is_processing = False
            return

        data = {
            "code": code,
            "ip_address": self.sys_info.get_ip_address(),
            "mac_address": self.sys_info.get_mac_address(),
            "username": username,
            "device_info": self.sys_info.get_pc_name()
        }
        
        self.show_loading()

        if not self.send_to_api(data):
            self.hide_loading()
            return

        time.sleep(1)

        ws_url = "ws://localhost:8000/tasks/ws"
        ws = websocket.WebSocketApp(
            ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        threading.Thread(target=ws.run_forever, daemon=True).start()

    def handle_task_received(self, task_data, image_paths):
        self.task_data = task_data
        self.image_paths = image_paths  
        self.show_notification("Сәтті", "Тапсырма сәтті қабылданды!")
        self.hide_loading()
        self.is_processing = False
        self.open_monitoring_window()

    def open_monitoring_window(self):
        pass