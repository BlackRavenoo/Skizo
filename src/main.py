import asyncio
import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from config import bot_config
from middlewares.is_owner import IsOwnerMiddleware
from middlewares.action import ActionMiddleware

load_dotenv()
API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if API_TOKEN is None:
    print("Something went wrong with your API_TOKEN. Check your .env file.")
    exit(1)
bot = Bot(token=API_TOKEN)
disp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler()

disp.message.middleware(IsOwnerMiddleware())
disp.callback_query.middleware(IsOwnerMiddleware())
disp.message.middleware(ActionMiddleware())

async def main():
    scheduler.start()
    result: bool = await bot.delete_webhook(drop_pending_updates=True)
    if result:
        from modules.modules import enable_modules
        enable_modules(disp)
        await disp.start_polling(
            bot,
            config=bot_config,
            scheduler=scheduler
        )
    else:
        raise RuntimeError

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот был остановлен")
