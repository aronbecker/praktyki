import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QGraphicsDropShadowEffect, QFormLayout, QLineEdit, QDialog, QMessageBox
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from Table import Table
class SetPointsWindow(QDialog):
    def __init__(self, table_id, player_1, player_2, player_3, player_4,
                 punkty_1=0, punkty_2=0, punkty_3=0, punkty_4=0, parent=None):
        super().__init__(parent)
        self.table_id = table_id
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_3 = player_3
        self.player_4 = player_4
        self.punkty_1 = punkty_1
        self.punkty_2 = punkty_2
        self.punkty_3 = punkty_3
        self.punkty_4 = punkty_4

        # tutaj dalszy kod GUI i inicjalizacji

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

        confirm_button = self.create_button("Zatwierdź", self.confirm_points)
        layout.addWidget(confirm_button)
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
    def confirm_points(self):
        try:
            self.punkty_1 = int(self.points_input_1.text())
            self.punkty_2 = int(self.points_input_2.text())
            self.punkty_3 = int(self.points_input_3.text())
            self.punkty_4 = int(self.points_input_4.text())
            Table.set_points(self, self.table_id, self.punkty_1, self.punkty_2, self.punkty_3, self.punkty_4)
            QMessageBox.information(self, "Sukces", "Punkty zostały pomyślnie zapisane.")
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Proszę wprowadzić poprawne liczby.")
            return