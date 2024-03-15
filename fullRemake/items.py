priorities_phone = {
    'storage':
        {
            "64": 0,
            "128": 1,
            "256": 2,
            "512": 3,
            "1": 4,
            "1024": 4,
            "2": 5,
            "2048": 5
        },
    'model':
        {
            "se3": 0,
            "11": 1,
            "12": 2,
            "13": 3,
            "14": 4,
            "15": 5,
            "16": 6,
        },
    'version':
        {
            '': 0,
            'Mini': 1,
            'Pro': 2,
            'Max':3,
            'Pro max': 4,
            'Plus': 5
        }
}

priorities_ipad = {
    'networks':
        {
            'wifi': 1,
            'wi fi': 1,
            'wi-fi': 1,
            'lte': 2
        },
    'model':
        {
            'mini 6': 1,
            'mini 7': 2,
            '5': 3,
            'air 5': 4,
            '9': 5,
            '10': 6,
            'pro 11': 7,
            'pro 12': 8
        },
    'storage':
        {
            "64": 0,
            "128": 1,
            "256": 2,
            "512": 3,
            "1": 4,
            "1024": 4,
            "2": 5,
            "2048": 5
        }
}

priorities_macbook = {
    'model':
        {
            '13': 1,
            '14': 2,
            'pro 14': 2,
            'air 14': 2,
            '15': 3,
            'air 15': 3,
            'pro 15': 3,
            '16': 4,
            'pro 16': 4,
            'air 16': 4,
        },
    'cpu':
        {
            'm1': 1,
            'm2': 2,
            'm3': 3,
        },
    'storage':
        {
            "64": 0,
            "128": 1,
            "256": 2,
            "512": 3,
            "1": 4,
            "1024": 4,
            "2": 5,
            "2048": 5
        }
}

priorities_watch = {
    'model':
        {
            'se': 1,
            's8': 2,
            's9': 3,
            'series 9': 4,
            '9' : 4,
            'ultra': 5,
            'ultra 2': 6
        },
    'size':
        {
            '40': 1,
            '41': 2,
            '44': 3,
            '45': 4,
            '49': 5
        },
    'strap_size':
        {
            's/m': 1,
            'sm': 1,
            's': 2,
            'm/l': 3,
            'ml': 3,
            'sport loop': 4
        },
    'year':
        {
            '2020': 1,
            '2021': 2,
            '2022': 3,
            '2023': 4,
            '2024': 4,
            '2025': 5,
        }
}

priorities_airpods = {
    'model':
        {
            'pro 2 lightning': 1,
            '2022': 1,
            'max': 2,
            'pro': 2,
            'pro 2': 3,
            '2': 3,
            '3': 4,
            'pro 2 type c': 5,
            '2023': 5
        },
    'year':
        {
            '10': 9999,
            '2018': 1,
            '2019': 2,
            '2020': 3,
            '2021': 4,
            '2022': 5,
            '2023': 6,
            '2024': 7,
        }
}

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


class Item:
    def __init__(self, model: str, price: int) -> None:

        """
        Запоминает все данные, расставляет приоритеты
        :param model: str, название модели
        :param price: int, цена товара
        :return None
        :raise TypeError
        """
        self.var_checker({model: str,
                          price: int})
        self.model: str = model
        self.price: int = price

    @staticmethod
    def var_checker(d) -> None:
        """
        Проверяет типы переменных
        :param dict d: словарь: переменная: какой должен быть тип
        :return:
        :raise TypeError
        """
        pass

    def generate_str(self):
        """
        Генерирует строку для принта

        :param все данные объединяем в одну строку начиная с модели и кончая ценой(цена через -)
        :return: str
        """
        pass

    def generate_sql(self, table_name):
        """
        Генерирует строку-команду SQL, которую просто нужно будет выполнить, чтобы добавить устройства в БД
        :param str table_name: название таблицы
        :return: str
        """


class Watch(Item):
    def __init__(self, model, size, color, strap_size, year, price):
        self.var_checker({
            size: str,
            color: str,
            strap_size: str,
            year: int
        })
        super().__init__(model, price)

        self.priority = int(str(priorities_watch['model'][model]) + str(priorities_watch['size'][size]) + str(priorities_watch['strap_size'][strap_size]) + str(priorities_watch['year'][str(year)]))

        self.size = size
        self.color = color
        self.strap_size = strap_size
        self.year = year


    def generate_str(self):
        return (f'{self.model} {self.year} {self.size} {self.strap_size} '
                f'{self.color} - {self.price}')

    def generate_sql(self):
        return f'("{self.model}","{self.size}", "{self.color}", "{self.strap_size}", {self.year}, {self.price})'

    def generate_opt(self):
        return (f'{self.model} {self.year} {self.size} {self.strap_size} '
                f'{self.color} - {make_price_beautiful(self.price + 500)}')

    def generate_opt(self):
        return (f'{self.model} {self.year} {self.size} {self.strap_size} '
                f'{self.color} - {make_price_beautiful(self.price + 1000)}')

    def generate_retail(self):
        return (f'{self.model} {self.year} {self.size} {self.strap_size} '
                f'{self.color} - {make_price_beautiful(self.price + 500)} ↔️ {make_price_beautiful(self.price + 1000)}')


