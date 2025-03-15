import time
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap

class MonitoringWindow(QMainWindow):
    def __init__(self, username, code, close_callback):
        super().__init__()
        self.setWindowTitle("Мониторинг")
        self.setGeometry(150, 150, 800, 600)

        self.close_callback = close_callback
        self.start_time = time.time()
        self.current_image_index = 0
        self.image_files = ["image/1.png", "image/2.png", "image/3.png"]  

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        left_layout = QVBoxLayout()
        
        self.timer_label = QLabel("Тайминг: 0 сек")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.timer_label)
        
        self.wish_label = QLabel("Удачи в задачах!")
        self.wish_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.wish_label)

        self.main_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()

        self.main_image_label = QLabel()
        self.main_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_main_image()
        right_layout.addWidget(self.main_image_label)

        button_layout = QHBoxLayout()
        for i in range(len(self.image_files)):
            btn = QPushButton(str(i + 1))
            btn.clicked.connect(lambda checked, idx=i: self.switch_image(idx))
            button_layout.addWidget(btn)
        right_layout.addLayout(button_layout)

        self.close_button = QPushButton("Закрытие")
        self.close_button.clicked.connect(self.close)
        right_layout.addWidget(self.close_button)

        self.main_layout.addLayout(right_layout)

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

    def append_event(self, event):
        pass  

    def closeEvent(self, event):
        self.timer.stop()
        self.close_callback()
        event.accept()