import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

class TournamentManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Przyciski
        add_tournament_button = QPushButton("Dodaj Turniej", self)
        show_tournaments_button = QPushButton("Wyświetl Turnieje", self)
        #nie wiem
        # Układ
        layout = QVBoxLayout()
        layout.addWidget(add_tournament_button)
        layout.addWidget(show_tournaments_button)
        self.setLayout(layout)

        # Podłączenie funkcji do przycisków
        add_tournament_button.clicked.connect(self.add_tournament)
        show_tournaments_button.clicked.connect(self.show_tournaments)

        # Ustawienia okna
        #komentarz
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Menadżer Turniejów")
        self.show()


    def add_tournament(self):
        # Tutaj będzie kod dodający turniej
        QMessageBox.information(self, "Dodaj Turniej", "Funkcja dodawania turnieju")

    def show_tournaments(self):
        # Tutaj będzie kod wyświetlający listę turniejów
        QMessageBox.information(self, "Wyświetl Turnieje", "Funkcja wyświetlania turniejów")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TournamentManager()
    sys.exit(app.exec_())