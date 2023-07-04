import requests
import asyncio
from aiogram import Bot
from aiogram.types import ParseMode
import config
from misc.db import Database

async def start():

    try:
        with open('last_lt.txt', 'r') as f:
            last_lt = int(f.read())
    except FileNotFoundError:
        last_lt = 0

    bot = config.bot

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
                uid = tx['in_msg']['message']

                if not uid.isdigit():
                    continue

                uid = int(uid)
                
                if not Database.check_user(uid):
                    continue

                Database.add_tonbalance(uid, value)

                await bot.send_message(uid, 'Пополнение прошло успешно.\nПополнено:'
                                      f'*{value / 1e9:.2f} TON*',
                                      parse_mode=ParseMode.MARKDOWN)

            last_lt = lt
            with open('last_lt.txt', 'w') as f:
                f.write(str(last_lt))
