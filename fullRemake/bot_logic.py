import telebot
from telebot.types import Message


TOKEN = '2054290165:AAGo7Dqybp5fkqORKccJZdmZTXNcohdpAKw'
bot = telebot.TeleBot(token=TOKEN)


def check_user_id(user_id):
    """
    Проверка на наличие БД пользователя. Создание бд, если её нет
    :param user_id:
    :return:
    """
    flag = True
    if not flag:   # TODO: Если id нет, создаём бд
        return True


@bot.message_handler(commands=['start'])
def start(message: Message):
    check_user_id(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=message.text + 's')


@bot.message_handler(commands=['help'])
def help(message: Message):
    pass


@bot.message_handler(commands=['number'])
def number(message: Message):
    pass


@bot.message_handler(commands=['clear'])
def clear(message: Message):
    pass


@bot.message_handler(commands=['table_best'])
def table_best(message: Message):
    pass


@bot.message_handler(commands=['table_opt'])
def table_opt(message: Message):
    pass


@bot.message_handler(commands=['table'])
def table(message: Message):
    pass


@bot.message_handler(commands=['table_retail'])
def table_retail(message: Message):
    pass


print('Бот запущен')
bot.polling(non_stop=True)



