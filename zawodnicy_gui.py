import random
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpacerItem,
    QSizePolicy
)
from PyQt5.QtCore import Qt


class AddPlayerWindow(QWidget):
    def __init__(self, zawodnicy):
        super().__init__()
        self.zawodnicy = zawodnicy
        self.setWindowTitle("Dodaj Zawodnika")
        self.setGeometry(400, 250, 500, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.setSpacing(20)

        self.imie_input = QLineEdit()
        self.nazwisko_input = QLineEdit()
        self.turniej_input = QLineEdit()

        self.imie_input.setPlaceholderText("Wpisz imię")
        self.nazwisko_input.setPlaceholderText("Wpisz nazwisko")
        self.turniej_input.setPlaceholderText("Numer turnieju")

        form_layout.addRow(QLabel("Imię:"), self.imie_input)
        form_layout.addRow(QLabel("Nazwisko:"), self.nazwisko_input)
        form_layout.addRow(QLabel("Turniej ID:"), self.turniej_input)

        add_button = QPushButton("➕ Dodaj Zawodnika")
        add_button.setStyleSheet("padding: 10px; font-weight: bold;")
        add_button.clicked.connect(self.save_player)

        layout.addLayout(form_layout)
        layout.addWidget(add_button)
        layout.setContentsMargins(40, 30, 40, 30)
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
        self.setGeometry(350, 200, 1000, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📋 Lista Zawodników")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Imię", "Nazwisko", "Turniej ID", "Punkty"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("font-size: 14px;")

        # Przyciski pod tabelą
        buttons_layout = QHBoxLayout()
        refresh_button = QPushButton("🔄 Odśwież")
        save_button = QPushButton("💾 Zapisz zmiany punktów")
        random_button = QPushButton("🎲 Wylosuj Punkty")

        for btn in [refresh_button, save_button, random_button]:
            btn.setStyleSheet("padding: 10px; font-weight: bold;")

        refresh_button.clicked.connect(self.load_players)
        save_button.clicked.connect(self.save_points)
        random_button.clicked.connect(self.randomize_points)

        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(refresh_button)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(random_button)
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)
        layout.setContentsMargins(30, 30, 30, 30)

        self.setLayout(layout)
        self.load_players()

    def load_players(self):
        zawodnicy = self.zawodnicy.show_zawodnicy()
        zawodnicy.sort(key=lambda z: z[3])  # sortuj po turniej_id

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
                    continue

        QMessageBox.information(self, "Zaktualizowano", f"Punkty zaktualizowane dla {updated} zawodników.")

    def randomize_points(self):
        zawodnicy = self.zawodnicy.show_zawodnicy()
        for z in zawodnicy:
            losowe_punkty = random.randint(0, 1000)
            self.zawodnicy.update_punkty(z[0], losowe_punkty)
        self.load_players()
        QMessageBox.information(self, "Gotowe", "Punkty zostały wylosowane!")
