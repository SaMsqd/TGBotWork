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
            "13": 1,
            "14": 2
        },
    'version':
        {
            'Pro': 1
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
            'mini 7': 2
        },
    'storage':
        {
            '64': 1
        }
}

priorities_macbook = {
    'model':
        {
            '13': 1
        },
    'cpu':
        {
            'm1':1
        },
    'storage':
        {
            '256':1
        }
}

priorities_watch = {
    'model':
        {
            'hz': 1
        },
    'size':
        {
            'hz': 1
        },
    'strap_size':
        {
            'hz': 1
        },
    'year':
        {
            'hz': 1
        }
}

priorities_airpods = {
    'model':
        {
            'hz': 1
        },
    'year':
        {
            'hz': 1
        }
}


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
        for k, v in d.items():
            if not isinstance(k, v):
                name = f'{k=}'.split('=')[0]
                raise TypeError(f'переменная {name} должна быть типа {v}')

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

        self.priority = int(str(priorities_watch['model'][model]) + str(priorities_watch['size'][size]) + str(priorities_watch['strap_size'][strap_size]) + str(priorities_watch['year'][year]))

        self.size = size
        self.color = color
        self.strap_size = strap_size
        self.year = year



    def generate_str(self):
        return (f'{self.model} {self.year} {self.size} {self.strap_size} '
                f'{self.color} - {self.price}')

    def generate_sql(self):
        return (f'({self.model},"{self.size}", "{self.color}", "{self.strap_size}", {self.year}, {self.price})')


class Airpod(Item):
    def __init__(self, model, case, year, price):

        self.var_checker({
            case: str,
            year: int
        })

        self.priority = int(str(priorities_airpods['model'][model]) + str(priorities_airpods['year'][year]))

        super().__init__(model, price)
        self.case = case
        self.year = year

    def generate_str(self):
        return f'{self.model} {self. year} {self.case} - {self.price}'

    def generate_sql(self):
        return (f'({self.model},"{self.case}", {self.year}, {self.price})')


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

    def generate_sql(self):
        return (f'({self.model},"{self.cpu}", "{self.color}", {self.storage},{self.price})')


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

    def generate_sql(self):
        return (f'("{self.model}", {self.storage}, '
                f' "{self.color}", "{self.network}", '
                f' {self.price})')