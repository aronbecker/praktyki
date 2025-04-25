import sqlite3

class Zawodnicy:
    def __init__(self, db_name="turniej_db.sqlite"):
        self.db_name = db_name
        self.create_table()

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

    def count_points(self, turniej_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("Select * FROM tables JOIN rounds ON tables.round_id = rounds.id WHERE round.turnament_id = ?", (turniej_id,))
        
        total_points = cursor.fetchone()[0]
        conn.close()

        return total_points if total_points is not None else 0

    def delete_zawodnik(self, zawodnik_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM zawodnicy WHERE id = ?", (zawodnik_id,))
        conn.commit()
        conn.close()

    def update_zawodnik(self, zawodnik_id, imie, nazwisko, turniej_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE zawodnicy
            SET imie = ?, nazwisko = ?, turniej_id = ?
            WHERE id = ?
        ''', (imie, nazwisko, turniej_id, zawodnik_id))
        conn.commit()
        conn.close()