from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QApplication, QWidget
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap
import sys

class FullScreenImageWindow(QMainWindow):
    def __init__(self, pixmap_path, parent=None):
        super().__init__(parent)
        print("Инициализация FullScreenImageWindow")  
        
        self.showFullScreen()
        self.setWindowTitle("Полноэкранное изображение")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel(central_widget)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: black;")

        self.pixmap = QPixmap(pixmap_path)
        if not self.pixmap.isNull():
            print("Изображение загружено успешно")
            self.image_label.setPixmap(self.pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            print("Ошибка: изображение не загружено")
            self.image_label.setText("Изображение не найдено")

        layout.addWidget(self.image_label)

        self.image_label.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.image_label and event.type() == QEvent.Type.MouseButtonPress:
            print("Закрытие по клику")
            self.close()
            return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            print("Закрытие по Esc")
            self.close()

    def closeEvent(self, event):
        print("Окно закрыто")
        super().closeEvent(event)