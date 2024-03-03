import sqlite3

from fullRemake.items import Item
from fullRemake.items import Phone
from fullRemake.items import Ipad
from fullRemake.items import Airpod
from fullRemake.items import Macbook
from fullRemake.items import Watch

import os
from os import listdir



class Database:
    def __init__(self, user_id):
        self.name = user_id
        self.connection = sqlite3.connect(f'./database/files/{user_id}.db'.replace('idid', 'id'))
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS Phones(model int , version str ,\
        color str , storage int , country str , market str , price int)')

        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS Watches(model int , size str ,\
        color str , strap_size str , year int , price int)')

        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS Airpods(model str, cas str ,\
        year int , price int)')

        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS Macbooks(model str , cpu str ,\
        color str , storage int , price int)')

        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS Ipads(model str , network str ,\
         color str , storage int, price int)')

        self.cursor.execute('CREATE TABLE IF NOT EXISTS Playstations(type str, name str, price int)')

        self.connection.commit()

    def add_items(self, items, item_name):
        """
        Метод для добавления товаров
        :param list[Item] items: предмет для добавления (либо объект, наследующий Item, либо sql строка)
        :param str item_name: название таблицы, в которую нужно добавить предмет
        :return:
        """
        if len(items) == 0:
            return
        string_items = items[0].generate_sql()
        for i in range(len(items)-1):
            string_items += ',' + items[i+1].generate_sql()
        print(string_items)
        self.cursor.execute(f'insert into {item_name} values{string_items}')
        self.connection.commit()


    def get_sorted_items(self):
        """
        Функция, которая возвращает ВСЕ отсортированные предметы
        :return: list(Item)
        """
        f = self._get_sorted_items
        l = list()
        return {'phones': f('Phones'), 'watches': f('Watches'), 'airpods': f('Airpods'), 'macbooks': f('Macbooks'),
                'ipads': f('Ipads')}

    def _get_sorted_items(self, items_name):
        """
        Функция, которая возвращает отсортированный список одного предмета
        :param str items_name: предмет, который нужно отсортировать
        :return: list[Item]
        """
        all_items = self.get_all(items_name)
        all_items_sorted = {}
        for item in all_items:
            if item[0] in all_items_sorted:
                if item[1].price < all_items_sorted[item[0]].price:
                    all_items_sorted[item[0]] = item[1]
            else:
                all_items_sorted[item[0]] = item[1]
        return list(all_items_sorted.values())

    def get_all(self,items_name):
        """
        :param str items_name: предметы, который нужно получить и конвертировать в item
        :return: list[Item]
        """
        self.cursor.execute(f'select * from {items_name}')
        all_items = self.cursor.fetchall()
        k = 0
        for item in all_items:
            if items_name == 'Phones':
                all_items[k] = [str(item[0]) + str(item[1]) +  str(item[2]) + str(item[3]) + str(item[5]),\
                                Phone(int(item[0]), str(item[1]), item[2], int(item[3]),item[4], item[6])]
            elif items_name == 'Ipads':
                all_items[k] = [str(item[0]) + str(item[1]) + str(item[2]) + str(item[3]), \
                                Ipad(str(item[0]), int(item[1]), str(item[2]), str(item[3]), int(item[4]))]
            elif items_name == 'Airpods':
                all_items[k] = [str(item[0]) + str(item[1]) + str(item[2]), \
                                Airpod(int(item[0]), str(item[1]), int(item[2]), int(item[3]))]
            elif items_name == 'Macbooks':
                all_items[k] = [str(item[0]) + str(item[1]) + str(item[2]) + str(item[3]), \
                                Macbook(str(item[0]), str(item[1]), str(item[2]), int(item[3]), int(item[4]))]
            elif items_name == 'Watches':
                all_items[k] = [str(item[0]) + str(item[1]) + str(item[2]) + str(item[3]) + str(item[4]), \
                                Watch(str(item[0]), str(item[1]), str(item[2]), str(item[3]),
                                      [0 if item[4] is None else int(item[4])][0],int(item[5]))]
            k+=1
        return all_items

    def clear(self):
        self.cursor.execute('DROP TABLE IF EXISTS Phones')
        self.cursor.execute('DROP TABLE IF EXISTS Watches')
        self.cursor.execute('DROP TABLE IF EXISTS Airpods')
        self.cursor.execute('DROP TABLE IF EXISTS Macbooks')
        self.cursor.execute('DROP TABLE IF EXISTS Ipads')
        self.cursor.execute('DROP TABLE IF EXISTS Playstations')
        self.connection.commit()
        self.create_tables()

    @staticmethod
    def check_table(database_name) -> bool:
        """
        :param str database_name: Имя таблицы(пользователя), существование которого надо проверить
        :return bool: True, если пользователь есть, False в другом случае
        """
        files = listdir('./database/files')
        for file in files:
            if database_name + '.db' in file:
                return True
        return False
