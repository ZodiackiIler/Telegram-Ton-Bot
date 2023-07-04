import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('mysql_host'),
    'port': os.getenv('mysql_port'),
    'user': os.getenv('mysql_user'),
    'password': os.getenv('mysql_password'),
    'database': os.getenv('mysql_database')
}

class Database:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()

    def check_user(self, uid):
        self.cursor.execute(f'SELECT * FROM users WHERE user_id = {uid}')
        user = self.cursor.fetchone()
        if user:
            return True
        return False
    
    def get_tonbalance(self, uid):
        self.cursor.execute(f'SELECT toncoin FROM users WHERE user_id = {uid}')
        balance = self.cursor.fetchone()[0]
        return balance

    def add_tonbalance(self, uid, amount):
        self.cursor.execute(f'UPDATE users SET toncoin= toncoin + {amount} WHERE user_id = {uid}')
        self.connection.commit()

    def user_exists(self, user_id):
        with self.connection:
            self.cursor.execute(f'SELECT * FROM users WHERE user_id = {uid}')
            result = self.cursor.fetchall()
            return bool(len(result))

    def add_user(self, user_id, username, toncoin):
        with self.connection:
            query = "INSERT INTO users (user_id, username, toncoin) VALUES (%s, %s, %s)"
            values = (user_id, username, toncoin)
            self.cursor.execute(query, values)
            self.connection.commit()
