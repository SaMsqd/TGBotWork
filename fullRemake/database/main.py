# Для каждого пользователя создавать свою бд и делать все товары в одной бд, но в разных таблицах
# Создать метод для иннициации бд и создания таблиц
import sqlite3
from fullRemake.items import Item


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(f'/files/{db_name}.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        pass

    def add_item(self, item):
        """
        Метод для добавления товаров
        :param Item | str item: предмет для добавления (либо объект, наследующий Item, либо sql строка)
        :return:
        """
        pass

    def get_sorted_items(self):
        pass

    def get_all(self):
        pass

    def convert_in_item(self):
        pass

    def sort_items(self):
        pass
