import mysql.connector
from mysql.connector import Error
from config import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER 

try:
    connection = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
    cursor = connection.cursor()
    print("Successfully connected to MySQL database")
except Error as e:
    print("Error connecting to MySQL database:", e)

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                username VARCHAR(255),
                toncoin INTEGER
            )''')
connection.commit()

def check_user(userid):
    cursor.execute(f'SELECT * FROM users WHERE user_id = {userid}')
    user = cursor.fetchone()
    if user:
        return True
    return False

def add_user(userid, username, toncoin):
    cursor.execute(f"INSERT INTO users (user_id, username, toncoin) VALUES ({userid}, '{username}', {toncoin})")
    connection.commit()

def get_balance(userid):
    cursor.execute(f'SELECT toncoin FROM users WHERE user_id = {userid}')
    balance = cursor.fetchone()[0]
    return balance

def add_balance(userid, amount):
    cursor.execute(f'UPDATE users SET toncoin = toncoin + {amount} WHERE user_id = {userid}')
    connection.commit()
