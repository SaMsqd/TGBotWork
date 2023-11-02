import telebot
from telebot.types import KeyboardButton


def command_start(message: telebot.types.Message) -> None:
    if check_user(message.chat.id):
        bot.send_message(chat_id=message.chat.id, text=f"Здравствуйте, {message.from_user.full_name}. Ваш ID есть "
        f"в системе, можете вводить команды")
        command_keyboard_on(message)
    else:
        bot.send_message(chat_id=message.chat.id, text=f"Здравствуйте, {message.from_user.full_name}. Видимо,"
                                                       f" вы у нас впервые, заношу ваш ID в базу данных...")
        if reg_user_database(message.chat.id):
            db.create_table(table_name=f"id{message.chat.id}", columns={
                "phone_number": "integer", "phone_name": "text", "phone_color": "text", "phone_price": "integer"
            })
            bot.send_message(chat_id=message.chat.id, text=f"Поздравляю, вы успешно зарегистрированы, ваш id - "
                                                           f"{message.chat.id}.\n\nЕсли вы потеряете доступ к текущему"
                                                           f"телеграм-аккаунту, можете обратиться к владельцу бота "
                                                           f"с целью восстановления")
        else:
            bot.send_message(chat_id=message.chat.id, text="Произошла какая-то ошибка, вы не были добавлены... "
                                                           "Обратитесь к владельцу бота")



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

Чтобы добавить в таблицу телефоны, просто введите их в следующем виде:
*Серия  *Название *Объём_хранилища *Цена(можно через точку) *Страна(смайликом или текстом)
    '''
                     )


def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    all_commands = list(commands.keys())
    row = list()
    for i in range(len(all_commands)):
        row.append(KeyboardButton(text=all_commands[i]))
        if all_commands[i] == "/keyboard_on":
            row.pop(-1)
            row.append(KeyboardButton(text="/keyboard_off"))
        if i % 3 == 0:
            keyboard.row(*row)
            row = []
    return keyboard


def command_keyboard_on(message: telebot.types.Message):
    bot.send_message(chat_id=message.chat.id, text="Клавиатура создана", reply_markup=create_keyboard())


def command_keyboard_off(message):
    bot.send_message(chat_id=message.chat.id, text="Клавиатура убрана", reply_markup=telebot.types.ReplyKeyboardRemove())


def command_number(message: telebot.types.Message):
    phones = db.get_user_by(table_name="id"+str(message.chat.id), value=message.chat.id)[0][1].split("\n")
    phone_number = len(phones)
    if phone_number == 1 and phones[0] == "":
        phone_number = 0
    bot.send_message(chat_id=message.chat.id, text=f"Количество телефонов, которое вы добавили: {phone_number}")


def command_clear(message: telebot.types.Message) -> None:
    db.delete_table(table_name="id" + str(message.chat.id))
    reg_user_database(message.chat.id)


def command_table_best(message: telebot.types.Message):
    pass


def command_table_client(message):
    pass


def command_table_opt(message):
    pass


def command_change_opt_prices(message):
    pass


def command_table(message):
    pass


from main import bot, commands, check_user, db, reg_user_database
