import time
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTextEdit, QTabWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QKeyEvent
from interface.window.fullscreen_image import FullScreenImageWindow
from interface.window.ending_window import  ConfirmCloseWindow


class MonitoringWindow(QMainWindow):
    def __init__(self, username, code, close_callback):
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

        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                border-radius: 0 0 10px 10px;
                background-color: #FFFFFF;
            }
            QTabBar::tab {
                background-color: #F0F0F0;
                color: #333333;
                border: 1px solid #D0D0D0;
                border-bottom: none;
                padding: 8px 15px;
                font-size: 14px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #FFFFFF;
                border-bottom: 1px solid #FFFFFF;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #E0E0E0;
            }
        """)
        self.tab_widget.currentChanged.connect(self.switch_image)  

        self.image_labels = []
        self.notepads = []
        self.titles = []
        for i, image_path in enumerate(self.image_files):
            tab_widget = QWidget()
            tab_layout = QVBoxLayout(tab_widget)
            tab_layout.setSpacing(10)

            title_label = QLabel(f"Тақырып {i + 1}")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet("""
                QLAbel {
                    background-color: #E8F0FE;
                    radding: 5px;
                    font-size: 16px;
                    color: #1E90FF;
                    border-bottom: 1px solid #E0E0E0;
                }
            """)
            tab_layout.addWidget(title_label)
            self.titles.append(title_label)

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
            image_label.setMouseTracking(True)
            image_label.mousePressEvent = lambda event, idx=i: self.show_fullscreen_image(event, idx)
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                image_label.setPixmap(scaled_pixmap)
            else:
                image_label.setText("Сурет табылмады")
            tab_layout.addWidget(image_label)
            self.image_labels.append(image_label)

            notepad = QTextEdit()
            notepad.setPlaceholderText("Тапсырма жауабын жазыңыз...")
            notepad.setStyleSheet("""
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
            tab_layout.addWidget(notepad)
            self.notepads.append(notepad)

            self.tab_widget.addTab(tab_widget, str(i + 1))

        right_layout.addWidget(self.tab_widget)

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

    def on_close_clicked(self):
        confirm_window = ConfirmCloseWindow(self)
        if confirm_window.exec():
            self.close()

    def show_fullscreen_image(self, event, index):
        print("Открываем FullScreenImageWindow")
        pixmap = QPixmap(self.image_files[index])
        if not pixmap.isNull():
            fullscreen_window = FullScreenImageWindow(pixmap, self)
            print("Экземпляр создан, вызываем show")
            fullscreen_window.show()
        else:
            print("Ошибка: изображение не загружено")

    def switch_image(self, index):
        self.tab_widget.setCurrentIndex(index)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Tab and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            print("Ctrl+Tab нажат, переключаем вкладку")
            current_index = self.tab_widget.currentIndex()
            next_index = (current_index + 1) % self.tab_widget.count()
            self.tab_widget.setCurrentIndex(next_index)
        super().keyPressEvent(event)

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.setText(f"Тайминг: {elapsed} сек")

    def closeEvent(self, event):
        self.timer.stop()
        self.close_callback()
        event.accept()