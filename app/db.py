import sqlite3


class Users:
    def __init__(self):
        self.conn = sqlite3.connect('../users.db', check_same_thread=False)
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

    def return_pass_by_uname(self, uname):
        self.cursor.execute('''
                    SELECT password FROM users
                    WHERE username = ?;
                ''', uname)
        users = self.cursor.fetchall()
        return users

    def contains_by_uname(self, uname):
        self.cursor.execute('''
            SELECT * FROM users
            WHERE username = ?;
        ''', (uname,))
        users = self.cursor.fetchall()
        return len(users) > 0



class Stores:
    def __init__(self):
        self.conn = sqlite3.connect('../stores.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                store_name TEXT NOT NULL,
                store_path TEXT NOT NULL
            )
        ''')

    def insert(self, uname, sname, spath):
        self.cursor.execute('''
            INSERT INTO stores (username, store_name, store_path)
            VALUES (?, ?, ?);
        ''', (uname, sname, spath))
        self.conn.commit()

    def get_by_uname(self, uname):
        self.cursor.execute('''
            SELECT * FROM stores
            WHERE username = ?;
        ''', (uname,))
        users = self.cursor.fetchall()
        return users

    def remove(self, uname, sname):
        self.cursor.execute('''
            DELETE FROM stores
            WHERE username = ? AND store_name = ?;
        ''', (uname, sname))
        self.conn.commit()
