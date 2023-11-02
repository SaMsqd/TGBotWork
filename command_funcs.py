import telebot
from telebot.types import KeyboardButton


def command_start(message):
    pass


def command_help(message):
    bot.send_message(chat_id=message.chat.id, text=
    '''
    /keyboard_on - включить клавиатуру
    /keyboard_off - выключить клавиатуру
    /clear - очистить таблицу
    /table_best - получить таблицу с лучшими ценами
    /table_client - что-то ещё
    /table_opt - получить таблицу с наценками на товар(наценки вы настраиваете сами в следующей функции)
    /change_opt_prices - запустить процесс смены наценок на товары
    /table - получить таблицу
    /number - количество добавленных телефонов
    '''
                     )


def command_create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    all_commands = list(commands.keys())
    for 
    return keyboard


def command_keyboard_on(message: telebot.types.Message):
    bot.send_message(chat_id=message.chat.id, text="Клавиатура создана", reply_markup=command_create_keyboard())


def command_keyboard_off(message):
    bot.send_message(chat_id=message.chat.id, text="Клавиатура убрана", reply_markup=telebot.types.ReplyKeyboardRemove())


def command_number(message):
    pass


def command_clear(message):
    pass


def command_table_best(message):
    pass


def command_table_client(message):
    pass


def command_table_opt(message):
    pass


def command_change_opt_prices(message):
    pass


def command_table(message):
    pass


from main import bot, commands
