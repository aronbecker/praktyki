import sqlite3

class Database:
    def __init__(self, db_name="turniej_db.sqlite"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        # Tabela zawodników
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS zawodnicy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imie TEXT NOT NULL,
                nazwisko TEXT NOT NULL,
                turniej_id INTEGER,
                punkty INTEGER DEFAULT 0,
                FOREIGN KEY (turniej_id) REFERENCES turnieje (id)
            )
        ''')

        # Tabela turniejów
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS turnieje (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                tables INTEGER NOT NULL,
                rounds INTEGER NOT NULL
            )
        ''')

        # Tabela rund
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                tables INTEGER NOT NULL,
                FOREIGN KEY (tournament_id) REFERENCES turnieje (id)
            )
        ''')

        # Tabela stołów
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                runda_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                player_1 TEXT,
                player_2 TEXT,
                player_3 TEXT,
                player_4 TEXT,
                FOREIGN KEY (runda_id) REFERENCES rounds (id)
            )
        ''')

        self.connection.commit()

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    db = Database()
    print("Baza danych została utworzona.")
    db.close()