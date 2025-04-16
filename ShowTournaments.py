from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpacerItem,
    QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from Runda import Runda
from RoundsWindow import RoundsWindow


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