import sqlite3


class Users:
    def __init__(self):
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

    def insert(self, uname, pwd):
        self.cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?);
        ''', (uname, pwd))
        self.conn.commit()

    def contains_by_uname_pwd(self, uname, pwd):
        self.cursor.execute('''
            SELECT * FROM users
            WHERE username = ? AND password = ?;
        ''', (uname, pwd))
        users = self.cursor.fetchall()
        return len(users) > 0

    def contains_by_uname(self, uname):
        self.cursor.execute('''
            SELECT * FROM users
            WHERE username = ?;
        ''', (uname,))
        users = self.cursor.fetchall()
        return len(users) > 0