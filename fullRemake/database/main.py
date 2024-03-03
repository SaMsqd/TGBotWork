# Для каждого пользователя создавать свою бд и делать все товары в одной бд, но в разных таблицах
# Создать метод для иннициации бд и создания таблиц
import asyncio
import sqlite3
from fullRemake.items import Item
from fullRemake.items import Phone
from fullRemake.items import Ipad
from fullRemake.items import Airpod
from fullRemake.items import Macbook
from fullRemake.items import Watch
class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(f'./files/{db_name}.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS Phones(model str , version str ,\
        color str , storage int , country str , market str , price int)')
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS Watches(model int , size str ,\
        color str , strap_size str , year int , price int)')
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS Airpods(model str, cas str ,\
        year int , price int)')
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS Macbooks(model str , cpu str ,\
        color str , storage int , price int)')
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS Ipads(model str , network str ,\
         color str , storage int, price int)')
        self.connection.commit()

    def add_items(self, items, item_name):
        """
        Метод для добавления товаров
        :param list[Item] items: предмет для добавления (либо объект, наследующий Item, либо sql строка)
        :param str item_name: название таблицы, в которую нужно добавить предмет
        :return:
        """
        string_items = items[0].generate_sql()
        for i in range(len(items)-1):
            string_items += ',' + items[i+1].generate_sql()

        self.cursor.execute(f'insert into {item_name} values{string_items}')
        self.connection.commit()

    def get_sorted_items(self, items_name):
        """
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
        return all_items_sorted.values()

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
                                Phone(str(item[0]), str(item[1]), item[2], int(item[3]),item[4], item[6]),' ']
                all_items[k][2] = all_items[k][1].priority
            elif items_name == 'Ipads':
                all_items[k] = [str(item[0]) + str(item[1]) + str(item[2]) + str(item[3]), \
                                Ipad(str(item[0]), int(item[1]), str(item[2]), str(item[3]), int(item[4])),' ']
                all_items[k][2] = all_items[k][1].priority
            elif items_name == 'Airpods':
                all_items[k] = [str(item[0]) + str(item[1]) + str(item[2]), \
                                Airpod(int(item[0]), str(item[1]), int(item[2]), int(item[3]))]
                all_items[k][2] = all_items[k][1].priority
            elif items_name == 'Macbooks':
                all_items[k] = [str(item[0]) + str(item[1]) + str(item[2]) + str(item[3]), \
                                Macbook(int(item[0]), str(item[1]), str(item[2]), int(item[3]), int(item[4])),' ']
                all_items[k][2] = all_items[k][1].priority
            elif items_name == 'Watches':
                all_items[k] = [str(item[0]) + str(item[1]) + str(item[2]) + str(item[3]) + str(item[4]), \
                                Watch(int(item[0]), str(item[1]), str(item[2]), str(item[3]), int(item[4]),int(item[5]))]
                all_items[k][2] = all_items[k][1].priority
            k+=1
        return self.__merge_sort(all_items)


    def __merge_sort(self,items):
        if len(items) > 1:
            mid = len(items)//2
            left = items[:mid]
            right = items[mid:]
            self.__merge_sort(left)
            self.__merge_sort(right)

            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i][2] < right[j][2]:
                    items[k] = left[i]
                    i += 1
                else:
                    items[k] = right[j]
                    j +=1
                k += 1

            while i < len(left):
                items[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                items[k] = right[j]
                j += 1
                k += 1
        return items


t = Database('Good')
t.create_tables()
# t.add_items([Ipad('mini 7', 64, 'Blue', 'lte', 130000)],'Ipads')
a = t.get_sorted_items('Ipads')
print(a)



