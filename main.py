import functools
from functools import wraps
import requests.exceptions as rqst
import telebot
import os
import time
import emoji
import project_databases
import keyboard
from CNV import *

TOKEN: str = "2054290165:AAGo7Dqybp5fkqORKccJZdmZTXNcohdpAKw"
bot = telebot.TeleBot(TOKEN)
keyboard = keyboard.Keyboard()
db = keyboard.active_database


# Отлавливается в парсерах, чтобы нормально добавлять ошибочные строки в роутер парсеров.
# Вызывается при любой ошибке в парсере
class ParseException(Exception):
    def __init__(self, text: str = ''):
        super().__init__(f'Ошибка в парсинге {text}')


# Декоратор. Применяется для проверки наличия таблиц с id пользователя, отправившего сообщение    #TODO: Пофиксить, совсем не отрабатывает
def check_user_id(func):
    def _wrapper(message, ret: bool = False):
        print('обёртка')
        if f'phones{message.chat.id}' in project_databases.databases['phones'].tables.keys():
            return func(message)
        else:
            project_databases.init_tables(message.chat.id)
            if ret:
                return func(message, ret)
            func(message)
    print('Конец обрётки')
    return _wrapper


def get_price_index(data: str) -> int:
    base = data
    data = data.replace(".", "").replace(",", "").replace('-', ' ').replace('(', ' ')
    price_index = 0
    for el in data.split():
        if el.isdigit() or delete_flag(el).isdigit():
            price_index = data.index(el)
    return price_index


def len_model_el(data: str, model: str) -> int:
    for el in data.split():
        if model in el:
            return len(el)


def get_data_from_string(phone_data: str) -> dict[str: str]:
    res_dict = dict()
    phone_data = phone_data.lower().replace("-", " ")
    for COLOR in COLORS:
        if COLOR in phone_data.lower():
            res_dict["color"] = COLOR.capitalize()
            phone_data = phone_data.replace(COLOR, "")
            break
    price_index = get_price_index(phone_data)
    for STORAGE in Phones.STORAGE:
        if STORAGE in phone_data[0: price_index]:
            if STORAGE == "1tb" or STORAGE == "1":
                res_dict["storage"] = STORAGE.upper()
                phone_data = phone_data.replace(STORAGE, "", 1)
            else:
                res_dict["storage"] = STORAGE + "GB"
                phone_data = phone_data.replace(STORAGE, "", 1)
            break
    price_index = get_price_index(phone_data)
    for NAME in Phones.NAMES:
        if NAME in phone_data.lower()[0: price_index]:
            res_dict["name"] = NAME.capitalize()
            phone_data = phone_data.replace(NAME, "", 1)
            break
    for VERSION in Phones.VERSIONS:
        if VERSION in phone_data:
            res_dict["model"] = VERSION.capitalize()
            phone_data = phone_data.replace(VERSION, "")
            break
    else:
        res_dict["model"] = ""

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
            return {"exception": "IndexError"}
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
        if (i + 1) % 3 == 0:
            res += rl_price[i] + "."
        else:
            res += rl_price[i]
    if res[-1] == ".":
        res = res[:-1]
    return res[::-1]


@bot.message_handler(commands=['start'])
@check_user_id
def command_start(message: telebot.types.Message) -> None:
    command_keyboard_on(message, text=f"Здравствуйте, {message.from_user.full_name}. Ваш ID есть "
                                      f"в системе, можете вводить команды")


def command_help(message):
    bot.send_message(chat_id=message.chat.id, text=f'''
Ваш ID - {message.chat.id}
/keyboard_on - включить клавиатуру
/keyboard_off - выключить клавиатуру
/clear - очистить таблицу
/table_best - получить таблицу с лучшими ценами
/table_opt - получить таблицу с наценками на товар
/table - получить файлик со всеми позициями выбранной таблицы
/number - количество добавленных элементов выбранной таблицы
    '''
                     )


def command_keyboard_on(message: telebot.types.Message, text: str):
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard.generate_keyboard())


def command_keyboard_off(message):
    bot.send_message(chat_id=message.chat.id, text="Клавиатура убрана",
                     reply_markup=telebot.types.ReplyKeyboardRemove())


@check_user_id
def command_number(message: telebot.types.Message):
    phones = db.get_all_rows(table_name="id" + str(message.chat.id))
    phone_number = len(phones)
    if phone_number == 1 and phones[0] == "":
        phone_number = 0
    bot.send_message(chat_id=message.chat.id, text=f"Количество телефонов, которое вы добавили: {phone_number}")


