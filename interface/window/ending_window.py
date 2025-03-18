from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class ConfirmCloseWindow(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Растау")
        self.setGeometry(300, 300, 300, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        question_label = QLabel("Сіз шынымен шыққыңыз келеді ме?\n Мүмкін тапсырма жауаптарын бір тексеріп шығарсыз!")
        question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        question_label.setStyleSheet("""
            QLabel{
                font-size: 16px;
                color: #333333;
            }
        """)
        layout.addWidget(question_label)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        yes_button = QPushButton("Иә,аяқтағым келеді\n Мен өзіме сенімдімін!")
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4040;
                color: white;
                border-radius: 10px;
                padding: 8px 20px;
                font-size: 14px;
                border: 1px solid #FF4040;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        yes_button.clicked.connect(self.accept)
        button_layout.addWidget(yes_button)

        no_button = QPushButton("Өзіме сенімді емеспін,\n Тағы бір тексеріп алайын")
        no_button.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                border-radius: 10px;
                padding: 8px 20px;
                font-size: 14px;
                border: 1px solid #1E90FF;
            }
            QPushButton:hover {
                background-color: #104E8B;
            }
        """)
        no_button.clicked.connect(self.reject)
        button_layout.addWidget(no_button)

        layout.addLayout(button_layout)

    def exec(self):
        result = super().exec()
        return result == QDialog.DialogCode.Accepted