from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QFormLayout, QLineEdit
)
from PyQt5.QtCore import Qt
from Runda import Runda
from TablesWindow import TablesWindow

class RoundsWindow(QWidget):
    def __init__(self, id_):
        super().__init__()
        self.id_ = id_
        self.rounds = Runda(1,2,3)
        self.setWindowTitle("Rundy Turnieju")
        self.setGeometry(350, 200, 1200, 600)
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("RUNDY TURNIEJU ID: {}".format(self.id_))
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "ID turnieju", "Nazwa", "Liczba Stołów","Więcej", "Usuń"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("font-size: 14px;")
        
        layout.addWidget(title)
        layout.addWidget(self.table)
        buttons_layout = QHBoxLayout()
        refresh_button = QPushButton("🔄 Odśwież")
        save_round_button = QPushButton("+ Dodaj Rundę")

        for btn in [refresh_button, save_round_button]:
            btn.setStyleSheet("padding: 10px; font-weight: bold;")

        refresh_button.clicked.connect(self.load_rounds)
        save_round_button.clicked.connect(self.open_save_round)

        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(refresh_button)
        buttons_layout.addWidget(save_round_button)
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(buttons_layout)
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)
        self.load_rounds()

    def load_rounds(self):
        rounds = self.rounds.show_rounds(self.id_)
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
            table_button = QPushButton("Szczegóły")
            table_button.clicked.connect(lambda _, id_=id_: self.show_tables(id_))
            self.table.setCellWidget(row_counter, 4, table_button)
            delete_button = QPushButton("🗑️")
            delete_button.clicked.connect(lambda _, id_=id_: self.remove_round(id_))
            self.table.setCellWidget(row_counter, 5, delete_button)
            row_counter += 1

    def remove_round(self, id_):
        confirm = QMessageBox.question(self, "Potwierdzenie", "Czy na pewno chcesz usunąć tę rundę?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.rounds.delete_round(id_)
            self.load_rounds()
            
    def open_save_round(self):
        self.save_round_window = SaveRoundWindow()
        self.save_round_window.show()

    def show_tables(self, id_):
        self.id_ = id_
        self.tables_window = TablesWindow(id_)
        self.tables_window.show()


class SaveRoundWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dodaj Rundę")
        self.setGeometry(450, 300, 350, 200)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.tournament_id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.tables_input = QLineEdit()
        self.liczba_rund_input = QLineEdit()

        layout.addRow(QLabel("ID Turnieju:"), self.tournament_id_input)
        layout.addRow(QLabel("Nazwa:"), self.name_input)
        layout.addRow(QLabel("Liczba Stołów:"), self.tables_input)

        add_button = QPushButton("Dodaj")
        add_button.clicked.connect(self.save_round)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def save_round(self):
        tournament_id = self.tournament_id_input.text()
        name = self.name_input.text()
        tables = self.tables_input.text()

        try:
            tables = int(tables)
            tournament_id = int(tournament_id)

            round = Runda(tournament_id, name, tables)
            round.add_round(round.tournament_id, round.name, round.tables,)

            QMessageBox.information(self, "Sukces", "Runda dodana pomyślnie!(Okno rund pokazuje tylko rundy z ID wybranego turnieju)")
            self.tournament_id_input.clear()
            self.name_input.clear()
            self.tables_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Podaj poprawne dane.")