class Airpod(Item):
    def __init__(self, model, case, year, color, price):

        self.var_checker({
            case: str,
            year: int
        })

        self.priority = int(str(priorities_airpods['model'][str(model)]) + str(priorities_airpods['year'][str(year)]))

        super().__init__(model, price)
        self.color = color
        self.case = case
        self.year = year

    def generate_str(self):
        return f'{self.model} {self.year} {self.case} {self.color} - {self.price}'

    def generate_opt(self):
        return f'{self.model} {self. year} {self.case} {self.color} - {make_price_beautiful(self.price + 500)}'

    def generate_1000(self):
        return f'{self.model} {self. year} {self.case} {self.color} - {make_price_beautiful(self.price + 1000)}'

    def generate_retail(self):
        if self.color == '10':
            return (f'{self.model} {self.year} {self.case} - {make_price_beautiful(self.price + 500)} '
                    f'↔️ {make_price_beautiful(self.price + 1000)}')
        return (f'{self.model} {self.year} {self.case} {self.color} - {make_price_beautiful(self.price + 500)} '
                    f'↔️ {make_price_beautiful(self.price + 1000)}')

    def generate_sql(self):
        return (f'("{self.model}","{self.case}", {self.year}, "{self.color}", {self.price})')


class Macbook(Item):
    def __init__(self, model, cpu, color, storage, price):
        self.var_checker({
            cpu: str,
            color: str,
            storage: int
        })

        super().__init__(model, price)
        self.cpu = cpu
        self.color = color
        self.storage = storage

        self.priority = int(str(priorities_macbook['model'][model]) + str(priorities_macbook['cpu'][cpu]) + str(priorities_macbook['storage'][str(storage)]))

    def generate_str(self):
        return f'{self.model} {self.cpu} {self.storage} {self.color} - {self.price}'

    def generate_opt(self):
        return f'{self.model} {self.cpu} {self.storage} {self.color} - {make_price_beautiful(self.price + 500)}'

    def generate_1000(self):
        return f'{self.model} {self.cpu} {self.storage} {self.color} - {make_price_beautiful(self.price + 1000)}'

    def generate_retail(self):
        return (f'{self.model} {self.cpu} {self.storage} {self.color} - {make_price_beautiful(self.price + 500)} '
                f'↔️ {make_price_beautiful(self.price + 1000)}')


    def generate_sql(self):
        return f'("{self.model}","{self.cpu}", "{self.color}", {self.storage},{self.price})'


class Phone(Item):
    def __init__(self, model, version, color, storage, country, price):

        self.var_checker({
            version: str,
            color: str,
            storage: int,
            country: str
        })

        self.priority = int(str(priorities_phone['model'][model]) + str(priorities_phone['version'][version]) + str(priorities_phone['storage'][str(storage)]))

        super().__init__(model, price)
        self.version = version
        self.color = color
        self.storage = storage
        self.country = country

        if int(self.model) >= 14 and self.country == '🇺🇸':
            self.market = 'us'
        elif self.country == '🇨🇳'or self.country == '🇭🇰':
            self.market = 'cn'
        else:
            self.market = 'others'

    def generate_str(self):
        return (f'{self.model} {self.version} {self.color} {self.storage} '
                f'- {self.country}{self.price}')

    def generate_opt(self):
        return (f'{self.model} {self.version} {self.color} {self.storage} {self.country} '
                f'- {make_price_beautiful(self.price + 500)}')

    def generate_1000(self):
        return (f'{self.model} {self.version} {self.color} {self.storage} {self.country} '
                f'- {make_price_beautiful(self.price + 1000)}')

    def generate_retail(self):
        return (f'{self.model} {self.version} {self.color} {self.storage} {self.country} '
                f'- {make_price_beautiful(self.price + 500)} ↔️ {make_price_beautiful(self.price + 1000)}')

    def generate_sql(self):
        return (f'("{self.model}", "{self.version}", '
                f' "{self.color}", {self.storage}, '
                f'"{self.country}", "{self.market}" , {self.price})')


class Ipad(Item):
    def __init__(self, model: str, storage: int, color: str, network: str, price: int):

        self.var_checker({
            storage: int,
            color: str,
            network: str,
        })

        self.priority = int(str(priorities_ipad['networks'][network]) + str(priorities_ipad['model'][model]) + str(priorities_ipad['storage'][str(storage)]))

        super().__init__(model, price)
        self.storage = storage
        self.color = color
        self.network = network


    def generate_str(self):
        return f'{self.model} {self.storage} {self.network} {self.color} - {self.price}'

    def generate_opt(self):
        return f'{self.model} {self.storage} {self.network} {self.color} - {make_price_beautiful(self.price + 500)}'

    def generate_1000(self):
        return f'{self.model} {self.storage} {self.network} {self.color} - {make_price_beautiful(self.price + 1000)}'

    def generate_retail(self):
        return (f'{self.model} {self.storage} {self.network} {self.color} - {make_price_beautiful(self.price + 500)}'
         f'↔️ {make_price_beautiful(self.price + 1000)}')

    def generate_sql(self):
        return (f'("{self.model}", {self.storage}, '
                f' "{self.color}", "{self.network}", '
                f' {self.price})')
