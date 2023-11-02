import os
from command_funcs import *
from DB import DataBase

TOKEN: str = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
db = DataBase("test.db")   # Чтобы можно было получить доступ к этой переменной

commands = {
    "/start": command_start,
    "/help": command_help,
    "/number": command_number,
    "/clear": command_clear,
    "/table_best": command_table_best,
    "/table_client": command_table_client,
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


@bot.message_handler(content_types=["text"])
def parse_phones(message: telebot.types.Message):
    if check_user(message.chat.id):
        phones = message.text
        phones = phones.replace("\n\n", "\n").split("\n")
        for phone in phones:
            pass
    else:
        bot.send_message(chat_id=message.chat.id, text="Простите, но вы ещё не зарегистрированы у нас. Чтобы начать"
                                                       "работу, надо ввести команду /start")


def check_user(chat_id) -> bool:    # Есть ли пользователь в базе данных
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
    bot.polling(none_stop=True)
