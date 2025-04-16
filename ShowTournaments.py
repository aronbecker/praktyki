from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpacerItem,
    QSizePolicy
)
from PyQt5.QtCore import Qt
from Runda import Runda
from RoundsWindow import RoundsWindow

class ShowTournamentsWindow(QWidget):
    def __init__(self, turnieje):
        super().__init__()
        self.turnieje = turnieje
        self.setWindowTitle("Lista Turnieji")
        self.setGeometry(350, 200, 1200, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📋 Lista Turnieji")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Nazwa", "Data", "Liczba Stołów", "Liczba Rund", "Więcej", "✏️ Edytuj", "🗑️ Usuń"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("font-size: 14px;")

        buttons_layout = QHBoxLayout()
        refresh_button = QPushButton("🔄 Odśwież")
        refresh_button.clicked.connect(self.load_tournaments)

        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(refresh_button)
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)
        layout.setContentsMargins(30, 30, 30, 30)

        self.setLayout(layout)
        self.load_tournaments()

    def load_tournaments(self):
        self.table.setRowCount(0)
        self.turnieje.update_round_counter()
        turnieje = self.turnieje.show_tournament()
        turnieje.sort(key=lambda z: z[4])  # sort by rounds

        row_counter = 0
        for turniej in turnieje:
            id_, name, date, tables, rounds = turniej
            self.table.insertRow(row_counter)
            self.table.setItem(row_counter, 0, QTableWidgetItem(str(id_)))
            self.table.setItem(row_counter, 1, QTableWidgetItem(name))
            self.table.setItem(row_counter, 2, QTableWidgetItem(date))
            self.table.setItem(row_counter, 3, QTableWidgetItem(str(tables)))
            self.table.setItem(row_counter, 4, QTableWidgetItem(str(rounds)))

            details_button = QPushButton("Szczegóły")
            details_button.clicked.connect(lambda _, id_=id_: self.show_details(id_))
            self.table.setCellWidget(row_counter, 5, details_button)

            edit_button = QPushButton("✏️")
            edit_button.clicked.connect(lambda _, row=row_counter, id_=id_: self.edit_tournament(row, id_))
            self.table.setCellWidget(row_counter, 6, edit_button)

            delete_button = QPushButton("🗑️")
            delete_button.clicked.connect(lambda _, id_=id_: self.remove_tournament(id_))
            self.table.setCellWidget(row_counter, 7, delete_button)

            row_counter += 1

    def remove_tournament(self, id_):
        confirm = QMessageBox.question(self, "Potwierdzenie", "Czy na pewno chcesz usunąć ten turniej?", QMessageBox.Yes | QMessageBox.No)
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
            QMessageBox.information(self, "Zaktualizowano", "Turniej został zaktualizowany.")
        except ValueError:
            QMessageBox.warning(self, "Błąd", "ID oraz liczba stołów muszą być liczbami.")
    
    def show_details(self, id_):
        self.id_ = id_
        self.rounds_window = RoundsWindow(id_)
        self.rounds_window.show()