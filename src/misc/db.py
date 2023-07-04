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
        try:
            self.connection = mysql.connector.connect(**db_config)
            self.cursor = self.connection.cursor()

            # Create the "users" table if it doesn't exist
            self.cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT PRIMARY KEY,
                    username VARCHAR(255),
                    toncoin DECIMAL(18, 9) DEFAULT 0
                )
                '''
            )
        except mysql.connector.Error as error:
            print("Ошибка подключения к базе данных:", error)

    def check_user(self, uid):
        self.cursor.execute(f'SELECT * FROM users WHERE user_id = {uid}')
        user = self.cursor.fetchone()
        if user:
            return True
        return False
    
    def get_tonbalance(self, uid):
        if not self.connection.is_connected():
            self.connection.reconnect()
            self.cursor = self.connection.cursor()
        self.cursor.execute(f'SELECT toncoin FROM users WHERE user_id = {uid}')
        balance = self.cursor.fetchone()[0]
        return balance

    def add_tonbalance(self, uid, amount):
        self.cursor.execute(f'UPDATE users SET toncoin= toncoin + {amount} WHERE user_id = {uid}')
        self.connection.commit()

    def user_exists(self, uid):
        with self.connection:
            self.cursor.execute(f'SELECT * FROM users WHERE user_id = {uid}')
            result = self.cursor.fetchall()
            return bool(len(result))

    def add_user(self, uid, username):
        with self.connection:
            query = "INSERT INTO users (user_id, username) VALUES (%s, %s)"
            values = (uid, username)
            self.cursor.execute(query, values)
            self.connection.commit()

db = Database(db_config)
