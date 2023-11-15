import sqlite3
import threading


lock = threading.Lock()


# Класс для взаимодействия с базами данных
class DataBase:
    def __init__(self, file_name="database.db"):
        self.file_name = file_name  # Запоминаем имя файла
        self.connection = sqlite3.connect(file_name, check_same_thread=False)    # Создаём соединение
        self.cursor = self.connection.cursor()  # Создаём курсор
        self.tables = self.__get_tables()     # Запоминаем все колонки в каждой таблице в виде списка

    # Нужен только для __init__ возвращает словарь {имя таблицы: [колонка1], [колонка2]}
    def __get_tables(self):
        table_names = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        res = dict()
        for table in table_names:
            res[table[0]] = [{x[1]: x[2]} for x in self.cursor.execute(f"PRAGMA table_info({table[0]})").fetchall()]
        return res

    # Получает инфу о всех пользователях. Аргументы: имя таблицы, распечатать результат? по дефолоту 0
    def get_all_rows(self, table_name, b_print=0):
        with lock:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            if b_print:
                print(self.cursor.fetchall())
            return self.cursor.fetchall()

    # Получает инфу о пользователе. Аргументы: имя таблицы, колонка(по чему мы будем искать), её значение,
    # распечатать результат? по дефолту 0
    def get_user_by(self, table_name, value, search_name="id", b_print=0):
        with lock:
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE {search_name} = {value}")
        return self.cursor.fetchall()

    # Внести в таблицу 1 пользователя. Аргументы: название таблицы, значения
    # Если внести на одно значение меньше, то будет заноситься всё, кроме айди. Чтобы сработало,
    # айди нужен автоинкрементированный
    def insert_user(self, table_name: str, *values):
        with lock:
            if len(values) == len(self.tables[table_name]):
                value = " ".join([f'"{x}",' for x in values])[0:-1]     # Да-да, куча говнокода
                self.cursor.execute(f"INSERT INTO {table_name} VALUES({value})")
                self.connection.commit()
            elif len(values) == len(self.tables[table_name])-1:
                value = " ".join([f'"{x}",' for x in values])[0:-1]
                columns = ", ".join([list(key.keys())[0] for key in self.tables[table_name]][1:])
                self.cursor.execute(f"INSERT INTO {table_name}({columns}) VALUES({value})")
                self.connection.commit()

    # Вставляет в таблицу сразу несоклько пользователей. Лень пока что реализовывать
    def insert_users(self):
        pass

    # Удаляет пользователя по его id. Аргументы: имя таблицы, id пользователя
    def delete_user_by_id(self, table_name, id):
        with lock:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id={id}")
            self.connection.commit()

    # Выполняет sql запрос и пытается его распечатать. Аргументы: команда
    def exec_command(self, command):
        with lock:
            self.cursor.execute(command)
            try:
                data = self.cursor.fetchall()
            except:
                pass
            self.connection.commit()
        return data

    # Удаляет таблицу
    def delete_table(self, table_name):
        with lock:
            self.cursor.execute(f"DROP TABLE {table_name}")
            self.connection.commit()
            self.update_tables()

    # Создаёт таблицу в базе данных. аргументы: название таблицы, **kwargs вида "имя": "колонки её параметры"
    # Пример: create_table(users, {"id": "integer primary key autoincrement", "name": "text"})
    def create_table(self, table_name, columns: dict):
        with lock:
            values = ''
            for key, value in columns.items():
                values += f'{key} {value},'
            values = values[0:-1]
            try:
                self.cursor.execute(f"CREATE TABLE {table_name}({values})")
                self.connection.commit()
                self.update_tables()
                return f"Таблица {table_name} успешно создана в базе {self.file_name}"
            except Exception:
                return False

    def update_tables(self):
        self.tables = self.__get_tables()
