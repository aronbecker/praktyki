import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, QFormLayout, QLabel

class Zawodnicy:
    def __init__(self, host="127.0.0.1", user="root", password="", db_name="turniejedb"):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name

    def connect(self):
        """Nawiązanie połączenia z bazą danych MySQL."""
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )

    def create_table(self):
        """Tworzenie tabeli Zawodnicy w bazie danych, jeśli jeszcze nie istnieje."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS zawodnicy (
                id INT AUTO_INCREMENT PRIMARY KEY,
                imie VARCHAR(100) NOT NULL,
                nazwisko VARCHAR(100) NOT NULL,
                turniej_id INT,
                FOREIGN KEY (turniej_id) REFERENCES turnieje(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        conn.close()

    def add_zawodnik(self, imie, nazwisko, turniej_id):
        """Dodawanie zawodnika do tabeli Zawodnicy."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO zawodnicy (imie, nazwisko, turniej_id)
            VALUES (%s, %s, %s)
        ''', (imie, nazwisko, turniej_id))
        conn.commit()
        conn.close()

    def show_zawodnicy(self):
        """Wyświetlanie wszystkich zawodników w tabeli."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM zawodnicy')
        zawodnicy = cursor.fetchall()
        conn.close()
        return zawodnicy

class TournamentManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.zawodnicy = Zawodnicy()  # Utworzenie instancji klasy Zawodnicy
        self.zawodnicy.create_table()  # Tworzenie tabeli, jeśli nie istnieje

    def initUI(self):
        # Przyciski
        add_tournament_button = QPushButton("Dodaj Turniej", self)
        show_tournaments_button = QPushButton("Wyświetl Turnieje", self)
        add_player_button = QPushButton("Dodaj Zawodnika", self)
        show_players_button = QPushButton("Wyświetl Zawodników", self)
        
        # Układ
        layout = QVBoxLayout()
        layout.addWidget(add_tournament_button)
        layout.addWidget(show_tournaments_button)
        layout.addWidget(add_player_button)
        layout.addWidget(show_players_button)
        self.setLayout(layout)

        # Podłączenie funkcji do przycisków
        add_tournament_button.clicked.connect(self.add_tournament)
        show_tournaments_button.clicked.connect(self.show_tournaments)
        add_player_button.clicked.connect(self.add_player)
        show_players_button.clicked.connect(self.show_players)

        # Ustawienia okna
        self.setGeometry(300, 300, 300, 250)
        self.setWindowTitle("Menadżer Turniejów")
        self.show()


    def add_tournament(self):
        # Funkcja dodająca turniej
        QMessageBox.information(self, "Dodaj Turniej", "Funkcja dodawania turnieju")

    def show_tournaments(self):
        # Funkcja wyświetlająca turnieje
        QMessageBox.information(self, "Wyświetl Turnieje", "Funkcja wyświetlania turniejów")

    def add_player(self):
        """Dodawanie zawodnika do bazy danych."""
        dialog = QWidget(self)
        dialog.setWindowTitle("Dodaj Zawodnika")
        dialog.setGeometry(400, 400, 250, 150)
        
        # Form for adding player
        layout = QFormLayout()
        imie_input = QLineEdit(dialog)
        nazwisko_input = QLineEdit(dialog)
        turniej_input = QLineEdit(dialog)  # Nowe pole na turniej_id
        
        layout.addRow(QLabel("Imię:"), imie_input)
        layout.addRow(QLabel("Nazwisko:"), nazwisko_input)
        layout.addRow(QLabel("Turniej ID:"), turniej_input)  # Dodanie pola na ID turnieju
        
        add_button = QPushButton("Dodaj", dialog)
        layout.addWidget(add_button)
        
        add_button.clicked.connect(lambda: self.save_player(imie_input.text(), nazwisko_input.text(), turniej_input.text(), dialog))
        
        dialog.setLayout(layout)
        dialog.show()

    def save_player(self, imie, nazwisko, turniej_id, dialog):
        """Zapisanie danych zawodnika do bazy i zamknięcie okna."""
        try:
            turniej_id = int(turniej_id)  # Próbujemy konwertować turniej_id na liczbę
            self.zawodnicy.add_zawodnik(imie, nazwisko, turniej_id)
            QMessageBox.information(self, "Sukces", "Zawodnik dodany pomyślnie!")
            dialog.close()  # Zamknięcie okna
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Proszę podać prawidłowe id turnieju.")

    def show_players(self):
        """Wyświetlanie zawodników z bazy danych."""
        zawodnicy = self.zawodnicy.show_zawodnicy()
        if zawodnicy:
            player_list = "\n".join([f"{zawodnik[1]} {zawodnik[2]} (Turniej ID: {zawodnik[3]})" for zawodnik in zawodnicy])
            QMessageBox.information(self, "Zawodnicy", player_list)
        else:
            QMessageBox.information(self, "Brak Zawodników", "Brak zawodników w bazie.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TournamentManager()
    sys.exit(app.exec_())
