from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup,\
                          InlineKeyboardMarkup, InlineKeyboardButton, \
                          KeyboardButton

# Main Keyboard
ready_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

ready_button = KeyboardButton("Я участвую!")

ready_keyboard.add(ready_button)

# Admin Keyboard
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

help_button = KeyboardButton("❗ПРОЧИТАТЬ СРАЗУ ПОСЛЕ ЗАПУСКА❗")
edit_hello_message_button = KeyboardButton("Изменить приветствие")
edit_record_member_message_button = KeyboardButton("Edit MSG после включения в список участников")
add_admin_user_button = KeyboardButton("Добавить администратора")
export_member_list_button = KeyboardButton("Выгрузить список участников")

admin_keyboard.add(help_button)
admin_keyboard.add(edit_hello_message_button)
admin_keyboard.add(edit_record_member_message_button)
admin_keyboard.add(add_admin_user_button)
admin_keyboard.add(export_member_list_button)
