from exceptions import ParseException
from fullRemake import item_patterns
from item_patterns import *
import re


class Parser:
    @staticmethod
    def get_data_from_string(phone_data: str) -> dict[str: str]:
        res_dict = dict()
        phone_data = phone_data.lower().replace("-", " ").replace('iphone', '').replace('apple', '')

        for COLOR in COLORS:
            if COLOR in phone_data.lower():
                res_dict["color"] = COLOR.capitalize()
                phone_data = phone_data.replace(COLOR, "")
                break
        phone_data = phone_data.strip()
        price_index = Parser.get_price_index(phone_data)

        for STORAGE in Phones.STORAGE:
            if STORAGE in phone_data[0: price_index]:
                if STORAGE == "1tb" or STORAGE == "1":
                    res_dict["storage"] = STORAGE.upper()
                    phone_data = phone_data.replace(STORAGE, "", 1)
                else:
                    res_dict["storage"] = STORAGE + "GB"
                    phone_data = phone_data.replace(STORAGE, "", 1)
                break

        price_index = Parser.get_price_index(phone_data)

        for NAME in Phones.MODELS:
            if NAME in phone_data.lower()[0: price_index]:
                res_dict["model"] = NAME.capitalize()
                phone_data = phone_data.replace(NAME, "", 1)


        for VERSION in Phones.VERSIONS:
            if VERSION in phone_data:
                res_dict["version"] = VERSION.capitalize()
                phone_data = phone_data.replace(VERSION, "")
                break
        else:
            res_dict["version"] = ""

        if "iphone" in phone_data:
            phone_data = phone_data.replace("iphone", "")
        phone_data = phone_data.replace("  ", " ").replace("-", " ").replace(".", "").replace(",", "").split()
        res_dict["price"] = ""
        res_dict["country"] = ""
        buff = ''
        if len(phone_data) == 1:
            try:
                for i in phone_data:
                    for el in i:
                        if el.isdigit():
                            buff += el
                    if buff.isdigit() and int(buff) > 1000:
                        res_dict['price'] = buff
                    elif res_dict["country"] == '' and not buff.isdigit():
                        res_dict["country"] = i
                    buff = ''

            except IndexError:
                return {"exception": "IndexError"}
        else:
            try:
                for i in phone_data:
                    for el in i:
                        if el.isdigit():
                            res_dict["price"] += el
                    if res_dict["country"] == '' and not i.isdigit():
                        res_dict["country"] = i
            except IndexError:
                return {"exception": "indexError"}
        return res_dict

    @staticmethod
    def delete_flag(data: str) -> str:
        for el in Phones.COUNTRIES[0]:
            data = data.replace(el, "")
        return data

    @staticmethod
    def len_model_el(data: str, model: str) -> int:
        for el in data.split():
            if model in el:
                return len(el)

    @staticmethod
    def get_price_index(data: str) -> int:
        base = data
        data = data.replace(".", "").replace(",", "").replace('-', ' ').replace('(', '').replace(')', ' ')
        price_index = 0
        for el in data.split():
            if el.isdigit() or Parser.delete_flag(el).isdigit():
                price_index = data.index(el)
        return price_index

    @staticmethod
    def parse_phones(phone: str):
        try:
            data = Parser.get_data_from_string(phone)
            data["storage"] = data["storage"].replace("тбGB", "TB").replace("GB", "").replace("TB", "")
            # Заказчик попросил, произвести некоторые изменения
            if data["model"] == '13' and (data["color"] == "Black" or data["color"] == "White") and \
                    (data["version"] == "Plus" or data["version"] == "") or \
                    data["model"] == '14' and (data["color"] == "Black" or data["color"] == "White") and \
                    (data["model"] == "Plus" or data["version"] == ""):
                data["color"] = ["Midnight" if data["color"] == "Black" else "Starlight"][0]
            if data["color"] == "Silver":
                data["color"] = "White"
            if data["version"] == "Max" or data["version"] == "Pro":
                data["version"] = "Pro max"
            if data["storage"] == "1":
                data["storage"] = "1024"
            if data['country']:
                for el in data['country'][::-1]:
                    if el not in Phones.COUNTRIES or el.isdigit():
                        data['country'] = data['country'].replace(el, '')
        except KeyError or ValueError:
            raise ParseException
            # О да! Я отлавливаю две ошибки и объединяю их в мою одну, чтобы
            # мой роутер парсеров смог нормально отработать ошибку)
        return data

    @staticmethod
    def parse_watches(watch: str) -> dict:
        res_dict = dict()
        res_dict['price'] = ''

        for model in Watches.models:
            if model in watch[:Parser.get_price_index(watch)]:
                res_dict['model'] = model
                watch = watch.replace(model, '', 1)
                break
        else:
            raise ParseException('ошибка в парсинге модели')

        for size in Watches.sizes:
            if size in watch[:Parser.get_price_index(watch)]:
                res_dict['size'] = size
                watch = watch.replace(size, '')
                break
        else:
            raise ParseException('ошибка в парсинге размера')

        for strap_size in Watches.strap_sizes:
            if strap_size in watch[:Parser.get_price_index(watch)]:
                res_dict['strap_size'] = strap_size
                watch = watch.replace(strap_size, '')
                if 'alpine loop' in watch:
                    res_dict['strap_size'] = 'alpine loop ' + res_dict['strap_size']
                break
        else:
            raise ParseException('ошибка в парсинге размера ремешка')

        for color in Watches.colors:
            if color in watch[:Parser.get_price_index(watch)]:
                res_dict['color'] = color
                watch = watch.replace(color, '')
                break

        else:
            raise ParseException('ошибка в парсинге цвета')

        for year in Watches.year:
            if year in watch[:Parser.get_price_index(watch)]:
                res_dict['year'] = year
                watch = watch.replace(year, '')
                break

        for symb in watch[Parser.get_price_index(watch):]:
            if symb.isdigit():
                res_dict['price'] = res_dict['price'] + symb

        return res_dict

    @staticmethod
    def parse_airpods(airpod: str) -> dict:
        airpod = airpod.replace('max', 'pro').lower()
        res_dict = dict()
        res_dict['price'] = ''

        for model in Airpods.models:
            if (model != '2' or model != '3') and model in airpod[:Parser.get_price_index(airpod)] \
                    or Parser.len_model_el(airpod, model) == 1:
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
            if case in airpod[:Parser.get_price_index(airpod)]:
                res_dict['case'] = case
                break
        airpod = re.sub(r'(\d)\s+(\d)', r'\1\2', airpod)
        airpod = airpod.replace("  ", " ").replace("-", " ").replace(".", "").replace(",", "").split()
        res_dict["price"] = ""
        buff = ''
        if len(airpod) == 1:
            try:
                for el in airpod[0]:
                    if el.isdigit():
                        res_dict["price"] += el
                res_dict["country"] = airpod[0].replace(item_patterns.delete_flag(airpod[0]), '')
            except IndexError:
                return {"exception": "IndexError"}
        else:
            try:
                for i in airpod:
                    for el in i:
                        if el.isdigit():
                            buff += el
                    if buff.isdigit() and int(buff) > 1000:
                        res_dict['price'] = buff
                    buff = ''

            except IndexError:
                return {"exception": "indexError"}

        return res_dict
    @staticmethod
    def parse_macbooks(macbook: str) -> dict:
        macbook = macbook.lower().replace('2022', '').replace('2023', '')
        res_dict = dict()
        res_dict['price'] = ''

        for model in Macbooks.models:
            if model in macbook[:Parser.get_price_index(macbook)] and Parser.len_model_el(macbook, model) == 2:
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
                res_dict['storage'] = int(storage.replace('тб', '').replace('tb', '').replace('gb', '').replace('гб', ''))
                macbook = macbook.replace(storage, '')
                break
        else:
            raise ParseException('ошибка в парсинге хранилища')

        price_index = Parser.get_price_index(macbook)
        for symb in macbook[price_index:]:
            if symb.isdigit():
                res_dict['price'] = res_dict['price'] + symb

        return res_dict

    @staticmethod
    def parse_ipads(ipad: str) -> dict:
        ipad = ipad.lower().replace('109', '10').replace('5th', '5').replace('cellular', 'lte')
        res_dict = dict()
        res_dict['price'] = ''
        for model in Ipads.models:
            if model + ' ' in ipad[:Parser.get_price_index(ipad)]:
                res_dict['model'] = model
                ipad = ipad.replace(model, '', 1)
                break

        else:
            raise ParseException('ошибка в парсинге модели')

        for storage in Ipads.storages:
            if storage in ipad:
                res_dict['storage'] = int(storage.replace('тб', '').replace('tb', '').replace('gb', '').replace('гб', ''))
                ipad = ipad.replace(storage, '')
                break
        else:
            raise ParseException('ошибка в парсинге хранилища')

        for color in Ipads.COLORS:
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

        price_index = Parser.get_price_index(ipad)
        for symb in ipad[price_index:]:
            if symb.isdigit():
                res_dict['price'] = res_dict['price'] + symb

        return res_dict

    @staticmethod
    def parse_playstation(position):
        pass

    @staticmethod
    def parse_router(position):
        """

        :param str position: Строка для парсинга товара
        :return dict, str: В словаре будут все данные + название товара
        """
        try:
            if Parser.is_macbook(position):
                return Parser.parse_macbooks(position), 'macbook'

            elif 'iphone' in position.lower():
                return Parser.parse_phones(position), 'phone'

            elif Parser.is_ipad(position):
                return Parser.parse_ipads(position), 'ipad'

            elif Parser.is_airpod(position):
                return Parser.parse_airpods(position), 'airpod'

            elif Parser.is_watch(position):
                return Parser.parse_watches(position), 'watch'

            # Телефоны идут в else, так как я не смог придумать для них нормальную проверку. Но и так должно работать
            # нормально, так как для них создан очень чувствительный парсер
            else:
                return Parser.parse_phones(position), 'phone'

        except ParseException:
            return f'Ошибка в парсинге: {position}'


    @staticmethod
    def is_watch(data: str) -> bool:
        data = data.lower()
        for model in Watches.models:
            for size in Watches.sizes:
                if ((model in data[:Parser.get_price_index(data)] and size in data[:Parser.get_price_index(data)])
                        or 'watch' in data or 'aw' in data or 'apple' in data):
                    return True
        return False

    @staticmethod
    def is_airpod(data: str) -> bool:
        data = data.lower()
        for model in Airpods.models:
            for case in Airpods.cases:
                if ('airpods' in data) or (model in data.split() and case in data):
                    return True
        return False

    @staticmethod
    def is_macbook(data: str) -> bool:
        data = data.lower()
        for serial_number in Macbooks.serial_numbers:
            if serial_number in data:
                return True
        for model in Macbooks.models:
            for cpu in Macbooks.cpus:
                if (model in data and cpu in data) or \
                        ('mb' in data or 'macbook' in data or 'mac book' in data):
                    return True
        return False

    @staticmethod
    def is_ipad(data: str) -> bool:
        data = data.lower()
        for model in Ipads.models:
            for network in Ipads.networks:
                if ('ipad' in data) or (network in data and \
                                        ((not model.isdigit()) and model in data)):
                    return True
        return False

    @staticmethod
    def is_playstation(data: str) -> bool:
        pass
