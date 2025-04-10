import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QMessageBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from zawodnicy import Zawodnicy
from zawodnicy_gui import AddPlayerWindow, ShowPlayersWindow
from AddTournament import AddTournamentWindow
from ShowTournaments import ShowTournamentsWindow
from Turniej import Turniej

class TournamentManager(QWidget):
    def __init__(self):
        super().__init__()
        self.turnieje = Turniej(1, 2, 3, 4)
        self.zawodnicy = Zawodnicy()
        self.zawodnicy.create_table()
        self.setFocusPolicy(Qt.StrongFocus)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Menadżer Turniejów")
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2691f7,
                    stop: 1 #e6f3ff
                );
            }
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

        layout = QVBoxLayout()
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setSpacing(24)

        title = QLabel("🎯 Menadżer Turniejów")
        title.setFont(QFont("Segoe UI", 30, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0a0a0a; background: transparent;")
        layout.addWidget(title)

        def create_button(text, action):
            button = QPushButton(text)
            button.setMinimumHeight(52)

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setOffset(0, 4)
            shadow.setColor(QColor(0, 0, 0, 40))
            button.setGraphicsEffect(shadow)

            button.clicked.connect(action)
            layout.addWidget(button)
            return button

        create_button("➕ Dodaj nowy turniej", self.add_tournament)
        create_button("📆 Lista turniejów", self.show_tournaments)
        create_button("🧍 Dodaj zawodnika", self.open_add_player)
        create_button("📑 Lista zawodników", self.open_show_players)

        self.setLayout(layout)
        self.setMinimumSize(720, 520)
        self.setFocus()

    def add_tournament(self):
        self.add_tournament_window = AddTournamentWindow()
        self.add_tournament_window.show()

    def show_tournaments(self):
        self.show_tournaments_window = ShowTournamentsWindow(self.turnieje)
        self.show_tournaments_window.show()

    def open_add_player(self):
        self.add_player_window = AddPlayerWindow(self.zawodnicy)
        self.add_player_window.show()

    def open_show_players(self):
        self.show_players_window = ShowPlayersWindow(self.zawodnicy)
        self.show_players_window.show()

    def close_application(self):
        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz zamknąć aplikację?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_application()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = TournamentManager()
    window.show()
    sys.exit(app.exec_())
