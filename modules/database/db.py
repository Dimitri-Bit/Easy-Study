import sqlite3
from pyargon2 import hash
from modules.auth.user import User

DATABASE = "db.db"
SALT = "Some_Random_Salt_HeHe"

class Database_Manager:

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.init_tables()

    
    def init_tables(self):
        sql = "CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"
        self.cursor.execute(sql)
        self.connection.commit()


    def get_user_by_username(self, username):
        query = f"SELECT * from users where username = '{username}'"
        rows = self.cursor.execute(query).fetchall()
        return rows

    
    def add_user(self, username, password):
        query = f"INSERT INTO users VALUES (NULL, '{username}', '{password}')"
        self.cursor.execute(query)
        self.connection.commit()