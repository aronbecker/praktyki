from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
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
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "ID Rundy", "Nazwa", "Gracz 1", "Gracz 2", "Gracz 3", "Gracz 4"])
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
        refresh_button = self.create_button("🔄 Odśwież",self.load_tables)
        randomize_button = self.create_button("🎲 Losuj Zawodników",self.randomize_players)

        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
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