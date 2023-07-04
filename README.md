<h1 align="center">Telegram-Ton-Bot</h1>
<p></p>Telegram Ton Bot - это пример Telegram бота, разработанного для приема платежей в криптовалюте Ton с использованием Python. Цель проекта - продемонстрировать, насколько просто можно принимать платежи в Ton с помощью языка программирования Python и библиотеки aiogram.</p>

# Основные функциональные возможности бота:

<p>Возможность пополнения баланса пользователя.</br>
Отображение текущего баланса пользователя.</br>
Оповещение пользователя о подтверждении пополнения баланса.</p>

# Установка 
`git clone https://github.com/ZodiackiIler/Telegram-Ton-Bot.git`
`cd src`
`pip install -r requirements.txt`

# Настройка
`config.py`: содержит настройки бота, включая токен Telegram, адрес кошелька для пополнения и настройки API.</br>
```py
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
```
`main.py`: основной файл, который запускает бота и регистрирует обработчики сообщений.</br>
```py
import asyncio
from aiogram.utils import executor
from handlers.tonbalance import dp
from misc.transaction import start 

async def on_startup(_):
    print('Бот вышел в онлайн')

from handlers import tonbalance
tonbalance.register_handlers_ton(dp)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
```
`.env`: файл, содержащий переменные среды, такие как токен бота, ключ API и настройки базы данных MySQL.</br>
```txt
TOKEN_BOT=your_token_BotFather
apikey=your_apikey_tonapibot
deposit_address=your_deposit_address
mysql_host=your_db_host
mysql_port=3306
mysql_user=your_db_username
mysql_password=your_db_password
mysql_database=your_db_dbname
```
`misc/db.py`: модуль для работы с базой данных MySQL, включающий функции проверки пользователя, получения и обновления баланса.</br>
```py
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
```
`misc/transaction.py`: модуль, отвечающий за проверку новых платежей на кошелек бота и обработку их, включая увеличение баланса пользователя и отправку уведомлений.</br>
```py
import requests
import asyncio
from aiogram import Bot
from aiogram.types import ParseMode
import config
from misc.db import add_balance, check_user

async def start():

    try:
        with open('last_lt.txt', 'r') as f:
            last_lt = int(f.read())
    except FileNotFoundError:
        last_lt = 0

    bot = Bot(token=config.TOKEN_BOT)

    while True:
        await asyncio.sleep(2)

        resp = requests.get(f'{config.API_BASE_URL}/api/v2/getTransactions?'
                            f'address={config.DEPOSIT_ADDRESS}&limit=100&'
                            f'archival=true&api_key={config.API_KEY}').json()

        if not resp['ok']:
            continue

        for tx in resp['result']:
            lt, hash = int(tx['transaction_id']['lt']), tx['transaction_id']['hash']

            if lt <= last_lt:
                continue

            value = int(tx['in_msg']['value'])
            if value > 0:
                userid = tx['in_msg']['message']

                if not userid.isdigit():
                    continue

                userid = int(userid)

                if not check_user(userid):
                    continue

                add_balance(userid, value)

                await bot.send_message(userid, 'Пополнение прошло успешно!\n'
                                      f'*+{value / 1e9:.2f} TON*',
                                      parse_mode=ParseMode.MARKDOWN)

            last_lt = lt
            with open('last_lt.txt', 'w') as f:
                f.write(str(last_lt))
```
`handlers/tonbalance.py`: модуль, содержащий обработчики команд и сообщений бота, такие как приветственное сообщение, запрос баланса и пополнение баланса.
```py
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, \
                          InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import config
from misc.db import check_user, add_user, get_balance

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN_BOT)
dp = Dispatcher(bot)

async def welcome_handler(message: types.Message):
    userid = message.from_user.id 
    username = message.from_user.username
    toncoin = 0

    if not check_user(userid):
        add_user(userid, username, toncoin)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton('Deposit'))
    keyboard.row(KeyboardButton('Balance'))

    await message.answer('Привет!\nЯ пример бота, мой исходный код в [GitHub](https://'
                     'github.com/ZodiackiIler/Telegram-Ton-Bot/)'
                     '\n'
                     'Моя цель - показать, насколько просто получать '
                     'платежи в Ton с помощью Python.\n\n'
                     'Используйте клавиатуру, чтобы протестировать мою функциональность.',
                     reply_markup=keyboard,
                     parse_mode=ParseMode.MARKDOWN)

async def balance_handler(message: types.Message):
    userid = message.from_user.id
    user_balance = get_balance(userid) / 1e9
    await message.answer(f'Ваш баланс: *{user_balance:.2f} TON*',
                         parse_mode=ParseMode.MARKDOWN)

async def deposit_handler(message: types.Message):

    userid = message.from_user.id
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Deposit',
                                  url=f'ton://transfer/{config.DEPOSIT_ADDRESS}&text={userid}')
    keyboard.add(button)

    await message.answer('Пополнить баланс очень просто.\n'
                     'Просто отправьте любое количество TON на этот адрес:\n\n'
                     f'`{config.DEPOSIT_ADDRESS}`\n\n'
                     f'И включите следующий комментарий: `{userid}`\n\n'
                     'Вы также можете пополнить баланс, нажав на кнопку ниже.',
                     reply_markup=keyboard,
                     parse_mode=ParseMode.MARKDOWN)

def register_handlers_ton(dp):
    dp.register_message_handler(welcome_handler, commands=['start', 'help'])
    dp.register_message_handler(balance_handler, commands='balance')
    dp.register_message_handler(balance_handler, Text(equals='balance', ignore_case=True))
    dp.register_message_handler(deposit_handler, commands='deposit')
    dp.register_message_handler(deposit_handler, Text(equals='deposit', ignore_case=True))
```
<p>Проект может быть использован в качестве основы для разработки Telegram-бота с функционалом работы с криптовалютой Ton и базой данных MySQL.</p>

# Пример
<img src="https://github.com/ZodiackiIler/Telegram-Ton-Bot/images/image1.jpg" >

<img src="https://github.com/ZodiackiIler/Telegram-Ton-Bot/images/image2.jpg">

<img src="https://github.com/ZodiackiIler/Telegram-Ton-Bot/images/image3.jpg">

<img src="https://github.com/ZodiackiIler/Telegram-Ton-Bot/images/image4.jpg" >
