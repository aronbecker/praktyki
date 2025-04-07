import sqlite3

class Zawodnicy:
    def __init__(self, db_name="turniejedb.sqlite3"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS zawodnicy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imie TEXT NOT NULL,
                nazwisko TEXT NOT NULL,
                turniej_id INTEGER,
                punkty INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def add_zawodnik(self, imie, nazwisko, turniej_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO zawodnicy (imie, nazwisko, turniej_id, punkty)
            VALUES (?, ?, ?, 0)
        ''', (imie, nazwisko, turniej_id))
        conn.commit()
        conn.close()

    def show_zawodnicy(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM zawodnicy')
        zawodnicy = cursor.fetchall()
        conn.close()
        return zawodnicy

    def update_punkty(self, zawodnik_id, punkty):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE zawodnicy SET punkty = ? WHERE id = ?", (punkty, zawodnik_id))
        conn.commit()
        conn.close()

    