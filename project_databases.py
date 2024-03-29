import DB
from DB import DataBase
from main import to_replace_positions


# Если что, можно добавить к какому-то продукту дополнительные колонки, которые будут определять приоритет одного или
# другого значения, чтобы исправить проблемы с выводом
columns_for_databases = {
    'phones': {
        'name': 'text',
        'model': 'text',
        'color': 'text',
        'price': 'integer',
        'storage': 'integer',
        'country': 'text'
    },
    'watches': {
        'model': 'text',
        'size': 'integer',
        'color': 'text',
        'strap_size': 'text',
        'year': 'integer',
        'price': 'integer'
    },
    'airpods': {
        'model': 'text',
        'color': 'text',
        'case_type': 'text',
        'year': 'integer',
        'price': 'integer'
    },
    'macbooks': {
        'model': 'text',
        'cpu': 'text',
        'color': 'text',
        'storage': 'integer',
        'price': 'integer'
    },
    'ipads': {
        'model': 'text',
        'storage': 'integer',
        'color': 'text',
        'price': 'integer'
    }
}


# Функция создаёт базы данных под каждый продукт. Для пользователей базы общие
def init_databases() -> dict:
    phones_db = DataBase('databases/phones.db')         # БД с айфонами
    watches_db = DataBase('databases/watches.db')       # БД с часами
    airpods_db = DataBase('databases/airpods.db')       # БД с наушниками
    macbooks_db = DataBase('databases/macbooks.db')     # БД с макбуками
    ipads_db = DataBase('databases/ipads.db')           # БД с айпадами
    return {
        'phones': phones_db,
        'watches': watches_db,
        'airpods': airpods_db,
        'macbooks': macbooks_db,
        'ipads': ipads_db
    }


# Да, знаю, что плохо, но удобно. Используется для доступа к базам данных извне
databases = init_databases()


# Функция создаёт таблицы, в базе данных каждого продукта. К ним может получить доступ только пользователь,
# для которого (с использованием чьего id) была создана таблицы
def init_tables(chat_id: int):
    for db_name, db_object in databases.items():
        db_object.create_table(table_name=f'{db_name}{chat_id}', columns=columns_for_databases[db_name])
        print('создана таблица', db_name)
    return True


def get_best_from_active_database(database: str, chat_id: str | int):    # Реализовать выборку лучших результатов
    active_db = databases[database]
    match database:
        case 'phones':
            t_data = active_db.exec_command(f"SELECT * FROM phones{chat_id} ORDER BY name, model, storage, country, price")
            best_sorted = []
            for phone in t_data:
                b, index = to_replace_positions(phone, best_sorted)
                if b:
                    if index != -1:
                        best_sorted.insert(index, phone)
                        best_sorted.pop(index + 1)
                elif index == 2:
                    continue
                else:
                    best_sorted.append(phone)
            return best_sorted
        case 'watches':
            pass
        case 'airpods':
            pass
        case 'macbooks':
            pass
        case 'ipads':
            pass


# В классе будут собираться лучшие позиции из баз данных пользователя
class BestPositions:
    def __init__(self, user_id: int | str,
                 databases: dict):
        self.user_id = user_id
        self.databases = databases

    def phones(self):
        t_data = self.databases[f'phones{self.user_id}'].exec_command(
            f"SELECT * FROM phones{self.user_id} ORDER BY name, model, storage, country, price")
        best_sorted = []
        for phone in t_data:
            b, index = to_replace_positions(phone, best_sorted)
            if b:
                if index != -1:
                    best_sorted.insert(index, phone)
                    best_sorted.pop(index + 1)
            elif index == 2:
                continue
            else:
                best_sorted.append(phone)
        return best_sorted

    def watches(self):
        t_data = self.databases[f'watches{self.user_id}'].execute(
            f"SELECT * FROM watches{self.user_id} ORDER BY model, size, strap_size, year, color, price")

    def airpods(self):
        t_data = self.databases[f'airpods{self.user_id}'].execute(
            f"SELECT * FROM airpods{self.user_id} ORDERED BY model, case_type, year, color, price")

    def macbooks(self):
        t_data = self.databases[f'macbooks{self.user_id}'].execute(
            f"SELECT * FROM macbooks{self.user_id} ORDERED BY model, cpu, storage, color, price")

    def ipads(self):
        t_data = self.databases[f'ipads{self.user_id}'].execute(
            f"SELECT * FROM ipads{self.user_id} ORDERED BY model, storage, color, price")
