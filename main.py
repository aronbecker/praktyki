import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QMessageBox,
    QLineEdit, QFormLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from zawodnicy import Zawodnicy
from zawodnicy_gui import AddPlayerWindow, ShowPlayersWindow
from AddTournament import AddTournamentWindow
from ShowTournaments import ShowTournamentsWindow
from Turniej import Turniej

class TournamentManager(QWidget):
    def __init__(self):
        super().__init__()
        self.turnieje = Turniej(1,2,3,4)
        self.zawodnicy = Zawodnicy()
        self.zawodnicy.create_table()
        self.setFocusPolicy(Qt.StrongFocus)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        add_tournament_button = QPushButton("Dodaj Turniej", self)
        show_tournaments_button = QPushButton("Wyświetl Turnieje", self)
        add_player_button = QPushButton("Dodaj Zawodnika", self)
        show_players_button = QPushButton("Wyświetl Zawodników", self)
       

        add_tournament_button.clicked.connect(self.add_tournament)
        show_tournaments_button.clicked.connect(self.show_tournaments)
        add_player_button.clicked.connect(self.open_add_player)
        show_players_button.clicked.connect(self.open_show_players)
        

        layout.addWidget(add_tournament_button)
        layout.addWidget(show_tournaments_button)
        layout.addWidget(add_player_button)
        layout.addWidget(show_players_button)
      

        self.setLayout(layout)
        self.setWindowTitle("Menadżer Turniejów")
        self.showMaximized()  
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
    window = TournamentManager()
    sys.exit(app.exec_())
