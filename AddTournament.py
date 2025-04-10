import sys
import sqlite3
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, QFormLayout, QLabel
from Turniej import Turniej

class AddTournamentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dodaj Turniej")
        self.setGeometry(450, 300, 350, 200)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.nazwa_input = QLineEdit()
        self.data_input = QLineEdit()
        self.liczba_stolow_input = QLineEdit()
        self.liczba_rund_input = QLineEdit()

        layout.addRow(QLabel("Nazwa:"), self.nazwa_input)
        layout.addRow(QLabel("Data:"), self.data_input)
        layout.addRow(QLabel("Liczba Stołów:"), self.liczba_stolow_input)
        layout.addRow(QLabel("Liczba Rund:"), self.liczba_rund_input)

        add_button = QPushButton("Dodaj")
        add_button.clicked.connect(self.save_tournament)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def save_tournament(self):
        nazwa = self.nazwa_input.text()
        data = self.data_input.text()
        liczba_stolow = self.liczba_stolow_input.text()
        liczba_rund = self.liczba_rund_input.text()

        try:
            liczba_stolow = int(liczba_stolow)
            liczba_rund = int(liczba_rund)

            turniej = Turniej(nazwa, data, liczba_stolow, liczba_rund)
            turniej.add_tournament(turniej.name, turniej.date, turniej.tables, turniej.rounds)

            QMessageBox.information(self, "Sukces", "Turniej dodany pomyślnie!")
            self.nazwa_input.clear()
            self.data_input.clear()
            self.liczba_stolow_input.clear()
            self.liczba_rund_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Podaj poprawne dane.")