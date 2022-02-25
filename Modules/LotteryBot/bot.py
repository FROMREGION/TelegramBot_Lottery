from TeleShop.settings import TOKEN, PARSE_MODE, CHANNEL_ID

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .keyboard import ready_keyboard, admin_keyboard

from MessageApp.models import TelegramMessagePattern, TelegramUser
from asgiref.sync import sync_to_async, async_to_sync

from channels.db import database_sync_to_async


# ----------------------------------------------------------------------------------------------------------------------

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

channel_id = CHANNEL_ID


def run():
    try:
        print("Bot was born!")
        register_handlers_hello_message(dp)
        register_handlers_add_admin(dp)
        register_handlers_record_member_message(dp)
        executor.start_polling(dp)
    except:
        print("Bot was not started")


def export():
    return TelegramUser.objects.all()

# Register -------------------------------------------------------------------------------------------------------------


def register_handlers_hello_message(dp: dp):
    dp.register_message_handler(hello_message_edit_save,
                                state=HelloMessagePattern.waiting_for_hello_message)


def register_handlers_add_admin(dp: dp):
    dp.register_message_handler(add_admin_user_save,
                                state=AddAdminUser.waiting_for_admin_id)


def register_handlers_record_member_message(dp: dp):
    dp.register_message_handler(record_member_message_edit_save,
                                state=RecordMemberMessagePattern.waiting_for_record_member_message)


# Commands -------------------------------------------------------------------------------------------------------------


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    try:
        start_message = await sync_to_async(TelegramMessagePattern.objects.get, thread_sensitive=True)(role="start")
        text = start_message.text
    except:
        text = "Edit this msg pls xD"
        await sync_to_async(TelegramMessagePattern.objects.create, thread_sensitive=True)(role="start", text=text)
    await bot.send_message(message.chat.id, text, reply_markup=ready_keyboard, parse_mode=PARSE_MODE)


@dp.message_handler(commands=['admin'])
async def process_help_command(message: types.Message):
    try:
        user = await sync_to_async(TelegramUser.objects.get, thread_sensitive=True)(id=message.chat.id)
        is_admin = user.is_admin
    except:
        is_admin = False

    if is_admin:
        await message.reply("Admin Granted", reply_markup=admin_keyboard)
    else:
        await message.reply("Access Denied", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['id'])
async def process_help_command(message: types.Message):
    await bot.send_message(message.chat.id, f"<b>YOUR ID:</b>  <code>{message.chat.id}</code>", parse_mode=PARSE_MODE)
    await sync_to_async(TelegramUser.objects.update_or_create,
                        thread_sensitive=True)(id=message.chat.id,
                                               defaults={"username": message.chat.username,
                                                         "first_name": message.chat.first_name})


# Message handler ------------------------------------------------------------------------------------------------------


@dp.message_handler()
async def handler_message(message: types.Message):
    if message.text == "Я участвую!":
        user_channel_status = await bot.get_chat_member(chat_id='@cc_clicker_channel', user_id=message.chat.id)
        if user_channel_status["status"] != 'left':
            await sync_to_async(TelegramUser.objects.update_or_create,
                                thread_sensitive=True)(id=message.chat.id,
                                                       defaults={"username": message.chat.username,
                                                                 "first_name": message.chat.first_name,
                                                                 "is_subscribe": True})
            try:
                register_message = await sync_to_async(TelegramMessagePattern.objects.get, thread_sensitive=True)(
                    role="record_member")
                text = register_message.text
            except:
                text = "Edit this 'record_member' msg pls xD"
                await sync_to_async(TelegramMessagePattern.objects.create, thread_sensitive=True)(role="record_member",
                                                                                                  text=text)
            await bot.send_message(message.chat.id, text)
        else:
            await bot.send_message(message.from_user.id, 'Для участия тебе необходимо подписаться на канал '
                                                         '\nПосле подписки нажми ещё раз на кнопку "Я участвую!"')

    # Admin command ----------------------------------------------------------------------------------------------------
    # HELP MESSAGE --------------------------------------------------
    elif message.text == "ПРОЧИТАТЬ СРАЗУ ПОСЛЕ ЗАПУСКА":
        try:
            user = await sync_to_async(TelegramUser.objects.get, thread_sensitive=True)(id=message.chat.id)
            is_admin = user.is_admin
        except:
            is_admin = False
        if is_admin:
            text = "<b>При первом запуске необходимо:</b>\n\n" \
                   "1. Изменить приветствие\n" \
                   "2. Изменить сообщение после включения в список участников\n" \
                   "3. Изменить сообщение которое будет отправлено пользователю"
            await bot.send_message(message.chat.id, text, parse_mode=PARSE_MODE)
        else:
            await bot.send_message(message.chat.id, "Я не понимаю :(")
    # Edit record member message ------------------------------------
    elif message.text == "Изменить приветствие":
        try:
            user = await sync_to_async(TelegramUser.objects.get, thread_sensitive=True)(id=message.chat.id)
            is_admin = user.is_admin
        except:
            is_admin = False
        if is_admin:
            await message.answer("Напиши сообщение приветствия:")
            await HelloMessagePattern.waiting_for_hello_message.set()
        else:
            await bot.send_message(message.chat.id, "Я не понимаю :(")
