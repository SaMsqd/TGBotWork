from DB import DataBase


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
        'size': 'int',
        'color': 'text',
        'strap_size': 'text',
        'year': 'int',
        'price': 'integer'
    },
    'airpods': {
        'model': 'text',
        'color': 'text',
        'case': 'text',
        'price': 'integer'
    },
    'macbooks': {
        'model': 'text',
        'cpu': 'text',
        'color': 'text',
        'storage': 'int',
        'price': 'integer'
    },
    'ipads': {
        'model': 'text',
        'storage': 'int',
        'color': 'str',
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
        print(db_object.create_table(table_name=f'{db_name}{chat_id}', columns=columns_for_databases[db_name]))
    return True
