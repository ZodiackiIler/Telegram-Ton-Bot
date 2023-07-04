import os
from dotenv import load_dotenv
load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')
DEPOSIT_ADDRESS = os.getenv('deposit_address')
API_KEY = os.getenv('apikey')
RUN_IN_MAINNET = False  # Установите True/False, чтобы переключиться на mainnet или testnet

if RUN_IN_MAINNET:
    API_BASE_URL = 'https://toncenter.com'
else:
    API_BASE_URL = 'https://testnet.toncenter.com'

MYSQL_HOST = os.getenv('mysql_host')
MYSQL_PORT = int(os.getenv('mysql_port'))
MYSQL_USER = os.getenv('mysql_user')
MYSQL_PASSWORD = os.getenv('mysql_password')
MYSQL_DATABASE = os.getenv('mysql_database')
