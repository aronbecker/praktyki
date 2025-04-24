from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QFormLayout, QLineEdit, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from Runda import Runda
from Turniej import Turniej
from TablesWindow import TablesWindow
from Table import Table

class RoundsWindow(QWidget):
    def __init__(self, tournaments_id):
        super().__init__()
        self.tournaments_id = tournaments_id
        self.rounds = Runda(1,2,3)
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
        refresh_button = self.create_button("🔄",self.load_rounds)
        save_round_button = self.create_button("+ Dodaj Rundę",self.open_save_round)
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
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