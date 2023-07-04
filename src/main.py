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
