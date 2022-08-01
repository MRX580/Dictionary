from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import API_TOKEN
brain = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=brain)
