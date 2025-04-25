from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpacerItem,
    QSizePolicy, QGraphicsDropShadowEffect, QFormLayout, QLineEdit
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from Runda import Runda
from Turniej import Turniej
from Table import Table
import sqlite3
import random
from SetPointsWindow import SetPointsWindow


class ShowTournamentsWindow(QWidget):
    def __init__(self, turnieje):
        super().__init__()
        self.turnieje = turnieje
        self.setWindowTitle("Lista Turnieji")
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

        title = QLabel("📋 Lista Turnieji")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #0a0a0a; background: transparent;")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Nazwa", "Data", "Liczba Stołów", "Liczba Rund", "Więcej", "✏️ Edytuj", "🗑️ Usuń"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setDefaultSectionSize(80)
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


        buttons_layout = QHBoxLayout()
        refresh_button = self.create_button("🔄 Odśwież", self.load_tournaments)

        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(refresh_button)
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)
        layout.setContentsMargins(30, 30, 30, 30)

        self.setLayout(layout)
        self.load_tournaments()
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

    def load_tournaments(self):
        self.table.setRowCount(0)
        turnieje = self.turnieje.update_round_counter()
        turnieje = self.turnieje.show_tournament()
        turnieje.sort(key=lambda z: z[3])


        row_counter = 0
        for turniej in turnieje:
            id_, name, date, tables, rounds = turniej

            self.table.insertRow(row_counter)
            self.table.setItem(row_counter, 0, QTableWidgetItem(str(id_)))
            self.table.setItem(row_counter, 1, QTableWidgetItem(name))
            self.table.setItem(row_counter, 2, QTableWidgetItem(date))
            self.table.setItem(row_counter, 3, QTableWidgetItem(str(tables)))

            rounds_item = QTableWidgetItem(str(rounds))
            rounds_item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row_counter, 4, rounds_item)
            # Przyciski do wyświetlania okna rund, przekazuje id turnieju, które jest niezbędne do wyświetlenie rund przypisanych do tego turnieju
            details_button = self.create_button("Rundy",lambda _, id_=id_: self.show_details(id_))
            self.table.setCellWidget(row_counter, 5, details_button)

            # Przyciski edytuj/usuń
            edit_button = self.create_button("✏️",lambda _, row=row_counter, id_=id_: self.edit_tournament(row, id_))
            self.table.setCellWidget(row_counter, 6, edit_button)

            delete_button = self.create_button("🗑️",lambda _, id_=id_: self.remove_tournament(id_))
            self.table.setCellWidget(row_counter, 7, delete_button)

            row_counter += 1

    def remove_tournament(self, id_):
        confirm = QMessageBox.question(self, "Potwierdzenie", "Czy na pewno chcesz usunąć ten turniej?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.turnieje.delete_tournament(id_)
            self.load_tournaments()

    def edit_tournament(self, row, id_):
        name_item = self.table.item(row, 1)
        date_item = self.table.item(row, 2)
        tables_item = self.table.item(row, 3)

        name = name_item.text() if name_item else ""
        date = date_item.text() if date_item else ""
        tables = tables_item.text() if tables_item else ""

        try:
            tables = int(tables) if tables else 0
            self.turnieje.update_tournament(id_, name, date, tables)
            QMessageBox.information(self, "Zaktualizowano", "turniej został zaktualizowany.")
        except ValueError:
            QMessageBox.warning(self, "Błąd", "ID, liczba stołów muszą być liczbami.")
    def show_details(self, id_):
        self.id_ = id_
        self.rounds_window = RoundsWindow(id_)
        self.rounds_window.show()
        self.close()




class RoundsWindow(QWidget):
    def __init__(self, tournaments_id):
        super().__init__()
        self.tournaments_id = tournaments_id
        self.rounds = Runda(1,2,3)
        self.turnieje = Turniej(1,2,3)
        self.setWindowTitle("Rundy Turnieju")
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

        title = QLabel("RUNDY TURNIEJU ID: {}".format(self.tournaments_id))
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #0a0a0a; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "ID turnieju", "Nazwa", "Liczba Stołów","Więcej", "Usuń"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setDefaultSectionSize(80)
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

        
        layout.addWidget(title)
        layout.addWidget(self.table)
        buttons_layout = QHBoxLayout()
        back_button = self.create_button("⬅️ Powrót",self.go_back)
        refresh_button = self.create_button("🔄",self.load_rounds)
        save_round_button = self.create_button("+ Dodaj Rundę",self.open_save_round)
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(back_button)
        buttons_layout.addWidget(refresh_button)
        buttons_layout.addWidget(save_round_button)
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(buttons_layout)
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)
        self.load_rounds()

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

    def go_back(self):
        self.show_tournaments_window = ShowTournamentsWindow(self.turnieje)
        self.show_tournaments_window.show()
        self.close()

    def load_rounds(self):
        rounds = self.rounds.show_rounds(self.tournaments_id)
        self.populate_table(rounds)

    def populate_table(self, rounds):
        self.table.setRowCount(0)
        row_counter = 0
        for round in rounds:
            id_, tournament_id, name, tables = round
            self.table.insertRow(row_counter)
            self.table.setItem(row_counter, 0, QTableWidgetItem(str(id_)))
            self.table.setItem(row_counter, 1, QTableWidgetItem(str(tournament_id)))
            self.table.setItem(row_counter, 2, QTableWidgetItem(name))
            self.table.setItem(row_counter, 3, QTableWidgetItem(str(tables)))
            # Przycisk do wyświetlenia okna stołów, przekazuje id rundy, i liczbę stołów do niej przypisane, które są niezbędne do wyświetlenia tego okna
            table_button = self.create_button("Stoły",lambda _, round_id=id_, tables=tables: self.show_tables(round_id,tables))
            self.table.setCellWidget(row_counter, 4, table_button)
            delete_button = self.create_button("🗑️",lambda _, id_=id_: self.remove_round(id_))
            self.table.setCellWidget(row_counter, 5, delete_button)
            row_counter += 1

    def remove_round(self, id_):
        confirm = QMessageBox.question(self, "Potwierdzenie", "Czy na pewno chcesz usunąć tę rundę?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.rounds.delete_round(id_)
            Table.delete_tables(id_)
            self.load_rounds()

    def open_save_round(self):
        self.save_round_window = SaveRoundWindow(self.tournaments_id)
        self.save_round_window.show()

    def show_tables(self, round_id, tables):
        self.round_id = round_id
        self.tables = tables
        self.tables_window = TablesWindow(round_id,tables)
        self.tables_window.show()
        self.close()


class SaveRoundWindow(QWidget):
    def __init__(self, tournaments_id):

        super().__init__()
        self.tournament_id = tournaments_id
        self.setWindowTitle("Dodaj Rundę")
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
        title = QLabel("➕ Dodaj Rundę")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0a0a0a; background: transparent;")
        layout.addWidget(title)
        self.name_input = QLineEdit()
        self.tables_input = QLineEdit()
        self.liczba_rund_input = QLineEdit()

        layout.addRow(QLabel("Nazwa:"), self.name_input)
        layout.addRow(QLabel("Liczba Stołów:"), self.tables_input)

        add_button = self.create_button(("Dodaj"),lambda: self.save_round(self.tournament_id))
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

    def save_round(self, tournaments_id):
        self.tournament_id = tournaments_id
        tournament_id = self.tournament_id
        name = self.name_input.text()
        tables = self.tables_input.text()

        try:
            tables = int(tables)

            round = Runda(tournament_id, name, tables)
            round.add_round(round.tournament_id, round.name, round.tables,)

            QMessageBox.information(self, "Sukces", "Runda dodana pomyślnie do obecnego turnieju!")
            self.name_input.clear()
            self.tables_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Podaj poprawne dane.")





class TablesWindow(QWidget):
    def __init__(self, id_, tables):
        super().__init__()
        self.id_ = id_
        self.tables = tables
        self.setWindowTitle("Stoły Rundy")
        self.setGeometry(350, 200, 1200, 600)
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
        layout = QVBoxLayout()

        title = QLabel(f"Stoły Rundy ID: {self.id_}")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #0a0a0a; background: transparent;")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Nazwa", "Gracz 1", "Gracz 2", "Gracz 3", "Gracz 4",
            "Punkty 1", "Punkty 2", "Punkty 3", "Punkty 4", "Ustaw"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("font-size: 14px;")
        self.table.verticalHeader().setDefaultSectionSize(80)
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

        layout.addWidget(title)
        layout.addWidget(self.table)

        buttons_layout = QHBoxLayout()
        back_button = self.create_button("⬅️ Powrót", self.go_back)
        refresh_button = self.create_button("🔄 Odśwież", self.load_tables)
        randomize_button = self.create_button("🎲 Losuj Zawodników", self.randomize_players)

        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(back_button)
        buttons_layout.addWidget(refresh_button)
        buttons_layout.addWidget(randomize_button)
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(buttons_layout)
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)

        self.load_tables()

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
    
    def go_back(self):
        connection = sqlite3.connect("turniej_db.sqlite")
        cursor = connection.cursor()

        cursor.execute("SELECT tournament_id FROM rounds WHERE id = ?", (self.id_,))
        tournament_id = cursor.fetchone()[0]
        connection.close()
        self.tournaments_id = tournament_id
        self.rounds = Runda(1,2,3)
        self.rounds_window = RoundsWindow(tournament_id)
        self.rounds_window.show()
        self.close()
    
    def load_tables(self):
        connection = sqlite3.connect("turniej_db.sqlite")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name, player_1, player_2, player_3, player_4,
                   punkty_1, punkty_2, punkty_3, punkty_4
            FROM tables
            WHERE runda_id = ?
        """, (self.id_,))
        rows = cursor.fetchall()

        if not rows:
            for i in range(self.tables):
                table = Table(self.id_, f"Stolik {i + 1}", "brak", "brak", "brak", "brak")
                table.add_table()
            cursor.execute("""
                SELECT name, player_1, player_2, player_3, player_4,
                       punkty_1, punkty_2, punkty_3, punkty_4
                FROM tables
                WHERE runda_id = ?
            """, (self.id_,))
            rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            button = self.create_button("Punkty", lambda _, row=row_idx: self.show_points(row))
            self.table.setCellWidget(row_idx, 9, button)

        connection.close()

    def randomize_players(self):
        connection = sqlite3.connect("turniej_db.sqlite")
        cursor = connection.cursor()

        cursor.execute("SELECT id, imie, nazwisko FROM zawodnicy")
        players = cursor.fetchall()
        player_data = {row[0]: f"{row[1]} {row[2]}" for row in players}
        player_ids = list(player_data.keys())
        random.shuffle(player_ids)

        cursor.execute("SELECT id FROM tables WHERE runda_id = ?", (self.id_,))
        table_ids = [row[0] for row in cursor.fetchall()]

        table_data = {table_id: [] for table_id in table_ids}
        for i, player_id in enumerate(player_ids):
            table_id = table_ids[i % len(table_ids)]
            table_data[table_id].append(player_data[player_id])

        for table_id, players in table_data.items():
            player_columns = ["player_1", "player_2", "player_3", "player_4"]
            update_values = players[:4] + ["brak"] * (4 - len(players))
            sql = f"""
                UPDATE tables
                SET {', '.join(f"{col} = ?" for col in player_columns)}
                WHERE id = ?
            """
            cursor.execute(sql, update_values + [table_id])

        connection.commit()
        connection.close()
        for table_id in table_data:
            Table.set_points(self, table_id, 0, 0, 0, 0)
        self.load_tables()

    def show_points(self, row):
        table_name = self.table.item(row, 0).text()
        player_1 = self.table.item(row, 1).text()
        player_2 = self.table.item(row, 2).text()
        player_3 = self.table.item(row, 3).text()
        player_4 = self.table.item(row, 4).text()
        punkty_1 = int(self.table.item(row, 5).text())
        punkty_2 = int(self.table.item(row, 6).text())
        punkty_3 = int(self.table.item(row, 7).text())
        punkty_4 = int(self.table.item(row, 8).text())

        connection = sqlite3.connect("turniej_db.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM tables WHERE name = ? AND runda_id = ?", (table_name, self.id_))
        table_id = cursor.fetchone()[0]
        connection.close()

        self.points_window = SetPointsWindow(
            table_id, player_1, player_2, player_3, player_4,
            punkty_1, punkty_2, punkty_3, punkty_4
        )
        self.points_window.show()
