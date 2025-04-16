from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from Table import Table  # Upewnij się, że masz poprawnie zdefiniowaną klasę Table
import sqlite3
import random

class TablesWindow(QWidget):
    def __init__(self, id_, tables):
        super().__init__()
        self.id_ = id_
        self.tables = tables
        self.setWindowTitle("Stoły Rundy")
        self.setGeometry(350, 200, 1200, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel(f"Stoły Rundy ID: {self.id_}")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "ID Rundy", "Nazwa", "Gracz 1", "Gracz 2", "Gracz 3", "Gracz 4"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("font-size: 14px;")

        layout.addWidget(title)
        layout.addWidget(self.table)

        buttons_layout = QHBoxLayout()
        refresh_button = QPushButton("🔄 Odśwież")
        randomize_button = QPushButton("🎲 Losuj Zawodników")

        for btn in [refresh_button, randomize_button]:
            btn.setStyleSheet("padding: 10px; font-weight: bold;")

        refresh_button.clicked.connect(self.load_tables)
        randomize_button.clicked.connect(self.randomize_players)

        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(refresh_button)
        buttons_layout.addWidget(randomize_button)
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(buttons_layout)
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)

        self.load_tables()

    def load_tables(self):
        connection = sqlite3.connect("turniej_db.sqlite")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tables WHERE runda_id = ?", (self.id_,))
        rows = cursor.fetchall()

        if not rows:
            for i in range(self.tables):
                table = Table(self.id_, f"Stolik {i + 1}", "brak", "brak", "brak", "brak")
                table.add_table()

            cursor.execute("SELECT * FROM tables WHERE runda_id = ?", (self.id_,))
            rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        connection.close()

    def randomize_players(self):
        connection = sqlite3.connect("turniej_db.sqlite")
        cursor = connection.cursor()

        # Pobierz zawodników
        cursor.execute("SELECT id, imie, nazwisko FROM zawodnicy")
        players = cursor.fetchall()
        player_data = {row[0]: f"{row[1]} {row[2]}" for row in players}
        player_ids = list(player_data.keys())
        random.shuffle(player_ids)

        # Pobierz ID stołów
        cursor.execute("SELECT id FROM tables WHERE runda_id = ?", (self.id_,))
        table_ids = [row[0] for row in cursor.fetchall()]

        # Przydziel zawodników do stołów
        table_data = {table_id: [] for table_id in table_ids}
        for i, player_id in enumerate(player_ids):
            table_id = table_ids[i % len(table_ids)]
            table_data[table_id].append(player_data[player_id])

        # Zaktualizuj stoły
        for table_id, players in table_data.items():
            player_columns = ["player_1", "player_2", "player_3", "player_4"]
            
            # Ogranicz do maksymalnie 4 graczy, dodaj "brak" w razie potrzeby
            if len(players) > 4:
                players = players[:4]
            update_values = players + ["brak"] * (4 - len(players))  # Ensure exactly 4 players

            # Debug info
            print(f"Updating table {table_id} with players: {update_values}")
            print(f"Total bindings: {len(update_values) + 1}")  # Expect 5 bindings

            sql = f"""
                UPDATE tables
                SET {', '.join(f"{col} = ?" for col in player_columns)}
                WHERE id = ?
            """
            
            cursor.execute(sql, update_values + [table_id])  # Append table_id correctly

        connection.commit()
        connection.close()

        self.load_tables()