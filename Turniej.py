import sqlite3


class Turniej:
    def __init__(self, name, date, tables, rounds):
        self.name = name
        self.date = date
        self.tables = tables
        self.rounds = rounds

    def add_tournament(self, name, date, tables, rounds):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                tables INTEGER NOT NULL,
                rounds INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT INTO tournaments (name, date, tables, rounds)
            VALUES (?, ?, ?, ?)
        ''', (name, date, tables, rounds))
        conn.commit()
        conn.close()

    def delete_tournament(self, tournament_id):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tournaments WHERE id = ?', (tournament_id,))
        conn.commit()
        conn.close()

    def update_tournament(self, tournament_id, name, date, tables, rounds):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tournaments
            SET name = ?, date = ?, tables = ?, rounds = ?
            WHERE id = ?
        ''', (name, date, tables, rounds, tournament_id))
        conn.commit()
        conn.close()

    def show_tournament(self):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tournaments')
        tournaments = cursor.fetchall()
        conn.close()
        return tournaments