# Edit hello message -------------------------------------------
    elif message.text == "Изменить сообщение после включения в список участников":
        try:
            user = await sync_to_async(TelegramUser.objects.get, thread_sensitive=True)(id=message.chat.id)
            is_admin = user.is_admin
        except:
            is_admin = False
        if is_admin:
            await message.answer("Edit MSG после включения в список участников:")
            await RecordMemberMessagePattern.waiting_for_record_member_message.set()
        else:
            await bot.send_message(message.chat.id, "Я не понимаю :(")
    # Edit record member message ------------------------------------
    elif message.text == "Изменить приветствие":
        try:
            user = await sync_to_async(TelegramUser.objects.get, thread_sensitive=True)(id=message.chat.id)
            is_admin = user.is_admin
        except:
            is_admin = False
        if is_admin:
            await message.answer("Напиши сообщение приветствия:")
            await HelloMessagePattern.waiting_for_hello_message.set()
        else:
            await bot.send_message(message.chat.id, "Я не понимаю :(")
    # Add admin -----------------------------------------------------
    elif message.text == "Добавить администратора":
        try:
            user = await sync_to_async(TelegramUser.objects.get, thread_sensitive=True)(id=message.chat.id)
            is_admin = user.is_admin
        except:
            is_admin = False
        if is_admin:
            await message.answer("Напиши ID пользователя:")
            await AddAdminUser.waiting_for_admin_id.set()
        else:
            await bot.send_message(message.chat.id, "Я не понимаю :(")
    # Export members list -------------------------------------------
    elif message.text == "Выгрузить список участников":
        try:
            user = await sync_to_async(TelegramUser.objects.get, thread_sensitive=True)(id=message.chat.id)
            is_admin = user.is_admin
        except:
            is_admin = False
        if is_admin:
            export_list = ''
            all_tg_users = await database_sync_to_async(list)(TelegramUser.objects.all())
            for tg_user in all_tg_users:
                export_list += f'@{tg_user.username}\n'

            await bot.send_message(message.chat.id, export_list, parse_mode=PARSE_MODE)
        else:
            await bot.send_message(message.chat.id, "Я не понимаю :(")

    else:
        await bot.send_message(message.chat.id, "Я не понимаю :(")


# Hello Message Pattern Handler ----------------------------------------------------------------------------------------


class HelloMessagePattern(StatesGroup):
    waiting_for_hello_message = State()


async def hello_message_edit_save(message: types.Message, state: FSMContext):
    await state.update_data(hello_message_pattern=message.text)
    user_data = await state.get_data()
    text = user_data["hello_message_pattern"]
    try:
        await sync_to_async(TelegramMessagePattern.objects.update_or_create,
                            thread_sensitive=True)(role="start", defaults={"text": text})
        await message.answer(f"<b>Стартовое сообщение обновлено на:</b> \n\n{text}", parse_mode=PARSE_MODE)
    except:
        await message.answer("Произошла непредвиденная ошибка, обратитесь к администратору")
    await state.finish()

# Hello Message Pattern Handler ----------------------------------------------------------------------------------------


class RecordMemberMessagePattern(StatesGroup):
    waiting_for_record_member_message = State()


async def record_member_message_edit_save(message: types.Message, state: FSMContext):
    await state.update_data(record_member_message_pattern=message.text)
    user_data = await state.get_data()
    text = user_data["record_member_message_pattern"]
    try:
        await sync_to_async(TelegramMessagePattern.objects.update_or_create,
                            thread_sensitive=True)(role="record_member", defaults={"text": text})
        await message.answer(f"<b>Сообщение после успешной записи человека обновлено на:</b> \n\n{text}",
                             parse_mode=PARSE_MODE)
    except:
        await message.answer("Произошла непредвиденная ошибка, обратитесь к администратору")
    await state.finish()

# Admin User Add Handler -----------------------------------------------------------------------------------------------


class AddAdminUser(StatesGroup):
    waiting_for_admin_id = State()


async def add_admin_user_save(message: types.Message, state: FSMContext):
    await state.update_data(add_admin_user_id=message.text)
    user_data = await state.get_data()
    user_id = user_data["add_admin_user_id"]
    print(user_id)
    try:
        await sync_to_async(TelegramUser.objects.update_or_create,
                            thread_sensitive=True)(id=user_id,
                                                   defaults={"is_admin": True})
        await message.answer(f"Назначен новый администратор: \n", parse_mode=PARSE_MODE)
    except:
        new_admin = await sync_to_async(TelegramUser.objects.create, thread_sensitive=True)(id=user_id,
                                                                                            username=f"Admin_{user_id}",
                                                                                            first_name=f"AdminUser_{user_id}",
                                                                                            is_subscribe=False,
                                                                                            is_admin=True,)
        await message.answer(f"Пользователя нет в базе данных, но его аккаунт в телеграме"
                             f" был назначен администратором по ID {user_id}")
    await state.finish()