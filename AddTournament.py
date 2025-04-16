import sys
import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QMessageBox, QLineEdit,
    QFormLayout, QLabel, QGraphicsDropShadowEffect,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from Turniej import Turniej

class AddTournamentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dodaj Turniej")
        self.setGeometry(450, 300, 350, 200)
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
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        title = QLabel("➕ Dodaj Turniej")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0a0a0a; background: transparent;")
        layout.addWidget(title)

        self.nazwa_input = QLineEdit()
        self.data_input = QLineEdit()
        self.liczba_stolow_input = QLineEdit()

        layout.addRow(QLabel("Nazwa:"), self.nazwa_input)
        layout.addRow(QLabel("Data:"), self.data_input)
        layout.addRow(QLabel("Liczba Stołów:"), self.liczba_stolow_input)

        add_button = self.create_button("Dodaj", self.save_tournament)
        layout.addWidget(add_button)

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

    def save_tournament(self):
        nazwa = self.nazwa_input.text()
        data = self.data_input.text()
        liczba_stolow = self.liczba_stolow_input.text()

        try:
            liczba_stolow = int(liczba_stolow)

            turniej = Turniej(nazwa, data, liczba_stolow)
            turniej.add_tournament()  # ✅ Poprawione wywołanie metody

            QMessageBox.information(self, "Sukces", "Turniej dodany pomyślnie!")
            self.nazwa_input.clear()
            self.data_input.clear()
            self.liczba_stolow_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Podaj poprawne dane.")
