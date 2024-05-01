import sqlite3
from pyargon2 import hash

class Database_Manager:

    def __init__(self, database_url, salt):
        self.connection = sqlite3.connect(database_url, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.init_tables()

    
    def init_tables(self):
        sql = "CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"
        self.cursor.execute(sql)
        self.connection.commit()


    def get_user_by_username(self, username):
        query = f"SELECT * from users where username = \'{username}\'"
        rows = self.cursor.execute(query).fetchall()
        return rows

    
    def add_user(self, username, password):
        query = f"INSERT INTO users VALUES (NULL, \'{username}\', \'{password}\')"
        print(query)
        self.cursor.execute(query)
        self.connection.commit()