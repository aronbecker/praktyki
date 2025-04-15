import sqlite3

class Table:
    def __init__(self, runda_id, name, player_1, player_2, player_3, player_4):
        self.runda_id = runda_id
        self.name = name
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_3 = player_3
        self.player_4 = player_4
        self.table_id = None
    def add_table(self, runda_id, name, player_1, player_2, player_3, player_4):
        conn = sqlite3.connect('tysiac.db')
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
        cursor.execute('''
            INSERT INTO tables (runda_id, name, player_1, player_2, player_3, player_4)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (runda_id, name, player_1, player_2, player_3, player_4))
        conn.commit()
        conn.close()
    def delete_table(self, table_id):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tables WHERE id = ?', (table_id,))
        conn.commit()
        conn.close()
    def delete_tables(self, runda_id):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tables WHERE runda_id = ?', (runda_id,))
        conn.commit()
        conn.close()
    def delete_ALL_tables(self):
        conn = sqlite3.connect('tysiac.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tables')
        conn.commit()
        conn.close()