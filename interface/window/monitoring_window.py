import time
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, 
                             QTextEdit, QTabWidget, QScrollArea, QDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QKeyEvent
from interface.window.ending_window import ConfirmCloseWindow
from interface.system.notification_manager import NotificationManager

class ImageZoomDialog(QDialog):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Увеличенное изображение")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout(self)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setPixmap(pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(self.image_label)

        close_button = QPushButton("Жабу")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4040;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

class MonitoringWindow(QMainWindow):
    def __init__(self, task_data, image_paths, close_callback):
        super().__init__()
        self.setWindowTitle("Сынақ алаңы")
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
        self.task_data = task_data
        self.image_paths = image_paths if isinstance(image_paths, list) else [image_paths]
        self.notification_manager = NotificationManager()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Левая часть: таймер и пожелание
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

        self.wish_label = QLabel("Сынақты жақсы тапсырып шығуыңа тілектеспін студент!")
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

        # Правая часть: табы с изображениями, текст задания и блокнот
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        self.task_label = QLabel("Тапсырма: Жоқ")
        if self.task_data:
            task_text = self.task_data.get("task", "Тапсырма жоқ")
            self.task_label.setText(f"Тапсырма: {task_text}")
        self.task_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.task_label.setStyleSheet("""
            QLabel {
                background-color: #E8F0FE;
                padding: 5px;
                font-size: 16px;
                color: #1E90FF;
                border-bottom: 1px solid #E0E0E0;
            }
        """)
        right_layout.addWidget(self.task_label)

        # Вкладки для изображений
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                background: #FFFFFF;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #E8F0FE;
                color: #1E90FF;
                padding: 8px 16px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #1E90FF;
                color: #FFFFFF;
            }
        """)

        for idx, image_path in enumerate(self.image_paths):
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            image_container = QWidget()
            image_layout = QVBoxLayout(image_container)

            image_label = QLabel()
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("""
                QLabel {
                    background-color: #FFFFFF;
                    border: 1px solid #E0E0E0;
                    border-radius: 5px;
                    padding: 10px;
                }
            """)
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                image_label.setPixmap(scaled_pixmap)
                # Делаем изображение кликабельным для увеличения
                image_label.setCursor(Qt.CursorShape.PointingHandCursor)
                image_label.mousePressEvent = lambda event, p=pixmap: self.show_zoomed_image(p)
            else:
                image_label.setText(f"Сурет табылмады: {image_path}")

            image_layout.addWidget(image_label)
            scroll_area.setWidget(image_container)
            tab_layout.addWidget(scroll_area)
            self.tab_widget.addTab(tab, f"Сурет {idx + 1}")

        right_layout.addWidget(self.tab_widget)

        self.notepad = QTextEdit()
        self.notepad.setPlaceholderText("Тапсырма жауабын жазыңыз...")
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
            }
        """)
        right_layout.addWidget(self.notepad)

        self.close_button = QPushButton("Аяқтау")
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
        self.close_button.clicked.connect(self.on_close_clicked)
        right_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(right_layout, 3)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def show_zoomed_image(self, pixmap):
        dialog = ImageZoomDialog(pixmap, self)
        dialog.exec()

    def on_close_clicked(self):
        self.notification_manager.show_notification("Ескерту", "Сынақты аяқтауға дайынсыз ба?")
        confirm_window = ConfirmCloseWindow(self)
        if confirm_window.exec():
            self.close()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.setText(f"Тайминг: {elapsed} сек")

    def closeEvent(self, event):
        self.timer.stop()
        self.close_callback()
        event.accept()