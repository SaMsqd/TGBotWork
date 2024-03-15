import telebot
from telebot.types import Message

from fullRemake import parsers, items, item_patterns
from fullRemake.database.main import Database


from fullRemake.keyboard import Keyboard as keyboard


TOKEN = '2054290165:AAGNEgLlp1eUDWs_NRldLCnshWl4-5nx-ug'
bot = telebot.TeleBot(token=TOKEN)


def check_user_id(user_id):
    """
    Проверка на наличие БД пользователя. Создание бд, если её нет
    :param user_id:
    :return:
    """
    res = Database.check_table(f'id{user_id}')
    if res:
        return True
    Database(f'id{user_id}')


@bot.message_handler(commands=['start'])
def start(message: Message):
    check_user_id('id'+str(message.chat.id))
    bot.send_message(chat_id=message.chat.id, text='Клавиатура создана', reply_markup=keyboard)


# @bot.message_handler(commands=['help'])
# def help(message: Message):
#     pass


@bot.message_handler(commands=['number'])
def number(message: Message):
    db = Database('id'+str(message.chat.id))
    text = (f'Количество всех итемов: ',
            sum([len(db.get_all("Phones")), len(db.get_all("Ipads")),
                 len(db.get_all("Airpods")), len(db.get_all("Macbooks")), len(db.get_all("Watches"))]))
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard
        )


@bot.message_handler(commands=['clear'])
def clear(message: Message):
    db = Database('id'+str(message.chat.id))
    db.clear()
    bot.send_message(chat_id=message.chat.id, text='Прайсы успешно очищены!')



@bot.message_handler(commands=['table_best'])
def table_best(message: Message):
    db = Database('id'+str(message.chat.id))
    items = db.get_sorted_items()
    text = ''
    version = ''
    storage = 00
    model = ''
    for key in items.keys():
        if len(items[key]) > 0:
            text += key + '\n'
            for item in items[key]:

                if hasattr(item, 'model') and item.model != model or \
                   hasattr(item, 'storage') and storage != item.storage or \
                   hasattr(item, 'version') and version != item.version:
                    text += '\n'

                if len(text) + len(item.generate_str()) > 4000:
                    bot.send_message(chat_id=message.chat.id, text=text.replace('None', ''))
                    text = ''
                if hasattr(item, 'year') and int(item.year) == 10:
                    text += '\n' + item.generate_str().replace('10', '')
                else:
                    text += '\n' + item.generate_str()


                if hasattr(item, 'version') and version != item.version:
                    version = item.version

                if hasattr(item, 'storage') and storage != item.storage:
                    storage = item.storage

                if hasattr(item, 'model') and item.model != model:
                    model = item.model



            text += '\n\n\n'
            version = ''
            storage = ''
            model = ''
    if len(text) != 0:
        bot.send_message(chat_id=message.chat.id, text=text.replace(' None ', ''), reply_markup=keyboard)



@bot.message_handler(commands=['table_opt'])
def table_opt(message: Message):
    db = Database('id'+str(message.chat.id))
    items = db.get_sorted_items()
    text = ''
    version = ''
    storage = 00
    model = ''
    for key in items.keys():
        if len(items[key]) > 0:
            text += key + '\n'
            for item in items[key]:

                if hasattr(item, 'model') and item.model != model or \
                   hasattr(item, 'storage') and storage != item.storage or \
                   hasattr(item, 'version') and version != item.version:
                    text += '\n'

                if len(text) + len(item.generate_opt()) > 4000:
                    bot.send_message(chat_id=message.chat.id, text=text.replace('None', ''))
                    text = ''
                if hasattr(item, 'year') and int(item.year) == 10:
                    text += '\n' + item.generate_opt().replace('10', '')
                else:
                    text += '\n' + item.generate_opt()


                if hasattr(item, 'version') and version != item.version:
                    version = item.version

                if hasattr(item, 'storage') and storage != item.storage:
                    storage = item.storage

                if hasattr(item, 'model') and item.model != model:
                    model = item.model


            text += '\n\n\n'
            version = ''
            storage = ''
            model = ''
    if len(text) != 0:
        bot.send_message(chat_id=message.chat.id, text=text.replace(' None ', ''), reply_markup=keyboard)


@bot.message_handler(commands=['table_1000'])
def table_1000(message: Message):
    db = Database('id'+str(message.chat.id))
    items = db.get_sorted_items()
    text = ''
    version = ''
    storage = 00
    model = ''
    for key in items.keys():
        if len(items[key]) > 0:
            text += key + '\n'
            for item in items[key]:

                if hasattr(item, 'model') and item.model != model or \
                   hasattr(item, 'storage') and storage != item.storage or \
                   hasattr(item, 'version') and version != item.version:
                    text += '\n'

                if len(text) + len(item.generate_1000()) > 4000:
                    bot.send_message(chat_id=message.chat.id, text=text.replace('None', ''))
                    text = ''
                if hasattr(item, 'year') and int(item.year) == 10:
                    text += '\n' + item.generate_1000().replace('10', '')
                else:
                    text += '\n' + item.generate_1000()


                if hasattr(item, 'version') and version != item.version:
                    version = item.version

                if hasattr(item, 'storage') and storage != item.storage:
                    storage = item.storage

                if hasattr(item, 'model') and item.model != model:
                    model = item.model


            text += '\n\n\n'
            version = ''
            storage = ''
            model = ''
    if len(text) != 0:
        bot.send_message(chat_id=message.chat.id, text=text.replace(' None ', ''), reply_markup=keyboard)


