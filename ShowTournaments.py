import sys
import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt
from Turniej import Turniej

class ShowTournamentsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista Turniejów")
        self.setGeometry(600, 600, 547, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Nazwa", "Data", "Liczba Stołów", "Liczba Rund"])
        layout.addWidget(self.table_widget)

        self.load_tournaments()

        self.setLayout(layout)

    def load_tournaments(self):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tournaments")
        tournaments = cursor.fetchall()
        conn.close()

        self.table_widget.setRowCount(len(tournaments))

        for row_index, tournament in enumerate(tournaments):
            for column_index, data in enumerate(tournament[1:]):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row_index, column_index, item)