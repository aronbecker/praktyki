import sqlite3


class Turniej:
    def __init__(self, name, date, tables, rounds):
        self.name = name
        self.date = date
        self.tables = tables
        self.rounds = rounds

    def save(self):
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
        ''', (self.name, self.date, self.tables, self.rounds))
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM tournaments WHERE name = ?
        ''', (self.name,))
        conn.commit()
        conn.close()

    def update(self, new_name, new_date, new_tables, new_rounds):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tournaments
            SET name = ?, date = ?, tables = ?, rounds = ?
            WHERE name = ?
        ''', (new_name, new_date, new_tables, new_rounds, self.name))
        conn.commit()
        conn.close()