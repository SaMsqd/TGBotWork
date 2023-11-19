import requests.exceptions as rqst

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
    best_values = command_table_best(message, ret=True)
    answer = ""
    previous = ""
    for i in best_values.keys():
        buff = i.split()
        number = buff.pop(0)
        storage = buff.pop(-1)
        color = buff.pop(-1)
        name = " ".join(buff)
        try:
            country = emoji.emojize(db.exec_command(f'SELECT phone_country FROM id{message.chat.id} WHERE phone_number={number} and phone_name="{name}" and phone_color="{color}" and storage="{storage}" and phone_price={best_values[i]}')[0][0])
        except IndexError:
            country = ""
        try:
            if previous == number + name + storage:
                answer += f"{number} {name} {storage} {color}{country} - {make_price_beautiful(int(best_values[i]) + 500)}\n"
            else:
                answer += f"\n{number} {name} {storage} {color}{country} - {make_price_beautiful(int(best_values[i]) + 500)}\n"
                previous = number + name + storage
        except IndexError:
            print("Опять ошибка IndexError. main.py-45")
            bot.send_message(chat_id=message.chat.id, text=f"Произошла ошибка, телефон {number} {name} не будет "
                                                           f"указан в таблице")
    cur_answer = ""
    for line in answer.split("\n"):
        if len(cur_answer + line + "\n") < 1500 or line == "":
            if line == "":
                cur_answer += "\n"
            else:
                cur_answer += line + "\n"
        else:
            bot.send_message(chat_id=message.chat.id, text=cur_answer)
            cur_answer = ""
    bot.send_message(chat_id=message.chat.id, text=cur_answer)


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
        while "\n\n" in phones:
            phones = phones.replace("\n\n", "\n")
        phones = phones.split("\n")
        errors_l = list()
        success = 0
        for phone in phones:
            try:
                data = get_data_from_string(phone)
                db.insert_user(f"id{message.chat.id}", data["name"], data["version"], data["color"],
                               int(data["price"]), data["storage"], data["country"])
                success += 1
            except KeyError:
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
    except rqst.ReadTimeout as e:
        print("Ошибка 'ReadTimeout'. Проблемы либо с подключением, либо с API. Если эта ошибка будет часто повторятся,"
              " то нужно использовать VPN/Proxy")


if __name__ == "__main__":
    while True:
        main()
