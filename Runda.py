import sqlite3

class Runda:
    def __init__(self,tournament_id,name,tables,):
        self.tournament_id = tournament_id
        self.tables = tables
        self.name =name

    def add_round(self, tournament_id, name, tables):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                tables INTEGER NOT NULL,
                FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
            )
        ''')
        cursor.execute('''
            INSERT INTO rounds (tournament_id, name, tables)
            VALUES (?, ?, ?)
        ''', (tournament_id, name, tables))
        conn.commit()
        conn.close()
    def delete_round(self, round_id):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM rounds WHERE id = ?', (round_id,))
        conn.commit()
        conn.close()
    def show_rounds(self, tournament_id):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rounds WHERE tournament_id = ?', (tournament_id,))
        rounds = cursor.fetchall()
        conn.close()
        return rounds