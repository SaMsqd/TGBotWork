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
        self.var_checker({model: int,
                          price: int})
        self.model: int = model
        self.price: int = price

    @staticmethod
    def var_checker(d) -> None:
        """
        Проверяет типы переменных
        :param dict d: словарь: переменная: какой должен быть тип
        :return:
        :raise TypeError
        """
        # for pair in list(d.items())[0]:
        #     print(pair)
        #     if not isinstance(pair[0], pair[1]):
        #
        #         name = f'{pair[0]=}'.split('=')[0]
        #         raise TypeError(f'переменная {name} должна быть типа {pair[1]}')
        pass

    def generate_str(self):
        """
        Генерирует строку для принта

        :param все данные объединяем в одну строку начиная с модели и кончая ценой(цена через -)
        :return: str
        """
        pass

    def generate_sql(self):
        """
        Генерирует значения, которые нужно вставить после ключевго sql-слова values
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



    def generate_str(self):
        return (f'{self.model} {self.year} {self.size} {self.strap_size} '
                f'{self.color} - {make_price_beautiful(self.price)}')

    def generate_opt(self):
        return (f'{self.model} {self.year} {self.size} {self.strap_size} '
                f'{self.color} - {make_price_beautiful(self.price + 500)}')

    def generate_retail(self):
        return (f'{self.model} {self.year} {self.size} {self.strap_size} '
                f'{self.color} - {make_price_beautiful(self.price + 500)} ↔️ {make_price_beautiful(self.price + 1000)}')

    def generate_sql(self):
        return (f'("{self.model}","{self.size}", "{self.color}", "{self.strap_size}", {self.year}, {self.price})')


class Airpod(Item):
    def __init__(self, model, case, year, price):

        self.var_checker({
            case: str,
            year: int
        })

        super().__init__(model, price)
        self.case = case
        self.year = year

    def generate_str(self):
        return f'{self.model} {self. year} {self.case} - {make_price_beautiful(self.price)}'

    def generate_opt(self):
        return f'{self.model} {self. year} {self.case} - {make_price_beautiful(self.price + 500)}'

    def generate_retail(self):
        return (f'{self.model} {self.year} {self.case} - {make_price_beautiful(self.price + 500)} '
                f'↔️ {make_price_beautiful(self.price + 1000)}')

    def generate_sql(self):
        return (f'("{self.model}","{self.case}", {self.year}, {self.price})')


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

    def generate_str(self):
        return f'{self.model} {self.cpu} {self.storage} {self.color} - {make_price_beautiful(self.price)}'

    def generate_opt(self):
        return f'{self.model} {self.cpu} {self.storage} {self.color} - {make_price_beautiful(self.price + 500)}'

    def generate_retail(self):
        return (f'{self.model} {self.cpu} {self.storage} {self.color} - {make_price_beautiful(self.price + 500)} '
                f'↔️ {make_price_beautiful(self.price + 1000)}')

    def generate_sql(self):
        return (f'("{self.model}","{self.cpu}", "{self.color}", {self.storage},{self.price})')


class Phone(Item):
    def __init__(self, model, version, color, storage, country, price):

        self.var_checker({
            version: str,
            color: str,
            storage: int,
            country: str
        })

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
        return (f'{self.model} {self.version} {self.color} {self.storage} {self.country} '
                f'- {make_price_beautiful(self.price)}')

    def generate_opt(self):
        return (f'{self.model} {self.version} {self.color} {self.storage} {self.country} '
                f'- {make_price_beautiful(self.price + 500)}')

    def generate_retail(self):
        return (f'{self.model} {self.version} {self.color} {self.storage} {self.country} '
                f'- {make_price_beautiful(self.price + 500)} ↔️ {make_price_beautiful(self.price + 1000)}')

    def generate_sql(self):
        return (f'({self.model}, "{self.version}", '
                f' "{self.color}", {self.storage}, '
                f'"{self.country}", "{self.market}" , {self.price})')


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


    def generate_str(self):
        return f'{self.model} {self.storage} {self.network} {self.color} - {make_price_beautiful(self.price)}'

    def generate_opt(self):
        return f'{self.model} {self.storage} {self.network} {self.color} - {make_price_beautiful(self.price + 500)}'

    def generate_retail(self):
        return (f'{self.model} {self.storage} {self.network} {self.color} - {make_price_beautiful(self.price + 500)}'
         f'↔️ {make_price_beautiful(self.price + 1000)}')

    def generate_sql(self):
        return (f'("{self.model}", "{self.storage}", '
                f' "{self.color}", "{self.network}", '
                f' {self.price})')


class Playstation:
    def __init__(self, type, name, price):
        self.type = type
        self.name = name
        self.price = price

