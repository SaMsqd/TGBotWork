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


def get_storage_index(data: str) -> int:
    data = data.replace(".", "").replace(",", "")
    color_index = 0
    for el in data.split():
        if el.lower() in CNV.STORAGE or CNV.delete_flag(el.lower()) in CNV.STORAGE:
            color_index = data.index(el)
            break
    return color_index


@bot.message_handler(commands=["table_opt"])
def command_table_opt(message: telebot.types.Message):
    if check_user(message.chat.id):
        best_sorted = command_table_best(message, ret=True)
        name = ""
        version = ""
        storage = ""
        answer = ""
        for phone in best_sorted:
            if phone[0] != name or phone[1] != version or phone[4] != storage:
                if answer != "":
                    answer += "\n"
                name = phone[0]
                version = phone[1]
                storage = phone[4]
            answer += f"{phone[0]} {phone[1]} {phone[4]} {phone[2]}{phone[5]} - {make_price_beautiful(phone[3] + 500)}\n"
            if len(answer) > 1500:
                answer = answer.split("\n\n")
                for i in range(1, len(answer)).__reversed__():
                    if answer[i][0:get_storage_index(answer[i])] == answer[-1][0:get_storage_index(answer[i-1])] and \
                            answer[i].count("64GB") != 0:
                        answer[i], answer[i-1] = answer[i-1], answer[i]
                bot.send_message(chat_id=message.chat.id, text="\n\n".join(answer))
                answer = ""
        if len(answer) != 0:
            bot.send_message(chat_id=message.chat.id, text=answer)
        else:
            bot.send_message(chat_id=message.chat.id, text="Таблица пуста")
    else:
        bot.send_message(chat_id=message.chat.id, text="Вашего ID нет в системе")


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
                               int(data["price"]), data["storage"].replace("тбGB", "TB"), data["country"].replace("gb", ""))
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
        db.create_table(table_name="id" + str(chat_id), columns={"name": "text", "version": "text",
                        "color": "text", "price": "integer", "storage": "text", "country": "text"})
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
    # except sqlite3.OperationalError as ex:
    #     print("Ошибка с операцией в sqlite", )
    except telebot.apihelper.ApiTelegramException:
        print("Пустое сообщение")


if __name__ == "__main__":
    while True:
        main()
