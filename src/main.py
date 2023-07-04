from aiogram.utils import executor
from config import dp

async def on_startup(_):
    print('Бот вышел в онлайн')

from handlers import tonbalance
tonbalance.register_handlers_ton(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
