import logging

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, \
                          InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

import config
from misc.transaction import *
from misc.transaction import *
from misc.db import *
from config import *

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start', 'help'])
async def welcome_handler(message: types.Message):

    uid = message.from_user.id  
    username = message.from_user.username
    toncoin = "0"

    if not db.check_user(uid):
        db.add_user(uid, username, toncoin)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton('Deposit'))
    keyboard.row(KeyboardButton('Balance'))

    await message.answer('Привет!\nЯ пример бота, мой исходный код в [GitHub](https://'
                     'github.com/ZodiackiIler/Telegram-Ton-Bot/'
                     '\n'
                     'Моя цель - показать, насколько просто получать '
                     'платежи в Ton с помощью Python.\n\n'
                     'Используйте клавиатуру, чтобы протестировать мою функциональность.',
                     reply_markup=keyboard,
                     parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands='balance')
@dp.message_handler(Text(equals='balance', ignore_case=True))
async def balance_handler(message: types.Message):

    uid = message.from_user.id

    user_balance = db.get_tonbalance(uid) / 1e9

    await message.answer(f'Ваш баланс: *{user_balance:.2f} TON*',
                         parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands='deposit')
@dp.message_handler(Text(equals='deposit', ignore_case=True))
async def deposit_handler(message: types.Message):

    uid = message.from_user.id
  
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Deposit',
                                  url=f'ton://transfer/{config.DEPOSIT_ADDRESS}&text={uid}')
    keyboard.add(button)

    await message.answer('Пополнить баланс очень просто.\n'
                     'Просто отправьте любое количество TON на этот адрес:\n\n'
                     f'`{config.DEPOSIT_ADDRESS}`\n\n'
                     f'И включите следующий комментарий: `{uid}`\n\n'
                     'Вы также можете пополнить баланс, нажав на кнопку ниже.',
                     reply_markup=keyboard,
                     parse_mode=ParseMode.MARKDOWN)

def register_handlers_ton(dp: Dispatcher):
    dp.register_message_handler(welcome_handler, commands=['start', 'help'])
    dp.register_message_handler(balance_handler, commands=['balance'])
    dp.register_message_handler(balance_handler, Text(equals='balance', ignore_case=True))
    dp.register_message_handler(deposit_handler, commands=['deposit'])
    dp.register_message_handler(deposit_handler, Text(equals='deposit', ignore_case=True))