@check_user_id
def command_clear(message: telebot.types.Message) -> None:
    db.delete_table(table_name="id" + str(message.chat.id))
    project_databases.init_tables(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Данные по телефонам были удалены из вашей базы")


# Функция для определения необходимости сделать замену в списке лучших
def to_replace_positions(cur_phone: tuple, best_sorted: list) -> bool and int:  # Возвращает bool и int
    for index, phone in enumerate(best_sorted):
        if cur_phone[0] + cur_phone[1] + cur_phone[2] + str(cur_phone[4]) == phone[0] + phone[1] + phone[2] + str(
                phone[4]) and \
                ((cur_phone[5] in "🇺🇸" and phone[5] in "🇺🇸" and phone[0] in ["14", "15"]) or
                 (cur_phone[5] in "🇭🇰🇨🇳" and phone[5] in "🇭🇰🇨🇳") or
                 ((cur_phone[5] not in "🇭🇰🇨🇳🇺🇸" and phone[5] not in "🇺🇸🇭🇰🇨🇳") or ((cur_phone[5] in "🇺🇸" and
                                                                                   phone[5] in "🇺🇸" and phone[
                                                                                       0] not in ["14", "15"])))):
            if cur_phone[3] <= phone[3]:
                return True, index
            else:
                return False, 2
    return False, -1





@check_user_id
def command_table_best(message: telebot.types.Message, ret: bool = False):
    best_sorted = command_table_best(message, True)
    name = ""
    model = ""
    storage = ""
    answer = ""
    for phone in best_sorted:
        if phone[0] != name or phone[1] != model or phone[4] != storage:
            if answer != "":
                answer += "\n"
            name = phone[0]
            model = phone[1]
            storage = phone[4]
        if phone[4] == 1024:
            answer += f"{phone[0]} {phone[1]} 1TB {phone[2]}{phone[5]} - {make_price_beautiful(phone[3] + 500)}\n"
        else:
            answer += f"{phone[0]} {phone[1]} {phone[4]}GB {phone[2]}{phone[5]} - " \
                      f"{make_price_beautiful(phone[3] + 500)}\n"
        if len(answer) > 1500:
            bot.send_message(chat_id=message.chat.id, text=answer)
            answer = ""
    if len(answer) != 0:
        bot.send_message(chat_id=message.chat.id, text=answer)
    else:
        bot.send_message(chat_id=message.chat.id, text="Таблица пуста")


@check_user_id
def command_table(message: telebot.types.Message):
    data = db.exec_command(f"SELECT * FROM id{str(message.chat.id)}")
    file_name = str(time.strftime('%H%M%S'))
    with open(f"./files/{file_name}.csv", mode="w+", encoding="utf-8") as f:
        f.write("Number, Name, Storage, Color, Country, Price\n")
        for el in data:
            f.write(f"{el[0]}, {el[1]}, {el[4]}, {el[2]}, {emoji.emojize(el[5])}, {make_price_beautiful(el[3])}\n")
    bot.send_document(message.chat.id, open(f"./files/{file_name}.csv", mode="r"))
    os.remove(f"./files/{file_name}.csv")


@bot.message_handler(commands=["table_opt"])
@check_user_id
def command_table_opt(message: telebot.types.Message):
    best_sorted = command_table_best(message, ret=True)
    name = ""
    model = ""
    storage = ""
    answer = ""
    for phone in best_sorted:
        if phone[0] != name or phone[1] != model or phone[4] != storage:
            if answer != "":
                answer += "\n"
            name = phone[0]
            model = phone[1]
            storage = phone[4]
        if phone[4] == 1024:
            answer += f"{phone[0]} {phone[1]} 1TB {phone[2]}{phone[5]} - {make_price_beautiful(phone[3] + 500)}\n"
        else:
            answer += f"{phone[0]} {phone[1]} {phone[4]}GB {phone[2]}{phone[5]} - " \
                      f"{make_price_beautiful(phone[3] + 500)}\n"
        if len(answer) > 1500:
            bot.send_message(chat_id=message.chat.id, text=answer)
            answer = ""
    if len(answer) != 0:
        bot.send_message(chat_id=message.chat.id, text=answer)
    else:
        bot.send_message(chat_id=message.chat.id, text="Таблица пуста")


@bot.message_handler(commands=["table_retail"])
@check_user_id
def command_table_retail(message: telebot.types.Message):
    __retail_assistent(message)


@bot.message_handler(commands=["table_retail_file"])
@check_user_id
def command_table_retail_file(message: telebot.types.Message):
    file_name = str(time.strftime('%H%M%S'))
    with open(f"./files/{file_name}.xlsx", mode="w+", encoding="utf-8") as f:
        __retail_assistent(message, f)
    bot.send_document(message.chat.id, open(f"./files/{file_name}.xlsx", mode="r"))
    os.remove(f"./files/{file_name}.xlsx")


def __retail_assistent(message: telebot.types.Message, f=None):
    best_sorted = command_table_best(message, ret=True)
    if f:
        f.write("Наименование, Гарантия\n")
        f.write(" , 14 дней, 1 год\n")
    name = ""
    model = ""
    storage = ""
    answer = ""
    for phone in best_sorted:
        if phone[0] != name or phone[1] != model or phone[4] != storage:
            if answer != "":
                f.write("\n")
            name = phone[0]
            model = phone[1]
            storage = phone[4]
        if f:
            if phone[4] == 1024:
                f.write(f"{phone[0]} {phone[1]} 1TB {phone[2]}{phone[5]}, {make_price_beautiful(phone[3] + 500)}, "
                        f"{make_price_beautiful(phone[3] + 3000)}\n".replace("  ", " "))
            else:
                f.write(f"{phone[0]} {phone[1]} {phone[4]}GB {phone[2]}{phone[5]}, "
                        f"{make_price_beautiful(phone[3] + 500)}, "
                        f"{make_price_beautiful(phone[3] + 3000)}\n".replace("  ", " "))
        else:
            if phone[4] == 1024:
                answer += f"{phone[0]} {phone[1]} 1TB {phone[2]}{phone[5]} - " \
                          f"{make_price_beautiful(phone[3] + 500)}↔️{make_price_beautiful(phone[3] + 3000)}\n"
            else:
                answer += f"{phone[0]} {phone[1]} {phone[4]}GB {phone[2]}{phone[5]} - " \
                          f"{make_price_beautiful(phone[3] + 500)}↔️{make_price_beautiful(phone[3] + 3000)}\n"
            if len(answer) > 1500:
                bot.send_message(chat_id=message.chat.id, text=answer)
                answer = ""


commands = {
    "/start": command_start,
    "/help": command_help,
    "/number": command_number,
    "/clear": command_clear,
    "/table_best": command_table_best,
    "/table_opt": command_table_opt,
    "/table": command_table,
    "/keyboard_on": command_keyboard_on,
    "/keyboard_off": command_keyboard_off,
    "/table_retail": command_table_retail,
    "/table_retail_file": command_table_retail_file
}


@bot.message_handler(commands=[x[1:] for x in commands.keys()])
def commands_handler(message: telebot.types.Message) -> None:
    for command in commands.keys():
        if command == message.text:
            commands[command](message)


@check_user_id
@bot.message_handler(commands=['phones', 'watches', 'airpods', 'macbooks', 'ipads', 'back'])
def change_active_db(message: telebot.types.Message):
    bot.send_message(chat_id=message.chat.id, text=keyboard.change_pos(message.text),
                     reply_markup=keyboard.generate_keyboard())


@check_user_id
@bot.message_handler(content_types=['text'])
def parse_router(message: telebot.types.Message):
    # Подготовка строки
    positions = message.text.replace('.', '').replace(',', '').replace('_', '').lower()
    while '\n\n' in positions:
        positions = positions.replace('\n\n', '')
    positions = positions.split('\n')

    errors = list()
    success = 0
    user_id = message.chat.id
    # Перебор строк
    for position in positions:
        try:
            if is_watch(position):
                data = parse_watches(position)
                project_databases.databases['watches'].insert_user(f'watches{user_id}', data['model'], data['size'],
                                                                data['color'], data['strap_size'],
                                                                data.get('year', 'None'),
                                                                data['price'])
            elif is_airpod(position):
                data = parse_airpods(position)
                project_databases.databases['airpods'].insert_user(f'airpods{user_id}', data['model'],
                                                                data.get('color', 'None'),
                                                                data.get('year', 0), data.get('case', 'None'),
                                                                data['price'])
            elif is_macbook(position):
                data = parse_macbooks(position)
                print(data)
                project_databases.databases['macbooks'].insert_user(f'macbooks{user_id}', data['model'], data['cpu'],
                                                                 data['color'], data['storage'], data['price'])
            elif is_ipad(position):
                data = parse_ipads(position)
                project_databases.databases['ipads'].insert_user(f'ipads{user_id}', data['model'], data['storage'],
                                                              data['color'], data['price'])

            # Телефоны идут в else, так как я не смог придумать для них нормальную проверку. Но и так должно работать
            # нормально, так как для них создан очень чувствительный парсер
            else:
                data = parse_phones(position)
                project_databases.databases['phones'].insert_user(f"phones{user_id}",
                                                               data["name"], data["model"],
                                                               data["color"],
                                                               int(data["price"]),
                                                               int(data["storage"]),
                                                               data["country"].replace("gb", ""))
            success += 1
        except ParseException:
            errors.append(position)
            print('Ошибка в парсинге:', position)

    if len(errors) > 0:
        beautiful_error_message = ""
        for error in errors:
            beautiful_error_message += error + "\n"
        bot.send_message(chat_id=message.chat.id, text=f"Было добавлено {success} позиций. Не получилось "
                                                       f"добавить {len(errors)}:"
                                                       f"\n{beautiful_error_message}")
    else:
        bot.send_message(chat_id=message.chat.id, text=f"Все {success} позиций были добавлены в таблицу!")


# Телефоны пока проверять не буду, так как у них нет принципиального отличия, по которым я могу их вычислить
# def is_phone(data: str) -> bool:
#     data = data.lower()
#     for model in Phones.NAMES:
#         if (model in data.split()) or ('iphone' in data):
#             return True
#     return False


def is_watch(data: str) -> bool:
    data = data.lower()
    for model in Watches.models:
        for size in Watches.sizes:
            if (model in data and size in data) or 'watch' in data or 'aw' in data or 'apple' in data:
                return True
    return False


def is_airpod(data: str) -> bool:
    data = data.lower()
    for model in Airpods.models:
        for case in Airpods.cases:
            if ('airpods' in data) or (model in data.split() and case in data):
                return True
    return False


def is_macbook(data: str) -> bool:
    data = data.lower()
    for model in Macbooks.models:
        for cpu in Macbooks.cpus:
            if (model in data and cpu in data) or \
                    ('mb' in data or 'macbook' in data or 'mac book' in data):
                return True
    return False


def is_ipad(data: str) -> bool:
    data = data.lower()
    for model in Ipads.models:
        for network in Ipads.networks:
            if ('ipad' in data) or (network in data and \
                                    ((not model.isdigit()) and model in data)):
                return True
    return False


def parse_phones(phone: str):
    try:
        data = get_data_from_string(phone)
        data["storage"] = data["storage"].replace("тбGB", "TB").replace("GB", "").replace("TB", "")
        # Заказчик попросил, произвести некоторые изменения
        if data["name"] == '13' and (data["color"] == "Black" or data["color"] == "White") and \
                (data["model"] == "Plus" or data["model"] == "") or \
                data["name"] == '14' and (data["color"] == "Black" or data["color"] == "White") and \
                (data["model"] == "Plus" or data["model"] == ""):
            data["color"] = ["Midnight" if data["color"] == "Black" else "Starlight"][0]
        if data["color"] == "Silver":
            data["color"] = "White"
        if data["model"] == "Max" or data["model"] == "Pro":
            data["model"] = "Pro max"
        if data["storage"] == "1":
            data["storage"] = "1024"
    except KeyError:
        raise ParseException
        # О да! Я отлавливаю две ошибки и объединяю их в мою одну, чтобы
        # мой роутер парсеров смог нормально отработать ошибку)\
    except ValueError:
        raise ParseException
    return data


def parse_watches(watch: str) -> dict:
    res_dict = dict()
    res_dict['price'] = ''

    for model in Watches.models:
        if model in watch[:get_price_index(watch)]:
            res_dict['model'] = model
            watch = watch.replace(model, '', 1)
            break
    else:
        raise ParseException('ошибка в парсинге модели')

    for size in Watches.sizes:
        if size in watch[:get_price_index(watch)]:
            res_dict['size'] = size
            watch = watch.replace(size, '')
            break
    else:
        raise ParseException('ошибка в парсинге размера')

    for strap_size in Watches.strap_sizes:
        if strap_size in watch[:get_price_index(watch)]:
            res_dict['strap_size'] = strap_size
            watch = watch.replace(strap_size, '')
            if 'alpine loop' in watch:
                res_dict['strap_size'] = 'alpine loop ' + res_dict['strap_size']
            break
    else:
        raise ParseException('ошибка в парсинге размера ремешка')

    for color in Watches.colors:
        if color in watch[:get_price_index(watch)]:
            res_dict['color'] = color
            watch = watch.replace(color, '')
            break

    else:
        raise ParseException('ошибка в парсинге цвета')

    for year in Watches.year:
        if year in watch[:get_price_index(watch)]:
            res_dict['year'] = year
            watch = watch.replace(year, '')
            break

    for symb in watch[get_price_index(watch):]:
        if symb.isdigit():
            res_dict['price'] = res_dict['price'] + symb

    return res_dict


def parse_airpods(airpod: str) -> dict:
    airpod = airpod.replace('max', 'pro').lower()
    res_dict = dict()
    res_dict['price'] = ''

    for model in Airpods.models:
        if (model != '2' or model != '3') and model in airpod[:get_price_index(airpod)] \
                or len_model_el(airpod, model) == 1:
            res_dict['model'] = model
            airpod = airpod.replace(model, '', 1)
            break
    else:
        raise ParseException('ошибка в парсинге модели')

    for color in COLORS:
        if color in airpod:
            res_dict['color'] = color
            airpod = airpod.replace(color, '')
            break

    for year in Airpods.year:
        if year in airpod and 2010 <= int(year) <= 2024:
            res_dict['year'] = year
            airpod = airpod.replace(year, '')
            break
        if res_dict['model'] == 'pro 2 lightning':
            res_dict['year'] = '2022'
            airpod = airpod.replace('2022', '')
            break
        if res_dict['model'] == 'pro 2 lightning':
            res_dict['year'] = '2023'
            airpod = airpod.replace('2023', '')
            break

    for case in Airpods.cases:
        if case in airpod[: get_price_index(airpod)]:
            res_dict['case'] = case
            break

    for symb in airpod[get_price_index(airpod):]:
        if symb.isdigit():
            res_dict['price'] = res_dict['price'] + symb

    return res_dict


def parse_macbooks(macbook: str) -> dict:
    macbook = macbook.lower().replace('2022', '').replace('2023', '')
    res_dict = dict()
    res_dict['price'] = ''

    for model in Macbooks.models:
        if model in macbook[:get_price_index(macbook)] and len_model_el(macbook, model) == 2:
            if 'pro' in macbook:
                res_dict['model'] = 'pro ' + model
                macbook = macbook.replace('pro ' + model, '', 1)
                break
            elif 'air' in macbook:
                res_dict['model'] = 'air ' + model
                macbook = macbook.replace('air ' + model, '', 1)
                break
    else:
        raise ParseException('ошибка в парсинге модели')

    for color in COLORS:
        if color in macbook:
            res_dict['color'] = color
            macbook = macbook.replace(color, '')
            break
    else:
        raise ParseException('ошибка в парсинге цвета')

    for cpu in Macbooks.cpus:
        if cpu in macbook:
            res_dict['cpu'] = cpu
            macbook = macbook.replace(cpu, '')
            break
    else:
        raise ParseException('ошибка в парсинге процессора')

    for storage in Macbooks.storages:
        if storage in macbook:
            res_dict['storage'] = storage
            macbook = macbook.replace(storage, '')
            break
    else:
        raise ParseException('ошибка в парсинге хранилища')

    price_index = get_price_index(macbook)
    for symb in macbook[price_index:]:
        if symb.isdigit():
            res_dict['price'] = res_dict['price'] + symb

    return res_dict


def parse_ipads(ipad: str) -> dict:
    ipad = ipad.lower()
    res_dict = dict()
    res_dict['price'] = ''
    for model in Ipads.models:
        if model in ipad[:get_price_index(ipad)]:
            res_dict['model'] = model
            ipad = ipad.replace(model, '', 1)
            break

    else:
        raise ParseException('ошибка в парсинге модели')

    for storage in Ipads.storages:
        if storage in ipad:
            res_dict['storage'] = storage
            ipad = ipad.replace(storage, '')
            break
    else:
        raise ParseException('ошибка в парсинге хранилища')

    for color in COLORS:
        if color in ipad:
            res_dict['color'] = color
            ipad = ipad.replace(storage, '')
            break
    else:
        raise ParseException('ошибка в парсинге цвета')

    for network in Ipads.networks:
        if network in ipad:
            res_dict['network'] = network
            ipad = ipad.replace(network, '')
            break
    else:
        raise ParseException('ошибка в парсинге поддреживаемой сети')

    price_index = get_price_index(ipad)
    for symb in ipad[price_index:]:
        if symb.isdigit():
            res_dict['price'] = res_dict['price'] + symb

    return res_dict


def main():
    print("Бот успешно запущен")
    try:
        bot.polling(none_stop=True)
    except ConnectionError:
        print("Проблема с подключением к интернету/серверу API. Завершаю работу...")
        bot.stop_bot()
    except rqst.ReadTimeout:
        print("Ошибка 'ReadTimeout'. Проблемы либо с подключением, либо с API. Если эта ошибка будет часто повторятся,"
              " то нужно использовать VPN/Proxy")
    except telebot.apihelper.ApiTelegramException:
        print("Пустое сообщение")


if __name__ == "__main__":
    while True:
        main()
