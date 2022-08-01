from create_bot import bot
from aiogram import types, Dispatcher
from utils.languages import lang, all_language
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from database.sqlite import Database
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from utils.work_with_word import words


class dictionary(StatesGroup):
    enterWord = State()
    confirmWord = State()


class welcome(StatesGroup):
    choose_lang = State()
    notification = State()


async def send_rand_word(user_id, state: FSMContext):
    while True:
        markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)
        markup.add(lang[Database().languageU(user_id)]['send1'], lang[Database().languageU(user_id)]['send2'])
        word = words().give_1_rand_word(user_id)
        async with state.proxy() as data:
            data['word'] = word
        await bot.send_message(user_id, word, reply_markup=markup)
        await asyncio.sleep(1800)


async def mark_as_learned(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        Database().set_status(message.chat.id, data['word'], 'learned')


async def mark_as_viewed(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        Database().set_status(message.chat.id, data['word'], 'viewed')


async def send_welcome(message: types.Message):
    if Database().languageU(message.chat.id) is None:
        user = types.User.get_current()
        markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)
        markup.add('ru🇺🇦', 'eng🇺🇸')
        await message.reply(f"Hi! {user.first_name}\nI'm smart dictionary!\nPowered by @MRXlllll\nChoose language:",
                            reply_markup=markup)
        await welcome.choose_lang.set()
    else:
        await message.answer(f"{lang[Database().languageU(message.chat.id)]['newD']} /newD")


async def message_notification(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(lang[Database().languageU(message.chat.id)]['yes'], lang[Database().languageU(message.chat.id)]['no'])
    await bot.send_message(message.chat.id, lang[Database().languageU(message.chat.id)]['notification'],
                           reply_markup=markup)


async def choose_lang(message: types.Message):
    if message.text.lower() == 'ru🇺🇦':
        Database().add_new_user('ru', message.chat.id)
        await bot.send_message(message.chat.id, 'Язык выбран как русский')
        await bot.send_message(message.chat.id, f"{lang[Database().languageU(message.chat.id)]['AboutDict']}")
        await message_notification(message)
        await welcome.notification.set()
    elif message.text.lower() == 'eng🇺🇸':
        Database().add_new_user('eng', message.chat.id)
        await bot.send_message(message.chat.id, 'Language selected as English')
        await bot.send_message(message.chat.id, f"{lang[Database().languageU(message.chat.id)]['AboutDict']}")
        await message_notification(message)
        await welcome.notification.set()
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)  # Создание кнопок resize_keyboard=True задает размер
        markup.add('ru🇺🇦', 'eng🇺🇸')
        await bot.send_message(message.chat.id, 'Choose language', reply_markup=markup)
    return


async def notification_word(message: types.Message, state: FSMContext):
    if message.text.lower() == lang[Database().languageU(message.chat.id)]['yes'].lower():
        Database().turn_on_notification(message.chat.id)
        asyncio.create_task(send_rand_word(message.chat.id, state))
        await state.finish()
    elif message.text.lower() == lang[Database().languageU(message.chat.id)]['no'].lower():
        Database().turn_off_notification(message.chat.id)
        await state.finish()


async def add_word(message: types.Message):
    await message.answer(f"{lang[Database().languageU(message.chat.id)]['EnterWord']}")
    await dictionary.enterWord.set()


async def wait_new_word(message: types.Message, state: FSMContext):
    await state.update_data(word=message.text.lower())
    await bot.send_message(message.chat.id, f"{lang[Database().languageU(message.chat.id)]['ConfirmNewWord']}")
    await dictionary.confirmWord.set()


async def wait_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == lang[Database().languageU(message.chat.id)]['yes'].lower():
        data = await state.get_data()
        await bot.send_message(message.chat.id, f"{lang[Database().languageU(message.chat.id)]['added']}")
        Database().add_word(data['word'], 'added', message.chat.id)
    elif message.text.lower() == lang[Database().languageU(message.chat.id)]['no']:
        await bot.send_message(message.chat.id, f"{lang[Database().languageU(message.chat.id)]['cancel']}")
        await dictionary.next()
    else:
        await bot.send_message(message.chat.id, f"{lang[Database().languageU(message.chat.id)]['ConfirmNewWord']}")


async def echo(message: types.Message):
    await message.answer(f"{lang[Database().languageU(message.chat.id)]['newD']} /newD")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(mark_as_learned, Text(equals=all_language['send1']))
    dp.register_message_handler(mark_as_viewed, Text(equals=all_language['send2']))
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(choose_lang, state=welcome.choose_lang)
    dp.register_message_handler(notification_word, state=welcome.notification)
    dp.register_message_handler(add_word, commands=['newD'])
    dp.register_message_handler(wait_new_word, state=dictionary.enterWord)
    dp.register_message_handler(wait_confirm, state=dictionary.confirmWord)
    dp.register_message_handler(echo)