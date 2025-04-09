# Removed unused import
import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from Turniej import Turniej

class EditTournamentWindow(QWidget):
    def __init__(self, turniej, parent=None):
        super().__init__(parent)
        self.turniej = turniej
        self.setWindowTitle("Edytuj Turniej")
        self.setGeometry(450, 300, 350, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nazwa_input = QLineEdit(self.turniej.name)
        self.data_input = QLineEdit(self.turniej.date)
        self.liczba_stolow_input = QLineEdit(str(self.turniej.tables))
        self.liczba_rund_input = QLineEdit(str(self.turniej.rounds))

        layout.addWidget(QLabel("Nazwa:"))
        layout.addWidget(self.nazwa_input)
        layout.addWidget(QLabel("Data:"))
        layout.addWidget(self.data_input)
        layout.addWidget(QLabel("Liczba Stołów:"))
        layout.addWidget(self.liczba_stolow_input)
        layout.addWidget(QLabel("Liczba Rund:"))
        layout.addWidget(self.liczba_rund_input)

        save_button = QPushButton("Zapisz")
        save_button.clicked.connect(self.save_tournament)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_tournament(self):
        new_name = self.nazwa_input.text()
        new_date = self.data_input.text()
        new_tables = int(self.liczba_stolow_input.text())
        new_rounds = int(self.liczba_rund_input.text())

        self.turniej.update(new_name, new_date, new_tables, new_rounds)
        QMessageBox.information(self, "Sukces", "Turniej zaktualizowany pomyślnie!")
        self.close()
class ShowTournamentsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista Turniejów")
        self.setGeometry(1000, 600, 820, 700)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Nazwa", "Data", "Liczba Stołów", "Liczba Rund"])
        layout.addWidget(self.table_widget)
        layout.addWidget(QPushButton("Usuń", clicked=self.delete_tournament))
        layout.addWidget(QPushButton("Edytuj", clicked=self.edit_tournament))
        layout.addWidget(QPushButton("Odśwież", clicked=self.load_tournaments))
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
    def delete_tournament(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            tournament_name = self.table_widget.item(selected_row, 0).text()
            turniej = Turniej(tournament_name, "", 0, 0)
            turniej.delete()
            QMessageBox.information(self, "Sukces", "Turniej usunięty pomyślnie!")
            self.load_tournaments()
        else:
            QMessageBox.warning(self, "Błąd", "Wybierz turniej do usunięcia.")
    def edit_tournament(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            tournament_name = self.table_widget.item(selected_row, 0).text()
            turniej = Turniej(tournament_name, "", 0, 0)
            self.edit_window = EditTournamentWindow(turniej, self)
            self.edit_window.show()
        else:
            QMessageBox.warning(self, "Błąd", "Wybierz turniej do edytowania.")