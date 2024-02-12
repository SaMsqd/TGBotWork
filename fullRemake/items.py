priorities = {
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

        self.size = size
        self.color = color
        self.strap_size = strap_size
        self.year = year

        self.model_priority = 0
        self.size_priority = 0,
        self.strap_size_priority = 0

    def generate_str(self):
        return (f'{self.model} {self.year} {self.size} {self.strap_size} '
                f'{self.color} - {self.price}')

    def generate_sql(self, table_name):
        return (f'INSERT INTO {table_name} VALUES ({self.model}, {self.model_priority}, '
                f'{self.size}, {self.size_priority}, {self.color}, {self.strap_size}, '
                f'{self.strap_size_priority}, {self.year}, {self.price})')


class Airpod(Item):
    def __init__(self, model, case, year, price):

        self.var_checker({
            case: str,
            year: int
        })

        super().__init__(model, price)
        self.case = case
        self.year = year

        self.model_priority = 0
        self.case_priority = 0

    def generate_str(self):
        return f'{self.model} {self. year} {self.case} - {self.price}'

    def generate_sql(self, table_name):
        return (f'INSERT INTO {table_name} VALUES({self.model}, {self.model_priority}, '
                f'{self.case}, {self.case_priority}, {self.year}, {self.price})')


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

        self.model_priority = 0
        self.cpu_priority = 0
        self.storage_priority = priorities['storage'][str(storage)]

    def generate_str(self):
        return f'{self.model} {self.cpu} {self.storage} {self.color} - {self.price}'

    def generate_sql(self, table_name):
        return (f'INSERT INTO {table_name} VALUES ({self.model}, {self.model_priority}, '
                f'{self.cpu}, {self.cpu_priority}, {self.color}, {self.storage}, '
                f'{self.storage_priority}, {self.price})')


class Phone(Item):
    def __init__(self, model, version, color, storage, country, price):

        self.var_checker({
            version: str,
            color: str,
            storage: int,
            country: str
        })

        super().__init__(model, price)
        self. version = version
        self.color = color
        self.storage = storage
        self.country = country

        self.model_priority = 0
        self.version_priority = 0
        self.storage_priority = priorities['storage'][str(storage)]

    def generate_str(self):
        return (f'{self.model} {self.version} {self.storage} {self.color} '
                f'- {self.price}{self.country}')

    def generate_sql(self, table_name):
        return (f'INSERT INTO {table_name} VALUES ({self.model}, {self.model_priority}, {self.version}, '
                f'{self.version_priority}, {self.color}, {self.storage}, {self.storage_priority}, '
                f'{self.country}, {self.price})')


class Ipad(Item):
    def __init__(self, model: str, storage: int, color: str, network: str, price: int):

        self.var_checker({
            storage: int,
            color: str,
            network: str,
        })

        super().__init__(model, price)
        self.storage = storage
        self.color = color
        self.network = network

        self.model_priority = 0
        self.storage_priority = priorities['storage'][str(storage)]
        self.network_priority = 0

    def generate_str(self):
        return f'{self.model} {self.storage} {self.network} {self.color} - {self.price}'

    def generate_sql(self, table_name):
        return (f'INSERT INTO {table_name} VALUES({self.model}, {self.model_priority}, {self.network}, '
                f'{self.network_priority}, {self.color}, {self.storage}, '
                f'{self.storage_priority}, {self.price})')
