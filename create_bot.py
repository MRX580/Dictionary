from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

brain = MemoryStorage()
bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(bot, storage=brain)
print("ONLINE")
