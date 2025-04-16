import sqlite3

class Table:
    def __init__(self, runda_id, name, player_1="brak", player_2="brak", player_3="brak", player_4="brak"):
        self.runda_id = runda_id
        self.name = name
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_3 = player_3
        self.player_4 = player_4
        self.create_table()

    def connect(self):
        return sqlite3.connect('turniej_db.sqlite')  # Poprawiona nazwa bazy danych

    def create_table(self):
        conn = self.connect()
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
        conn.commit()
        conn.close()

    def add_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tables (runda_id, name, player_1, player_2, player_3, player_4)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.runda_id, self.name, self.player_1, self.player_2, self.player_3, self.player_4))
        conn.commit()
        conn.close()

    def delete_table(self, table_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tables WHERE id = ?', (table_id,))
        conn.commit()
        conn.close()

    def delete_tables(self, runda_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tables WHERE runda_id = ?', (runda_id,))
        conn.commit()
        conn.close()