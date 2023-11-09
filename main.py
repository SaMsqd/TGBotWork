import os
import time

import telebot.types

from command_funcs import *
from DB import DataBase

TOKEN: str = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
db = DataBase("test.db")   # Чтобы можно было получить доступ к этой переменной
# Эти переменные для функции command_table_opt. Да, делал через костыли. Соболезную тем, кто будет поддерживать это код,
# хотя, скорее всего, это буду я сам... Блять, я себя захуярил
cur_overprice = 0
wait = True


@bot.message_handler(commands=["table_opt"])
def command_table_opt(message: telebot.types.Message):
    global cur_overprice
    global wait
    best_values = command_table_best(message, ret=True)
    old_values = best_values.copy()
    sended_phones = dict()   # Эта переменная меняется в функции __get_opt_price
    for i in best_values.keys():
        buff = i.split()
        number = buff.pop(0)
        buff.pop(-1)
        buff.pop(-1)
        name = " ".join(buff)
        if number + name not in sended_phones.keys():
            wait = True
            get_opt_price(message, number + name)
            while wait:
                time.sleep(0.5)
            sended_phones[number + name] = cur_overprice
        best_values[i] += sended_phones[number + name]
    file_name = str(time.strftime('%H%M%S'))
    with open(f"./files/{file_name}.csv", mode="w+", encoding="utf-8") as f:
        f.write("Number, Name, Storage, Color, Country, Price\n")
        for i in best_values.keys():
            buff = i.split()
            number = buff.pop(0)
            storage = buff.pop(-1)
            color = buff.pop(-1)
            name = " ".join(buff)
            f.write(f"""{number}, {name}, {storage}, {color}, {countryes.get_country(db.exec_command(f'SELECT phone_country FROM id{message.chat.id} WHERE phone_number={number} and phone_name="{name}" and '
                            f'phone_color="{color}" and storage="{storage}" and phone_price={old_values[i]}')[0][0])}, {best_values[i]}\n""")
    bot.send_document(message.chat.id, open(f"./files/{file_name}.csv", mode="r"))
    os.remove(f"./files/{file_name}.csv")



def __get_opt_price(message: telebot.types.Message):
    global cur_overprice
    global wait
    try:
        cur_overprice = int(message.text)
        wait = False
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text="Похоже, вы ввели символ...")


def get_opt_price(message: telebot.types.Message, name: str):
    bot.send_message(chat_id=message.chat.id, text=f"Введите наценку для товара {name}")
    bot.register_next_step_handler(message=message, callback=__get_opt_price)




commands = {
    "/start": command_start,
    "/help": command_help,
    "/number": command_number,
    "/clear": command_clear,
    "/table_best": command_table_best,
    #"/table_client": command_table_client,
    "/table_opt": command_table_opt,
    "/table": command_table,
    "/keyboard_on": command_keyboard_on,
    "/keyboard_off": command_keyboard_off,
}


@bot.message_handler(commands=[x[1:] for x in commands.keys()])
def commands_handler(message: telebot.types.Message) -> None:
    global db
    for command in commands.keys():
        if command == message.text:
            commands[command](message)
        db = DataBase("test.db")


@bot.message_handler(content_types=["text"])
def parse_phones(message: telebot.types.Message):
    if check_user(message.chat.id):
        phones = message.text
        phones = phones.replace("\n\n", "\n").split("\n")
        errors_l = list()
        success = 0
        for phone in phones:
            for i in range(len(phone)-1, 0, -1):
                if phone[i].isdigit():
                    phone = phone[:i+1] + " " + phone[i+1:]
                    break
            phone = phone.replace(".", "").replace("-", " ").replace("  ", " ")
            try:
                data = phone.split()
                number = data.pop(0)
                country = data.pop(-1)
                price = data.pop(-1)
                color = data.pop(-1)
                storage = data.pop(-1)
                name = " ".join(data)
                if not storage[0].isdigit():
                    name += " " + storage
                db.insert_user("id"+str(message.chat.id), int(number), name, color, int(price), storage, country)
                success += 1
            except IndexError:
                errors_l.append(phone)
            except ValueError:
                errors_l.append(phone)
                print(f"Что-то обработалось не так... {phone}")
        if len(errors_l) > 0:
            beautiful_error_message = ""
            for error in errors_l:
                beautiful_error_message += error + "\n"
            bot.send_message(chat_id=message.chat.id, text=f"Было добавлено {success} телефонов, не получилось "
                                                                   f"добавить {len(errors_l)} телефонов:\n{beautiful_error_message}"
                                                                   f"\n\nВозможно, эта строка не была похожа на шаблон. "
                                                                   f"Чтобы ознакомится с ним, введите /help")
        else:
            bot.send_message(chat_id=message.chat.id, text=f"Все {success} телефонов были добавлены в таблицу!")
    else:
        bot.send_message(chat_id=message.chat.id, text="Простите, но вы ещё не зарегистрированы у нас. Чтобы начать"
                                                       " работу, надо ввести команду /start")


def check_user(chat_id) -> bool:    # Есть ли пользователь в базе данных
    db.update_tables()
    if "id" + str(chat_id) in db.tables.keys():
        return True
    return False


def reg_user_database(chat_id) -> bool:
    try:
        db.create_table(table_name="id" + str(chat_id), columns={"phone_number": "integer", "phone_name": "text",
                        "phone_color": "text", "phone_price": "integer", "storage": "text", "phone_country": "text"})
        return True
    except Exception:
        return False


def main():
    print("Бот успешно запущен")
    try:
        bot.polling(none_stop=True)
    except ConnectionError:
        print("Проблема с подключением к интернету/серверу API. Завершаю работу...")
        bot.stop_bot()


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as ex:
            print(ex)
