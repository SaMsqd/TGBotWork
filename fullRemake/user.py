"""
Этот файл нужен для поддержки параллельной работы сразу нескольких юзеров
"""


statuses = {
    1: 'phones',
    2: 'watches',
    3: 'airpods',
    4: 'macbooks',
    5: 'ipads'
}


class User:
    def __init__(self, user_id):
        """
        В классе фигурирует id пользователя, название БД с ним и статус клавиатуры
        :param int user_id: id чата сс пользователем
        """
        self.user_id = user_id
        self.database_name = 'id' + str(user_id)
        self.keyboard_status = None

    def change_keyboard_status(self, new_status):
        """
        Меняет статус клавиатуры на строку
        :param str | int new_status:
        :return:
        """
        self.keyboard_status = [new_status.lower() if type(new_status) is str and new_status.lower() in statuses.keys()
                                else statuses[new_status]][0]

    @staticmethod
    def get_users():
        pass
