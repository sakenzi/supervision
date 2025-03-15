import time
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QGridLayout, QTextEdit
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPalette, QColor

class MonitoringWindow(QMainWindow):
    def __init__(self, username, code, close_callback):
        super().__init__()
        self.setWindowTitle("Мониторинг")
        self.setGeometry(150, 150, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
        """)

        self.close_callback = close_callback
        self.start_time = time.time()
        self.current_image_index = 0
        self.image_files = ["image/1.png", "image/2.png", "image/3.png"]  

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        
        self.timer_label = QLabel("Тайминг: 0 сек")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("""
            QLabel {
                background-color: #FFFFFF;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
                font-size: 16px;
                color: #333333;
            }
        """)
        left_layout.addWidget(self.timer_label)
        
        self.wish_label = QLabel("Удачи в задачах!")
        self.wish_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wish_label.setStyleSheet("""
            QLabel {
                background-color: #E8F0FE;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                color: #1E90FF;
            }
        """)
        left_layout.addWidget(self.wish_label)

        self.main_layout.addLayout(left_layout, 1)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        self.main_image_label = QLabel()
        self.main_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_image_label.setStyleSheet("""
            QLabel {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                padding: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
        """)
        self.update_main_image()
        right_layout.addWidget(self.main_image_label)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        for i in range(len(self.image_files)):
            btn = QPushButton(str(i + 1))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1E90FF;
                    color: white;
                    border-radius: 15px;
                    padding: 8px 15px;
                    font-size: 14px;
                    border: 1px solid #1E90FF;
                }
                QPushButton:hover {
                    background-color: #104E8B;
                }
            """)
            btn.clicked.connect(lambda checked, idx=i: self.switch_image(idx))
            button_layout.addWidget(btn)
        right_layout.addLayout(button_layout)

        self.notepad = QTextEdit()
        self.notepad.setPlaceholderText("Введите заметки здесь...")
        self.notepad.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #333333;
            }
            QTextEdit:focus {
                border: 1px solid #1E90FF;
                box-shadow: 0 0 5px rgba(30, 144, 255, 0.3);
            }
        """)
        right_layout.addWidget(self.notepad)

        self.close_button = QPushButton("Закрытие")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4040;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 16px;
                border: 1px solid #FF4040;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        self.close_button.clicked.connect(self.close)
        right_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(right_layout, 3)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  

    def update_main_image(self):
        if self.image_files and 0 <= self.current_image_index < len(self.image_files):
            pixmap = QPixmap(self.image_files[self.current_image_index])
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.main_image_label.setPixmap(scaled_pixmap)
            else:
                self.main_image_label.setText("Изображение не найдено")

    def switch_image(self, index):
        self.current_image_index = index
        self.update_main_image()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.setText(f"Тайминг: {elapsed} сек")

    def closeEvent(self, event):
        self.timer.stop()
        self.close_callback()
        event.accept()