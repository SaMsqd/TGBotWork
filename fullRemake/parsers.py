from exceptions import ParseException
import item_patterns
from item_patterns import *
import re


class Parser:
    @staticmethod
    def change_price_view(data: str):
        """Функция, которая убирает пробел между разрядами в цене: ... - 11 111 -> 11111"""
        try:
            res = ''
            el = data[Parser.get_price_index(data)-1]
            if el != ' ':
                return data
            counter = 0
            while el.isdigit() or el == ' ' and counter == 0:
                if el != ' ':
                    res += el
                counter += 1
                el = data[Parser.get_price_index(data)-counter]
            if el == ' ' and counter == 1:
                return data
            return data[:Parser.get_price_index(data)-counter] + res[::-1] + data[Parser.get_price_index(data):]
        except Exception:
            return data

    @staticmethod
    def change_parametres(data):
        data = {k: str(v).lower() for k, v in data.items()}
        """Функция, которая будет менять одинаковые цвета, модели и тд"""
        # Цвета
        if data['color'] in ['grey', 'gray', 'space gray', 'space grey', 'space']:
            data['color'] = 'Space Gray'

        if data.get('color', None) and (data['color'] in ["blue", "bluе"]):
            data['color'] = 'Blue'

        # airpods
        if data.get('model', None) and (data['model'] in ['pro 2 lightning', '2022']):
            data['model'] = 'pro 2 lightning'

        if data.get('model', None) and (data['model'] in ['pro 2 type c', '2023']):
            data['model'] = 'pro 2 type c'

        # Apple Watch
        if data.get('strap_size', None) and (data['strap_size'] in ['sm', 'ml']):
            data['strap_size'] = data['strap_size'][0] + '/' + data['strap_size'][1]

        # ipads
        if data.get('network', None) and (data['network'] in ['wi-fi', 'wifi', 'wi fi']):
            data['network'] = 'wi-fi'

        for k, v in data.items():
            if type(v) is str:
                data[k] = v.capitalize()
        return data

    @staticmethod
    def get_data_from_string(phone_data: str):
        res_dict = dict()
        phone_data = phone_data
        phone_data = phone_data.lower().replace("-", " ").replace('iphone', '').replace('apple', '')
        price_index = Parser.get_price_index(phone_data)

        for STORAGE in Phones.STORAGE:
            if STORAGE in phone_data[0: price_index]:
                if STORAGE == "1tb" or STORAGE == "1" or STORAGE == '1 tb':
                    res_dict["storage"] = STORAGE.upper()
                    phone_data = phone_data.replace(STORAGE, "", 1)
                    break
                else:
                    res_dict["storage"] = STORAGE + "GB"
                    phone_data = phone_data.replace(STORAGE, "", 1)
                break

        price_index = Parser.get_price_index(phone_data)

        for NAME in Phones.MODELS:
            if NAME in phone_data.lower()[: price_index]:
                res_dict["model"] = NAME.capitalize()
                phone_data = phone_data.replace(NAME, "", 1)
                break

        for COLOR in COLORS:
            if COLOR in phone_data.lower():
                res_dict["color"] = COLOR.capitalize()
                phone_data = phone_data.replace(COLOR, "")
                break
        phone_data = phone_data.strip()

        for VERSION in Phones.VERSIONS:
            if VERSION in phone_data[:Parser.get_price_index(phone_data)]:
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

                    if res_dict['country'] == '':
                        phone_data = ' '.join(phone_data)
                        res_dict['country'] = phone_data.replace(Parser.delete_flag(phone_data), '')
                    buff = ''

            except IndexError:
                return {"exception": "IndexError"}
        else:
            try:
                for i in phone_data:
                    for el in i:
                        if el.isdigit():
                            res_dict["price"] += el

                    if i.lower() in Phones.COUNTRIES[0]:
                        res_dict["country"] = i
            except IndexError:
                return {"exception": "indexError"}
        return res_dict

    @staticmethod
    def delete_flag(data: str) -> str:
        for el in Phones.COUNTRIES[0][:-7]:
            data = data.replace(el, "")
        return data.replace(' ', '')

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
            data["storage"] = data["storage"].replace("тбGB", "TB").replace("GB", "").replace("TB", "").replace(' tb', '')
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
                res_dict['model'] = model.capitalize()
                if model.lower() == 'se':
                    res_dict['model'] = model.upper()
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
                res_dict['strap_size'] = strap_size.capitalize()
                watch = watch.replace(strap_size, '')
                if 'alpine loop' in watch:
                    res_dict['strap_size'] = 'alpine loop' + res_dict['strap_size']
                break
        else:
            raise ParseException('ошибка в парсинге размера ремешка')

        for color in Watches.colors:
            if color in watch[:Parser.get_price_index(watch)]:
                res_dict['color'] = color.capitalize()
                watch = watch.replace(color, '')
                break

        else:
            raise ParseException('ошибка в парсинге цвета')

        for year in Watches.year:
            if year in watch[:Parser.get_price_index(watch)]:
                res_dict['year'] = year
                watch = watch.replace(year, '')
                break

        for symb in watch[Parser.get_price_index(watch)-3:]:
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
                res_dict['model'] = model.capitalize()
                airpod = airpod.replace(model, '', 1)
                break
        else:
            raise ParseException('ошибка в парсинге модели')

        for color in COLORS:
            if color in airpod:
                res_dict['color'] = color.capitalize()
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
                res_dict['case'] = case.capitalize()
                break

        if res_dict.get('case', None):
            res_dict['case'] = 'lightning'

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
            if res_dict['price'] == '':
                return {'exception': 'priceError'}
        return res_dict

    @staticmethod
    def _recreate_string(macbook):
        l = macbook.split('-')
        if len(l) == 3:
            for k, v in item_patterns.Macbooks.serial_numbers.items():
                if Parser.delete_flag(l[0].lower()) in v:
                    return k + l[2].replace('pro', '').replace('air', '').replace('max', '') + '-' + l[1]
        if len(l) > 3:
            for k, v in item_patterns.Macbooks.serial_numbers.items():
                if Parser.delete_flag(l[0]).lower() in v and l[1].replace(' ', '').isdigit():
                    return k + ' ' + ''.join([x.replace('pro', '').replace('air', '').replace('max', '') for x in l[2:]]) + '-' + l[1]
        return macbook

    @staticmethod
    def parse_macbooks(macbook: str) -> dict:
        macbook = macbook.lower().replace('2022', '').replace('2023', '')
        macbook = Parser._recreate_string(macbook)
        res_dict = dict()
        res_dict['price'] = ''

        for model in Macbooks.models:
            if model in macbook[:Parser.get_price_index(macbook)]   :
                if 'pro' in macbook:
                    res_dict['model'] = 'Pro ' + model
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
                res_dict['color'] = color.capitalize()
                macbook = macbook.replace(color, '')
                break
        else:
            raise ParseException('ошибка в парсинге цвета')

        for cpu in Macbooks.cpus:
            if cpu in macbook:
                res_dict['cpu'] = cpu.capitalize()
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
        for symb in macbook[price_index-3   :]:
            if symb.isdigit():
                res_dict['price'] = res_dict['price'] + symb

        return res_dict

    @staticmethod
    def parse_ipads(ipad: str) -> dict:
        ipad = ipad.lower().replace('109', '10').replace('5th', '5').replace('cellular', 'lte').replace('2022', '10').replace('(', ' ').replace(')', ' ')

        res_dict = dict()
        res_dict['price'] = ''
        for model in Ipads.models:
            if model + ' ' in ipad[:Parser.get_price_index(ipad)]:
                res_dict['model'] = model.capitalize()
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
                res_dict['color'] = color.capitalize()
                ipad = ipad.replace(storage, '')
                break
        else:
            raise ParseException('ошибка в парсинге цвета')

        for network in Ipads.networks:
            if network in ipad:
                if network in ['wifi', 'wi-fi', 'wi fi']:
                    res_dict['network'] = 'WIFI'
                    ipad = ipad.replace(network, '')
                    break
                res_dict['network'] = network.upper()
                ipad = ipad.replace(network, '')
                break
        else:
            raise ParseException('ошибка в парсинге поддреживаемой сети')

        price_index = Parser.get_price_index(ipad)
        for symb in ipad[price_index-4:]:
            if symb.isdigit():
                res_dict['price'] = res_dict['price'] + symb
        if int(res_dict['price']) > 10**6 and '10' in str(res_dict['price'])[:5]:
            res_dict['price'] = int(str(res_dict['price'].replace('10', '')))
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
        position = Parser.change_price_view(position)
        try:
            if Parser.is_airpod(position):
                return Parser.parse_airpods(position), 'airpod'

            elif 'iphone' in position.lower():
                return Parser.parse_phones(position), 'phone'

            elif Parser.is_ipad(position):
                return Parser.parse_ipads(position), 'ipad'

            elif Parser.is_watch(position):
                return Parser.parse_watches(position), 'watch'

            elif Parser.is_macbook(position):
                return Parser.parse_macbooks(position), 'macbook'

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
        for k, v in item_patterns.Macbooks.serial_numbers.items():
            for serial_number in v:
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

if __name__ == '__main__':
    print(Parser.change_price_view('asdklzxcjclh qwn lsodhfoz - 12 345'))
