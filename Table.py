import sqlite3

class Table:
    def __init__(self, runda_id, name, player_1="brak", player_2="brak", player_3="brak", player_4="brak"):
        self.runda_id = runda_id
        self.name = name
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_3 = player_3
        self.player_4 = player_4

        # Inicjalizacja tabeli tylko jeśli nie istnieje (można to zrobić np. w głównym skrypcie)
        self.create_table()

    def connect(self):
        return sqlite3.connect('turniej_db.sqlite')

    def create_table(self):
        # Stworzenie tabeli tylko raz, jeśli nie istnieje
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tables (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    runda_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    player_1 TEXT NOT NULL,
                    player_2 TEXT NOT NULL,
                    player_3 TEXT NOT NULL,
                    player_4 TEXT NOT NULL,
                    FOREIGN KEY (runda_id) REFERENCES rounds (id)
                )
            ''')

    def add_table(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tables (runda_id, name, player_1, player_2, player_3, player_4)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.runda_id, self.name, self.player_1, self.player_2, self.player_3, self.player_4))

    @staticmethod
    def delete_table(table_id):
        with sqlite3.connect('turniej_db.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tables WHERE id = ?', (table_id,))

    @staticmethod
    def delete_tables(runda_id):
        with sqlite3.connect('turniej_db.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tables WHERE runda_id = ?', (runda_id,))

    @staticmethod
    def get_tables(runda_id=None):
        with sqlite3.connect('turniej_db.sqlite') as conn:
            cursor = conn.cursor()
            if runda_id is not None:
                cursor.execute('SELECT * FROM tables WHERE runda_id = ?', (runda_id,))
            else:
                cursor.execute('SELECT * FROM tables')
            return cursor.fetchall()
