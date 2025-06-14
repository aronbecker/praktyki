import random
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpacerItem,
    QSizePolicy, QGraphicsDropShadowEffect, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from zawodnicy import Zawodnicy


class AddPlayerWindow(QWidget):
    def __init__(self, zawodnicy):
        super().__init__()
        self.zawodnicy = zawodnicy
        self.setWindowTitle("Dodaj Zawodnika")
        self.setGeometry(400, 250, 500, 300)

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
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.setSpacing(20)

        title = QLabel("➕ Dodaj Zawodnika")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0a0a0a; background: transparent;")
        layout.addWidget(title)

        self.imie_input = QLineEdit()
        self.nazwisko_input = QLineEdit()
        self.turniej_input = QLineEdit()

        self.imie_input.setPlaceholderText("Wpisz imię")
        self.nazwisko_input.setPlaceholderText("Wpisz nazwisko")
        self.turniej_input.setPlaceholderText("Numer turnieju")

        form_layout.addRow(QLabel("Imię:"), self.imie_input)
        form_layout.addRow(QLabel("Nazwisko:"), self.nazwisko_input)
        form_layout.addRow(QLabel("Turniej ID:"), self.turniej_input)

        add_button = self.create_button("Dodaj Zawodnika", self.save_player)

        layout.addLayout(form_layout)
        layout.addWidget(add_button)
        layout.setContentsMargins(40, 20, 40, 30)
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
        self.setGeometry(350, 200, 1200, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2691f7,
                    stop: 1 #e6f3ff
                );
            }
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 12px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #2691f7;
                color: white;
                padding: 6px;
                font-weight: bold;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📋 Lista Zawodników")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #0a0a0a; background: transparent;")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Imię", "Nazwisko", "Turniej ID", "Punkty", "✏️", "🗑️"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 12px;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)

        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 50)
        self.table.setColumnWidth(6, 50)

        buttons_layout = QHBoxLayout()
        refresh_button = self.create_button("🔄 Odśwież", self.load_players)
        save_button = self.create_button("💾 Zapisz punkty", self.save_points)
        random_button = self.create_button("Przelicz Punkty", self.points_operation)
        sort_asc_button = self.create_button("🔼 Rosnąco", lambda: self.sort_players_by_points(reverse=False))
        sort_desc_button = self.create_button("🔽 Malejąco", lambda: self.sort_players_by_points(reverse=True))

        details_button = self.create_button("🏆 Prezentacja", self.show_player_details)

        buttons_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(refresh_button)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(random_button)
        buttons_layout.addWidget(sort_asc_button)
        buttons_layout.addWidget(sort_desc_button)
        buttons_layout.addWidget(details_button)
        buttons_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.setLayout(layout)
        self.load_players()

    def create_button(self, text, action):
        button = QPushButton(text)
        button.setMinimumHeight(40 if text in ["✏️", "🗑️"] else 52)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 30))
        button.setGraphicsEffect(shadow)

        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.85);
                border: 1px solid #c0deff;
                border-radius: %s;
                padding: %s;
                font-size: %s;
                font-family: 'Segoe UI', sans-serif;
                color: #1a1a1a;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.95);
            }
            QPushButton:pressed {
                background-color: rgba(230, 244, 255, 0.95);
            }
        """ % (
            "12px" if text in ["✏️", "🗑️"] else "18px",
            "4px 8px" if text in ["✏️", "🗑️"] else "12px 24px",
            "16px" if text in ["✏️", "🗑️"] else "17px"
        ))

        button.clicked.connect(action)
        return button

    def load_players(self):
        zawodnicy = self.zawodnicy.show_zawodnicy()
        self.populate_table(zawodnicy)

    def populate_table(self, zawodnicy):
        self.table.setRowCount(0)
        for zawodnik in zawodnicy:
            id_, imie, nazwisko, turniej_id, punkty = zawodnik
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(id_)))
            self.table.setItem(row_position, 1, QTableWidgetItem(imie))
            self.table.setItem(row_position, 2, QTableWidgetItem(nazwisko))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(turniej_id)))

            punkty_item = QTableWidgetItem(str(punkty))
            punkty_item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.table.setItem(row_position, 4, punkty_item)

            edit_button = self.create_button("✏️", lambda _, row=row_position, id_=id_: self.edit_player(row, id_))
            delete_button = self.create_button("🗑️", lambda _, id_=id_: self.delete_player(id_))

            self.table.setCellWidget(row_position, 5, edit_button)
            self.table.setCellWidget(row_position, 6, delete_button)

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

    def points_operation(self):
        zawodnicy = self.zawodnicy.show_zawodnicy()
        point_data = self.zawodnicy.count_points(1)
        for zawodnik in zawodnicy:
            full_name = f"{zawodnik[1]} {zawodnik[2]}"
            points_counter = 0
            for point_data_row in point_data:
                    if full_name == point_data_row[0]:
                        points_counter += point_data_row[4]
                    elif full_name == point_data_row[1]:
                        points_counter += point_data_row[5]
                    elif full_name == point_data_row[2]:
                        points_counter += point_data_row[6]
                    elif full_name == point_data_row[3]:
                        points_counter += point_data_row[7]
            self.zawodnicy.update_punkty(zawodnik[0], points_counter)
        QMessageBox.information(self, "Sukces", "Punkty zostały przeliczone i zaktualizowane.")
        self.load_players()
    def delete_player(self, zawodnik_id):
        confirm = QMessageBox.question(self, "Potwierdzenie", "Czy na pewno chcesz usunąć tego zawodnika?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.zawodnicy.delete_zawodnik(zawodnik_id)
            self.load_players()

    def edit_player(self, row, zawodnik_id):
        imie_item = self.table.item(row, 1)
        nazwisko_item = self.table.item(row, 2)
        turniej_item = self.table.item(row, 3)

        imie = imie_item.text() if imie_item else ""
        nazwisko = nazwisko_item.text() if nazwisko_item else ""
        turniej_id = turniej_item.text() if turniej_item else ""

        try:
            turniej_id = int(turniej_id)
            self.zawodnicy.update_zawodnik(zawodnik_id, imie, nazwisko, turniej_id)
            QMessageBox.information(self, "Zaktualizowano", "Zawodnik został zaktualizowany.")
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Turniej ID musi być liczbą.")

    def sort_players_by_points(self, reverse=False):
        zawodnicy = self.zawodnicy.show_zawodnicy()
        zawodnicy.sort(key=lambda z: z[4], reverse=reverse)
        self.populate_table(zawodnicy)

    def show_player_details(self):
        sorted_players = sorted(self.zawodnicy.show_zawodnicy(), key=lambda x: x[4])  # Sortowanie od najmniejszej liczby punktów
        if sorted_players:
            rankings = self.get_player_rankings(sorted_players)
            self.display_player_details(sorted_players, rankings)
        else:
            QMessageBox.warning(self, "Brak Zawodników", "Nie ma żadnych zawodników w bazie danych.")

    def display_player_details(self, sorted_players, rankings):
        detail_window = PlayerDetailWindow(sorted_players, rankings)
        detail_window.exec_()

    def get_player_rankings(self, players):
        rankings = {player[0]: idx + 1 for idx, player in enumerate(players)}
        return rankings


class PlayerDetailWindow(QDialog):
    def __init__(self, sorted_players, rankings):
        super().__init__()
        self.sorted_players = sorted_players
        self.rankings = rankings
        self.current_index = 0  # Ustawiamy na pierwszy zawodnik, który będzie wyświetlany

        self.setWindowTitle("Szczegóły Zawodnika")
        self.setGeometry(400, 250, 400, 200)

        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2691f7,
                    stop: 1 #e6f3ff
                );
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #0a0a0a;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.details_label = QLabel(self.get_player_details())
        self.details_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.details_label)

        next_button = self.create_button("Następny", self.next_player)
        previous_button = self.create_button("Poprzedni", self.previous_player)

        button_layout = QHBoxLayout()
        button_layout.addWidget(previous_button)
        button_layout.addWidget(next_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_player_details(self):
        current_player = self.sorted_players[self.current_index]
        rank = self.rankings[current_player[0]]
        return f"{current_player[1]} {current_player[2]} - Punkty: {current_player[4]}, Miejsce: {rank}"

    def next_player(self):
        if self.current_index < len(self.sorted_players) - 1:
            self.current_index += 1
            self.details_label.setText(self.get_player_details())

    def previous_player(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.details_label.setText(self.get_player_details())

    def create_button(self, text, action):
        button = QPushButton(text)
        button.setMinimumHeight(40)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 30))
        button.setGraphicsEffect(shadow)

        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.85);
                border: 1px solid #c0deff;
                border-radius: 12px;
                padding: 8px 16px;
                font-size: 16px;
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


# Przykładowa implementacja klasy Zawodnicy
class Zawodnicy:
    def __init__(self):
        self.players = []

    def add_zawodnik(self, imie, nazwisko, turniej_id):
        id_ = len(self.players) + 1
        self.players.append([id_, imie, nazwisko, turniej_id, 0])

    def show_zawodnicy(self):
        return self.players

    def update_punkty(self, zawodnik_id, punkty):
        for player in self.players:
            if player[0] == zawodnik_id:
                player[4] = punkty

    def delete_zawodnik(self, zawodnik_id):
        self.players = [p for p in self.players if p[0] != zawodnik_id]

    def update_zawodnik(self, zawodnik_id, imie, nazwisko, turniej_id):
        for player in self.players:
            if player[0] == zawodnik_id:
                player[1] = imie
                player[2] = nazwisko
                player[3] = turniej_id


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    zawodnicy = Zawodnicy()
    main_window = ShowPlayersWindow(zawodnicy)
    main_window.show()

    sys.exit(app.exec_())