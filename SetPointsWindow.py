import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QGraphicsDropShadowEffect, QFormLayout, QLineEdit
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt

class SetPointsWindow(QWidget):
    def __init__(self, name, player_1, player_2, player_3, player_4):
        super().__init__()
        self.name = name
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_3 = player_3
        self.player_4 = player_4
        self.setWindowTitle("Ustaw Punkty")
        self.setGeometry(450, 300, 350, 300)
        self.init_ui()
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2691f7,
                    stop: 1 #e6f3ff
                );
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid #c0deff;
                border-radius: 12px;
                padding: 8px 12px;
                font-size: 15px;
                min-height: 30px;
            }
        """)
    def init_ui(self):
        layout = QFormLayout()
        title = QLabel("Ustaw Punkty")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0a0a0a; background: transparent;")
        layout.addWidget(title)

        self.points_input_1 = QLineEdit()
        self.points_input_2 = QLineEdit()
        self.points_input_3 = QLineEdit()
        self.points_input_4 = QLineEdit()

        layout.addRow(QLabel(f"{self.player_1}:"), self.points_input_1)
        layout.addRow(QLabel(f"{self.player_2}:"), self.points_input_2)
        layout.addRow(QLabel(f"{self.player_3}:"), self.points_input_3)
        layout.addRow(QLabel(f"{self.player_4}:"), self.points_input_4)

        self.setLayout(layout)


    def create_button(self, text, action):
        button = QPushButton(text)
        button.setMinimumHeight(52)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 40))
        button.setGraphicsEffect(shadow)

        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.85);
                border: 1px solid #c0deff;
                border-radius: 18px;
                padding: 12px 24px;
                font-size: 17px;
                font-family: 'Segoe UI', sans-serif;
                color: #1a1a1a;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.95);
            }
            QPushButton:pressed {
                background-color: rgba(230, 244, 255, 0.95);
            }
        """)

        button.clicked.connect(action)
        return button
