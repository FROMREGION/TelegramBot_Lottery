from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup,\
                          InlineKeyboardMarkup, InlineKeyboardButton, \
                          KeyboardButton

# Main Keyboard
ready_button = KeyboardButton("Я участвую!")
ready_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
ready_keyboard.add(ready_button)

# Admin Keyboard

edit_hello_message_button = KeyboardButton("Изменить приветствие", callback_data="edit_hello_message_button")

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_keyboard.add(edit_hello_message_button)
