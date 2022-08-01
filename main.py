from tgbot.handlers.dict_handlers import send_rand_word, register_handlers_client
from database.sqlite import Database
from aiogram.dispatcher import FSMContext
import logging
from aiogram import executor
import asyncio
from create_bot import dp, brain

logging.basicConfig(level=logging.INFO)

async def start(dp):
    users = Database().get_all_user()
    for user_id in users:
        if Database().get_notification(user_id[1]) == 'on':
            asyncio.create_task(send_rand_word(user_id[1], FSMContext(storage=brain, chat=user_id[1], user=user_id[1])))


if __name__ == "__main__":
    register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=start)
