import telebot
import os
from command_funcs import *

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

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
def commands_handler(message):
    for command in commands.keys():
        if command == message.text:
            commands[command](message)


if __name__ == "__main__":
    print("Бот успешно запущен")
    bot.polling(none_stop=True)
