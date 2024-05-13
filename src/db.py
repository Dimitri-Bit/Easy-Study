 
import sqlite3
from pyargon2 import hash

__USERS_TABLE_QUERY__ = "CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)"
__LECTURES_TABLE_QUERY__ = "CREATE TABLE IF NOT EXISTS lectures (ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, name TEXT, path TEXT)"

class Database_Manager:

    def __init__(self, database_url):
        self.connection = sqlite3.connect(database_url, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.init_tables()

    
    def init_tables(self):
        self.cursor.execute(__USERS_TABLE_QUERY__)
        self.cursor.execute(__LECTURES_TABLE_QUERY__)
        self.connection.commit()


    def get_user_by_username(self, username):
        query = f"SELECT * from users where username = \'{username}\'"
        rows = self.cursor.execute(query).fetchall()
        return rows

    
    def add_user(self, username, password):
        query = f"INSERT INTO users VALUES (NULL, \'{username}\', \'{password}\')"
        self.cursor.execute(query)
        self.connection.commit()

    
    def add_lecture(self, user_id, name, path):
        query = f"INSERT INTO lectures VALUES (NULL, \'{user_id}\', \'{name}\', \'{path}\')"
        self.cursor.execute(query)
        self.connection.commit()


    def get_lectures(self, user_id):
        query = f"SELECT * from lectures where user_id = \'{user_id}\'"
        rows = self.cursor.execute(query).fetchall()
        return rows