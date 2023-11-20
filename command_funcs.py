import telebot
from telebot.types import KeyboardButton
import os
import time
import emoji
import CNV


def get_price_index(data: str) -> int:
    data = data.replace(".", "").replace(",", "")
    price_index = 0
    for el in data.split():
        if el.isdigit() or CNV.delete_flag(el).isdigit():
            price_index = data.index(el)
    return price_index


def get_data_from_string(phone_data: str) -> dict[str: str]:
    res_dict = dict()
    phone_data = phone_data.lower().replace("-", " ")
    price_index = get_price_index(phone_data)    # С какой позиции начинается цена
    for COLOR in CNV.COLORS:
        if COLOR in phone_data.lower():
            res_dict["color"] = COLOR.capitalize()
            phone_data = phone_data.replace(COLOR, "")
            break
    price_index = get_price_index(phone_data)
    for STORAGE in CNV.STORAGE:
        if STORAGE in phone_data[0: price_index]:
            if STORAGE == "1tb" or STORAGE == "1":
                res_dict["storage"] = STORAGE.upper()
                phone_data = phone_data.replace(STORAGE, "", 1)
            else:
                res_dict["storage"] = STORAGE + "GB"
                phone_data = phone_data = phone_data.replace(STORAGE, "", 1)
            break
    price_index = get_price_index(phone_data)
    for NAME in CNV.NAMES:
        if NAME in phone_data.lower()[0: price_index]:
            res_dict["name"] = NAME.capitalize()
            phone_data = phone_data.replace(NAME, "", 1)
            break
    price_index = get_price_index(phone_data)
    for VERSION in CNV.VERSIONS:
        if VERSION in phone_data:
            res_dict["version"] = VERSION.capitalize()
            phone_data = phone_data.replace(VERSION, "")
            break
    else:
        res_dict["version"] = ""
    
    if "iphone" in phone_data:
        phone_data = phone_data.replace("iphone", "")
    phone_data = phone_data.replace("  ", " ").replace("-", " ").replace(".", "").replace(",", "").split()
    res_dict["price"] = ""
    res_dict["country"] = ""
    if len(phone_data) == 1:
        try:
            for el in phone_data[0]:
                if el.isdigit():
                    res_dict["price"] += el
                else:
                    res_dict["country"] += el
        except IndexError:
            return {"error": "IndexError"}
    else:
        try:
            for i in phone_data:
                for el in i:
                    if el.isdigit():
                        res_dict["price"] += el
                    else:
                        res_dict["country"] += el
        except IndexError:
            return {"exception": "indexError"}
    return res_dict


# Заказчик попросил сделать вывод цены через точку для удобства
def make_price_beautiful(price):
    rl_price = list(str(price))
    rl_price.reverse()
    res = ""
    for i in range(len(rl_price)):
        if (i+1) % 3 == 0:
            res += rl_price[i] + "."
        else:
            res += rl_price[i]
    if res[-1] == ".":
        res = res[:-1]
    return res[::-1]


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
                "number": "integer", "version": "text", "color": "text", "price": "integer"
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
    f'''
Ваш ID - {message.chat.id}
/keyboard_on - включить клавиатуру
/keyboard_off - выключить клавиатуру
/clear - очистить таблицу
/table_best - получить таблицу с лучшими ценами
/table_opt - получить таблицу с наценками на товар(наценки вы настраиваете сами в следу
ющей функции)
/table - получить таблицу
/number - количество добавленных телефонов
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
    if check_user(message.chat.id):
        phones = db.get_all_rows(table_name="id"+str(message.chat.id))
        phone_number = len(phones)
        if phone_number == 1 and phones[0] == "":
            phone_number = 0
        bot.send_message(chat_id=message.chat.id, text=f"Количество телефонов, которое вы добавили: {phone_number}")
    else:
        bot.send_message(chat_id=message.chat.id, text="Вас, похоже, нет в системе. Пропишите /start")


def command_clear(message: telebot.types.Message) -> None:
    if check_user(message.chat.id):
        db.delete_table(table_name="id" + str(message.chat.id))
        reg_user_database(message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="Данные по телефонам были удалены из вашей базы")


# Функция для определения необходимости сделать замену в списке лучших
def to_replace_positions(cur_phone: tuple, best_sorted: list):  # Возвращает bool и int
    for index, phone in enumerate(best_sorted):
        if cur_phone[0] + cur_phone[1] + cur_phone[2] + cur_phone[4] == phone[0] + phone[1] + phone[2] + phone[4] and \
                ((cur_phone[5] in "🇺🇸" and phone[5] in "🇺🇸" and phone[0] in ["14", "15"]) or \
                (cur_phone[5] in "🇭🇰🇨🇳" and phone[5] in "🇭🇰🇨🇳") or \
                 ((cur_phone[5] not in "🇭🇰🇨🇳🇺🇸" and phone[5] not in "🇺🇸🇭🇰🇨🇳") or ((cur_phone[5] in "🇺🇸" and\
                                        phone[5] in "🇺🇸" and phone[0] not in ["14", "15"])))):
            if cur_phone[3] <= phone[3]:
                return True, index
            else:
                return False, 2
    return False, -1


def command_table_best(message: telebot.types.Message, ret: bool = False):
    if check_user(message.chat.id):
        t_data = db.exec_command(f"SELECT * FROM id{message.chat.id} ORDER BY name, version, storage, country, price")
        best_sorted = []
        for phone in t_data:
            b, index = to_replace_positions(phone, best_sorted)
            if b:
                if index != -1:
                    best_sorted.insert(index, phone)
                    best_sorted.pop(index+1)
            elif index == 2:
                continue
            else:
                best_sorted.append(phone)
        if ret:
            return best_sorted
        bot.send_message(chat_id=message.chat.id, text="Функция пока не умеет выводить")


def command_table(message: telebot.types.Message):
    if check_user(message.chat.id):
        data = db.exec_command(f"SELECT * FROM id{str(message.chat.id)}")
        file_name = str(time.strftime('%H%M%S'))
        with open(f"./files/{file_name}.csv", mode="w+", encoding="utf-8") as f:
            f.write("Number, Name, Storage, Color, Country, Price\n")
            for el in data:
                f.write(f"{el[0]}, {el[1]}, {el[4]}, {el[2]}, {emoji.emojize(el[5])}, {make_price_beautiful(el[3])}\n")
        bot.send_document(message.chat.id, open(f"./files/{file_name}.csv", mode="r"))
        os.remove(f"./files/{file_name}.csv")


from main import bot, commands, check_user, reg_user_database
from main import db as database

db = database
