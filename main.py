import os
from command_funcs import *
from DB import DataBase

TOKEN: str = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
db = DataBase("test.db")   # Чтобы можно было получить доступ к этой переменной


@bot.message_handler(commands=["table_opt"])
def command_table_opt(message: telebot.types.Message):
    best_values = command_table_best(message, ret=True)
    answer = "Разрабатывется"
    bot.send_message(chat_id=message.chat.id, text=answer)
#    bot.register_next_step_handler(message, get_opt_prices, best_values)


commands = {
    "/start": command_start,
    "/help": command_help,
    "/number": command_number,
    "/clear": command_clear,
    "/table_best": command_table_best,
    #"/table_client": command_table_client,
    "/table_opt": command_table_opt,
    "/change_opt_prices": command_change_opt_prices,
    "/table": command_table,
    "/keyboard_on": command_keyboard_on,
    "/keyboard_off": command_keyboard_off,
}


@bot.message_handler(commands=[x[1:] for x in commands.keys()])
def commands_handler(message: telebot.types.Message) -> None:
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


if __name__ == "__main__":
    print("Бот успешно запущен")
    try:
        bot.polling(none_stop=True)
    except ConnectionError:
        print("Проблема с подключением к интернету/серверу API. Завершаю работу...")
        bot.stop_bot()
