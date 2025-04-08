import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QLineEdit, QFormLayout, QLabel, QPushButton
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox,
    QLineEdit, QFormLayout, QLabel, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from zawodnicy import Zawodnicy


class AddPlayerWindow(QWidget):
    def __init__(self, zawodnicy):
        super().__init__()
        self.zawodnicy = zawodnicy
        self.setWindowTitle("Dodaj Zawodnika")
        self.setGeometry(450, 300, 350, 200)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.imie_input = QLineEdit()
        self.nazwisko_input = QLineEdit()
        self.turniej_input = QLineEdit()

        layout.addRow(QLabel("Imię:"), self.imie_input)
        layout.addRow(QLabel("Nazwisko:"), self.nazwisko_input)
        layout.addRow(QLabel("Turniej ID:"), self.turniej_input)

        add_button = QPushButton("Dodaj")
        add_button.clicked.connect(self.save_player)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def save_player(self):
        imie = self.imie_input.text()
        nazwisko = self.nazwisko_input.text()
        turniej_id = self.turniej_input.text()

        try:
            turniej_id = int(turniej_id)
            self.zawodnicy.add_zawodnik(imie, nazwisko, turniej_id)
            QMessageBox.information(self, "Sukces", "Zawodnik dodany pomyślnie!")
            self.imie_input.clear()
            self.nazwisko_input.clear()
            self.turniej_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Podaj poprawne ID turnieju.")


class ShowPlayersWindow(QWidget):
    def __init__(self, zawodnicy):
        super().__init__()
        self.zawodnicy = zawodnicy
        self.setWindowTitle("Lista Zawodników")
        self.setGeometry(450, 300, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Imię", "Nazwisko", "Turniej ID", "Punkty"])

        refresh_button = QPushButton("Odśwież")
        refresh_button.clicked.connect(self.load_players)

        save_button = QPushButton("Zapisz zmiany punktów")
        save_button.clicked.connect(self.save_points)

        random_button = QPushButton("Wylosuj Punkty")
        random_button.clicked.connect(self.randomize_points)

        layout.addWidget(self.table)
        layout.addWidget(refresh_button)
        layout.addWidget(save_button)
        layout.addWidget(random_button)

        self.setLayout(layout)
        self.load_players()

    def load_players(self):
        zawodnicy = self.zawodnicy.show_zawodnicy()
        zawodnicy.sort(key=lambda z: z[3])  # Sortuj po turniej_id

        self.table.setRowCount(0)
        current_turniej = None
        row_counter = 0

        for zawodnik in zawodnicy:
            id_, imie, nazwisko, turniej_id, punkty = zawodnik

            if turniej_id != current_turniej:
                self.table.insertRow(row_counter)
                item = QTableWidgetItem(f"=== Turniej ID: {turniej_id} ===")
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setSpan(row_counter, 0, 1, 5)
                self.table.setItem(row_counter, 0, item)
                row_counter += 1
                current_turniej = turniej_id

            self.table.insertRow(row_counter)
            self.table.setItem(row_counter, 0, QTableWidgetItem(str(id_)))
            self.table.setItem(row_counter, 1, QTableWidgetItem(imie))
            self.table.setItem(row_counter, 2, QTableWidgetItem(nazwisko))
            self.table.setItem(row_counter, 3, QTableWidgetItem(str(turniej_id)))

            punkty_item = QTableWidgetItem(str(punkty))
            punkty_item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.table.setItem(row_counter, 4, punkty_item)

            row_counter += 1

    def save_points(self):
        rows = self.table.rowCount()
        updated = 0

        for i in range(rows):
            id_item = self.table.item(i, 0)
            punkty_item = self.table.item(i, 4)

            if id_item and id_item.text().isdigit():
                zawodnik_id = int(id_item.text())
                try:
                    nowe_punkty = int(punkty_item.text())
                    self.zawodnicy.update_punkty(zawodnik_id, nowe_punkty)
                    updated += 1
                except ValueError:
                    continue  # pomiń niepoprawne wartości

        QMessageBox.information(self, "Zaktualizowano", f"Punkty zaktualizowane dla {updated} zawodników.")

    def randomize_points(self):
        zawodnicy = self.zawodnicy.show_zawodnicy()
        for z in zawodnicy:
            losowe_punkty = random.randint(0, 1000)
            self.zawodnicy.update_punkty(z[0], losowe_punkty)
        self.load_players()
        QMessageBox.information(self, "Gotowe", "Punkty zostały wylosowane!")


class TournamentManager(QWidget):
    def __init__(self):
        super().__init__()
        self.zawodnicy = Zawodnicy()
        self.zawodnicy.create_table()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        add_tournament_button = QPushButton("Dodaj Turniej", self)
        show_tournaments_button = QPushButton("Wyświetl Turnieje", self)
        add_player_button = QPushButton("Dodaj Zawodnika", self)
        show_players_button = QPushButton("Wyświetl Zawodników", self)

        add_tournament_button.clicked.connect(self.add_tournament)
        show_tournaments_button.clicked.connect(self.show_tournaments)
        add_player_button.clicked.connect(self.open_add_player)
        show_players_button.clicked.connect(self.open_show_players)

        layout.addWidget(add_tournament_button)
        layout.addWidget(show_tournaments_button)
        layout.addWidget(add_player_button)
        layout.addWidget(show_players_button)

        self.setLayout(layout)
        self.setWindowTitle("Menadżer Turniejów")
        self.showFullScreen()  # ← FULLSCREEN tutaj

    def add_tournament(self):
        self.add_tournament_window = AddTournamentWindow()
        self.add_tournament_window.show()

    def show_tournaments(self):
        self.show_tournaments_window = ShowTournamentsWindow()
        self.show_tournaments_window.show()

    def open_add_player(self):
        self.add_player_window = AddPlayerWindow(self.zawodnicy)
        self.add_player_window.show()

    def open_show_players(self):
        self.show_players_window = ShowPlayersWindow(self.zawodnicy)
        self.show_players_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TournamentManager()
    sys.exit(app.exec_())
