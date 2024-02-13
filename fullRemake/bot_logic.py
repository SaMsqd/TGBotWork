import telebot
from telebot.types import Message


TOKEN = '2054290165:AAGo7Dqybp5fkqORKccJZdmZTXNcohdpAKw'

if __name__ == '__main__':
    bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(content_types=['text'])
def start(message: Message):
    bot.send_message(chat_id=message.chat.id, text=message.text + 's')


if __name__ == '__main__':
    bot.polling(non_stop=True, restart_on_change=True)



