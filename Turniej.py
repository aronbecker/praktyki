import sqlite3

class Turniej:
    def __init__(self, name, date, tables, rounds=0):
        self.name = name
        self.date = date
        self.tables = tables
        self.rounds = rounds
        self.create_table()

    def connect(self):
        return sqlite3.connect('turniej_db.sqlite')

    def create_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                tables INTEGER NOT NULL,
                rounds INTEGER NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def add_tournament(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tournaments (name, date, tables)
            VALUES (?, ?, ?)
        ''', (self.name, self.date, self.tables))
        conn.commit()
        conn.close()

    def show_tournament(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tournaments')
        tournaments = cursor.fetchall()
        conn.close()
        return tournaments

    def delete_tournament(self, tournament_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tournaments WHERE id = ?', (tournament_id,))
        conn.commit()
        conn.close()

    def update_tournament(self, tournament_id, name, date, tables):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tournaments
            SET name = ?, date = ?, tables = ?
            WHERE id = ?
        ''', (name, date, tables, tournament_id))
        conn.commit()
        conn.close()

    def update_round_counter(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM tournaments')
        tournament_ids = cursor.fetchall()
        for tournament_id in tournament_ids:
            cursor.execute('SELECT COUNT(*) FROM rounds WHERE tournament_id = ?', (tournament_id[0],))
            round_count = cursor.fetchone()[0]
            cursor.execute('UPDATE tournaments SET rounds = ? WHERE id = ?', (round_count, tournament_id[0]))
        conn.commit()
        conn.close()