@bot.message_handler(commands=['table'])
def table(message: Message):
    pass


@bot.message_handler(commands=['table_retail'])
def table_retail(message: Message):
    db = Database('id' + str(message.chat.id))
    items = db.get_sorted_items()
    text = ''
    version = ''
    storage = 00
    model = ''
    for key in items.keys():
        if len(items[key]) > 0:
            text += key + '\n'
            for item in items[key]:

                if hasattr(item, 'model') and item.model != model or \
                        hasattr(item, 'storage') and storage != item.storage or \
                        hasattr(item, 'version') and version != item.version:
                    text += '\n'

                if len(text) + len(item.generate_retail()) > 4000:
                    bot.send_message(chat_id=message.chat.id, text=text.replace('None', ''))
                    text = ''
                if hasattr(item, 'year') and int(item.year) == 10:
                    text += '\n' + item.generate_retail().replace('10', '')
                else:
                    text += '\n' + item.generate_retail()

                if hasattr(item, 'version') and version != item.version:
                    version = item.version

                if hasattr(item, 'storage') and storage != item.storage:
                    storage = item.storage

                if hasattr(item, 'model') and item.model != model:
                    model = item.model

            text += '\n\n\n'
            version = ''
            storage = ''
            model = ''
    if len(text) != 0:
        bot.send_message(chat_id=message.chat.id, text=text.replace(' None ', ''))


@bot.message_handler(commands=['playstation'])
def playstation(message: Message):
    bot.send_message(chat_id=message.chat.id, text='Загрузите прайс')
    bot.register_next_step_handler(message, _playstation)


def _playstation(message: Message):
    data = message.text.lower()
    play_stations = list()
    headphones = list()
    stations = list()
    wheels = list()
    vrs = list()

    for play_station_model in item_patterns.Playstation.play_station_models:
        if play_station_model in data:
            play_stations.append(play_station_model)
            data = data.replace(play_station_model, '')

    for headphone in item_patterns.Playstation.headphones:
        if headphone in data:
            headphones.append(headphone)
            data = data.replace(headphone, '')

    for station in item_patterns.Playstation.stations:
        if station in data:
            stations.append(station)
            data = data.replace(station, '')

    for wheel in item_patterns.Playstation.wheels:
        if wheel in data:
            wheels.append(wheel)
            data = data.replace(wheel, '')

    for vr in item_patterns.Playstation.vrs:
        if vr in data:
            vrs.append(vr)
            data = data.replace(vr, '')

    data = data.replace('\n\n', '\n')
    print(play_stations, headphones, stations, wheels, vrs)
    print(data)



@bot.message_handler(content_types=['text'])
def parse(message: Message):
    if 'уценка' in message.text.lower():
        data = message.text[:message.text.find('уценка')]
        data = data.replace('\n\n', '\n').replace('₽', '').replace('.', '').replace('🚛', '').replace('р', '').lower().split('\n')
    else:
        data = message.text.replace('\n\n', '\n').replace('₽', '').replace('.', '').replace('🚛', '').replace('р', '').lower().split('\n')

    watches = list()
    airpods = list()
    macbooks = list()
    phones = list()
    ipads = list()
    playstations = list()

    errors = list()

    for pos in data:
        try:
            result, item_name = parsers.Parser.parse_router(pos)
            if item_name == 'watch':
                watches.append(
                    items.Watch(result['model'], result['size'], result['color'], result['strap_size'],
                                result.get('year', 0), result['price'])
                )

            elif item_name == 'airpod':
                airpods.append(
                    items.Airpod(result['model'], result.get('case', 'None'), result.get('year', '10'),
                                 result.get('color', '10'), result['price'])
                )

            elif item_name == 'macbook':
                macbooks.append(
                    items.Macbook(result['model'], result['cpu'], result['color'], result['storage'], result['price'])
                )


            elif item_name == 'phone':
                phones.append(
                    items.Phone(result['model'], result['version'], result['color'], int(result['storage']), result['country'],
                                int(result['price']))
                )

            elif item_name == 'ipad':
                ipads.append(
                    items.Ipad(result['model'], result['storage'], result['color'], result['network'], result['price'])
                )
            elif item_name == 'playstation':
                playstations.append(
                    items.Playstation(result['type'], result['name'], result['price'])
                )
            else:
                errors.append(pos)

        except ValueError:
            errors.append(pos)

        except KeyError as ex:
            print(ex, pos, item_name)
            bot.send_message(chat_id=message.chat.id, text=f'Ошибка в списке проиоритетов, пожалуйста, отправьте строку'
                                                           f'\n\n{pos}\n\nразработчику')

    db = Database('id'+str(message.chat.id))

    db.add_items(watches, 'Watches')
    db.add_items(airpods, 'Airpods')
    db.add_items(macbooks, 'Macbooks')
    db.add_items(phones, 'Phones')
    db.add_items(ipads, 'Ipads')

    success = sum([len(watches), len(airpods), len(macbooks), len(phones), len(ipads)])
    if len(errors) > 0:
        beautiful_error_message = ""
        for error in errors:
            beautiful_error_message += error + "\n"

        bot.send_message(chat_id=message.chat.id, text=f"Было добавлено {success} позиций. Не получилось "
                                                       f"добавить {len(errors)}:"
                                                       f"\n{beautiful_error_message}")
    else:
        bot.send_message(chat_id=message.chat.id, text=f"Все {success} позиций были добавлены в таблицу!")


print('Бот запущен')
bot.polling(non_stop=True)



