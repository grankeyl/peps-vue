import sqlite3


def connect():
    conn = sqlite3.connect("database/database.db")

    cursor = conn.cursor()

    return conn, cursor

class User():
    
    def __init__(self, user_id=None, username=None):
        if username != None:
            conn, cursor = connect()

            cursor.execute(f'SELECT * FROM users WHERE username = "{username}"')
            user = cursor.fetchone()

            if user != None:
                user_id = user[0]
            else:
                self.user_id = None
                return

        conn, cursor = connect()
        cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
        user = cursor.fetchone()

        self.user_id = user[0]
        self.username = user[1]
        self.date = user[2]