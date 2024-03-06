from telebot.types import ReplyKeyboardMarkup, KeyboardButton


Keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
text = ['/number', '/clear', '/table',
        '/table_best', '/table_opt', '/table_retail',
        '/table_retail_file', '/table_1000']

buttons = []
for t in text:
    buttons.append(KeyboardButton(text=t))

Keyboard.add(*buttons)
