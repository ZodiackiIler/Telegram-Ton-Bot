from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from misc.db import Database
from aiogram import types

storage=MemoryStorage()

load_dotenv()

token = os.getenv('TOKEN_BOT')

DEPOSIT_ADDRESS = 'your_wallet_address'
API_KEY = os.getenv('apikey')
RUN_IN_MAINNET = False  # Ставь True/False чтобы сменить mainnet или testnet

if RUN_IN_MAINNET:
    API_BASE_URL = 'https://toncenter.com'
else:
    API_BASE_URL = 'https://testnet.toncenter.com'

bot = Bot(token);
dp = Dispatcher(bot)
