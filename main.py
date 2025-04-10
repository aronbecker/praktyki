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
                background-color: #f9f9f9;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 16px;
                padding: 12px;
                font-size: 16px;
                color: #333;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setSpacing(20)

        title = QLabel("🃏 Menadżer Turniejów")
        title.setFont(QFont("Helvetica Neue", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Przycisk z cieniem
        def create_button(text, action):
            button = QPushButton(text)
            button.setMinimumHeight(50)

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(0, 4)
            shadow.setColor(QColor(0, 0, 0, 50))
            button.setGraphicsEffect(shadow)

            button.clicked.connect(action)
            layout.addWidget(button)
            return button

        # Przyciskowe akcje
        create_button("➕ Dodaj Turniej", self.add_tournament)
        create_button("📅 Wyświetl Turnieje", self.show_tournaments)
        create_button("👤 Dodaj Zawodnika", self.open_add_player)
        create_button("📋 Wyświetl Zawodników", self.open_show_players)

        self.setLayout(layout)
        self.setMinimumSize(700, 500)
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
