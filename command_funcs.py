import telebot
from telebot.types import KeyboardButton
import os
import time
import countryes


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
/table_opt - получить таблицу с наценками на товар(наценки вы настраиваете сами в следующей функции)
/table - получить таблицу
/number - количество добавленных телефонов

Чтобы добавить в таблицу телефоны, просто введите их в следующем виде:
*Серия  *Название *Объём_хранилища *Цвет_телефона *Цена(можно через точку) *Страна(смайликом)
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
    phones = db.get_all_rows(table_name="id"+str(message.chat.id))
    phone_number = len(phones)
    if phone_number == 1 and phones[0] == "":
        phone_number = 0
    bot.send_message(chat_id=message.chat.id, text=f"Количество телефонов, которое вы добавили: {phone_number}")


def command_clear(message: telebot.types.Message) -> None:
    db.delete_table(table_name="id" + str(message.chat.id))
    reg_user_database(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Данные по телефонам были удалены из вашей базы")


def command_table_best(message: telebot.types.Message, ret: bool = False) -> {str: int}:
    data = db.exec_command(f"SELECT * FROM id{str(message.chat.id)}")
    best_values = dict()
    for phone in data:
        if str(phone[0]) + phone[1] + phone[2] + phone[4] not in best_values.keys():
            best_values[f"{phone[0]} {phone[1]} {phone[2]} {phone[4]}"] = phone[3]
        elif phone[3] < best_values[f"{phone[0]} {phone[1]} {phone[2]}"]:
            best_values[f"{phone[0]} {phone[1]} {phone[2]} {phone[4]} {phone[5]}"] = phone[3]
    if ret:
        return best_values
    answer = ""
    for i in best_values.keys():
        buff = i.split()
        number = buff.pop(0)
        storage = buff.pop(-1)
        color = buff.pop(-1)
        name = " ".join(buff)
        if name != "":
            answer += f"""{number}, {name}, {storage}, {color}, {best_values[i]}, {countryes.get_country(db.exec_command(f'SELECT phone_country FROM id{message.chat.id} WHERE phone_number={number} and phone_name="{name}" and '
                        f'phone_color="{color}" and storage="{storage}" and phone_price={best_values[i]}')[0][0])}\n"""
        else:
            answer += f"""{number}, {storage}, {color}, {best_values[i]}, {countryes.get_country(db.exec_command(f'SELECT phone_country FROM id{message.chat.id} WHERE phone_number={number} and phone_name="{name}" and '
                        f'phone_color="{color}" and storage="{storage}" and phone_price={best_values[i]}')[0][0])}\n"""
    bot.send_message(chat_id=message.chat.id, text=answer)
    # file_name = str(time.strftime('%H%M%S'))
    # with open(f"./files/{file_name}.csv", mode="w+", encoding="utf-8") as f:
    #     f.write("Number, Name, Storage, Color, Country, Price\n")
    #     for i in best_values.keys():
    #         buff = i.split()
    #         number = buff.pop(0)
    #         storage = buff.pop(-1)
    #         color = buff.pop(-1)
    #         name = " ".join(buff)
    #         f.write(f"""{number}, {name}, {storage}, {color}, {countryes.get_country(db.exec_command(f'SELECT phone_country FROM id{message.chat.id} WHERE phone_number={number} and phone_name="{name}" and '
    #                         f'phone_color="{color}" and storage="{storage}" and phone_price={best_values[i]}')[0][0])}, {best_values[i]}\n""")
    # bot.send_document(message.chat.id, open(f"./files/{file_name}.csv", mode="r"))
    # os.remove(f"./files/{file_name}.csv")

# def command_table_client(message: telebot.types.Message):
#     pass


def command_table(message: telebot.types.Message):
    data = db.exec_command(f"SELECT * FROM id{str(message.chat.id)}")
    print(data)
    file_name = str(time.strftime('%H%M%S'))
    with open(f"./files/{file_name}.csv", mode="w+", encoding="utf-8") as f:
        f.write("Number, Name, Storage, Color, Country, Price\n")
        for el in data:
            f.write(f"{el[0]}, {el[1]}, {el[4]}, {el[2]}, {countryes.get_country(el[5])}, {el[3]}\n")
    bot.send_document(message.chat.id, open(f"./files/{file_name}.csv", mode="r"))
    os.remove(f"./files/{file_name}.csv")

from main import bot, commands, check_user, reg_user_database
from main import db as database

db = database
