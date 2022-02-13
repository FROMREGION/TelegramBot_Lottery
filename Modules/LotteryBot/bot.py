from TeleShop.settings import TOKEN, PARSE_MODE

from time import sleep
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .keyboard import ready_keyboard, admin_keyboard

from MessageApp.models import TelegramMessagePattern

# ----------------------------------------------------------------------------------------------------------------------

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

channel_id = "-1001338596356"


def run():
    try:
        print("Bot was born!")
        register_handlers_hello(dp)
        executor.start_polling(dp)
    except:
        print("Bot was not started")

# Register -------------------------------------------------------------------------------------------------------------


def register_handlers_hello(dp: dp):
    dp.register_message_handler(hello_message_edit_save, state=HelloMessagePattern.waiting_for_hello_message)

# Commands -------------------------------------------------------------------------------------------------------------


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    text = "12"
    print(text)
    await bot.send_message(message.chat.id, "asdasd", reply_markup=ready_keyboard, parse_mode=PARSE_MODE)


@dp.message_handler(commands=['admin'])
async def process_help_command(message: types.Message):
    await message.reply("Admin Panel", reply_markup=admin_keyboard)


@dp.message_handler(commands=['id'])
async def process_help_command(message: types.Message):
    await bot.send_message(message.chat.id, f"<b>YOUR ID:</b>  <code>{message.chat.id}</code>", parse_mode=PARSE_MODE)

# Message handler ------------------------------------------------------------------------------------------------------


@dp.message_handler()
async def handler_message(message: types.Message):
    if message.text == "Я участвую!":
        user_channel_status = await bot.get_chat_member(chat_id='@cc_clicker_channel', user_id=message.chat.id)
        if user_channel_status["status"] != 'left':
            # Обработка если состоит!!!
            await bot.send_message(message.chat.id, "Отлично!", reply_markup=types.ReplyKeyboardRemove())
        else:
            print(user_channel_status)
            await bot.send_message(message.from_user.id, 'Для участия тебе необходимо подписаться на канал')

    elif message.text == "Изменить приветствие":
        await message.answer("Напиши сообщение приветствия:")
        await HelloMessagePattern.waiting_for_hello_message.set()

    else:
        await bot.send_message(message.chat.id, "Я не понимаю :(")


# Hello Message Pattern Handler ----------------------------------------------------------------------------------------


class HelloMessagePattern(StatesGroup):
    waiting_for_hello_message = State()


async def hello_message_edit_save(message: types.Message, state: FSMContext):
    await state.update_data(hello_message_pattern=message.text)
    user_data = await state.get_data()
    print(user_data["hello_message_pattern"])
    try:
        await message.answer("Стартовое сообщение обновлено!")
    except:
        await message.answer("Произошла непредвиденная ошибка")
    await state.finish()

# ----------------------------------------------------------------------------------------------------------------------
