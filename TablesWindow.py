from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QFormLayout, QLineEdit, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from Table import Table
import sqlite3
import random

class TablesWindow(QWidget):
    def __init__(self, id_,tables):
        super().__init__()
        self.id_ = id_
        self.tables = tables
        table_count = tables
        self.setWindowTitle("Stoły Rundy")
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

        title = QLabel("Stoły Rundy ID: {}".format(self.id_))
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #0a0a0a; background: transparent;")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "ID Rundy", "Nazwa", "Gracz 1","Gracz 2","Gracz 3","Gracz 4"])
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

    def load_tables(self):
        connection = sqlite3.connect("tysiac.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tables WHERE runda_id = ?", (self.id_,))
        rows = cursor.fetchall()

        if not rows:
            for i in range(self.tables):
                Table.add_table(1, self.id_, f"Stolik {i + 1}", "brak", "brak", "brak", "brak")
            cursor.execute("SELECT * FROM tables WHERE runda_id = ?", (self.id_,))
            rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        connection.close()
    def randomize_players(self):
        connection = sqlite3.connect("turniejedb.sqlite3")
        cursor = connection.cursor()

        # Fetch all player IDs and their names
        cursor.execute("SELECT id, imie, nazwisko FROM zawodnicy")
        players = cursor.fetchall()
        player_data = {row[0]: f"{row[1]} {row[2]}" for row in players}
        player_ids = list(player_data.keys())
        connection.close()
        random.shuffle(player_ids)

        # Calculate the total number of spots at the tables
        total_spots = self.tables * 4
        num_players = len(player_ids)

        # Determine the grouping rule
        if num_players > total_spots:
            group_size = 4
        else:
            group_size = 3

        # Fetch all table IDs for the current round
        connection = sqlite3.connect("tysiac.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM tables WHERE runda_id = ?", (self.id_,))
        table_ids = [row[0] for row in cursor.fetchall()]

        # Assign players to tables
        table_data = {table_id: [] for table_id in table_ids}
        player_index = 0

        # Assign players to tables based on the group size
        for table_id in table_ids:
            if player_index + group_size <= num_players:
                table_data[table_id] = player_ids[player_index:player_index + group_size]
                player_index += group_size

        # Distribute any remaining players to the tables
        remainder = num_players - player_index
        if remainder > 0:
            for i in range(remainder):
                table_id = table_ids[i % len(table_ids)]
                table_data[table_id].append(player_ids[player_index])
                player_index += 1

        # Ensure remaining players fill the fourth spot if group size is 3
        for table_id, players in table_data.items():
            if len(players) == 3 and player_index < num_players:
                players.append(player_ids[player_index])
                player_index += 1

        # Update tables in the database
        for table_id, players in table_data.items():
            player_columns = ["player_1", "player_2", "player_3", "player_4"]
            update_values = [player_data.get(player_id, "brak") for player_id in players] + ["brak"] * (4 - len(players))
            update_values = update_values[:4]  # Ensure exactly 4 player values
            cursor.execute(f"""
            UPDATE tables
            SET {', '.join(f"{col} = ?" for col in player_columns)}
            WHERE id = ?
            """, (*update_values, table_id))

        connection.commit()
        connection.close()

        # Reload the table view
        self.load_tables()