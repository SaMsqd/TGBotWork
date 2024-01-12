from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from init_databases import databases


class Keyboard:
    def __init__(self):
        self.active_buttons = ['/help', '/clear', '/number', '/table', '/table_best',
                               '/table_opt', '/table_retail', '/back']
        self.start_buttons = ['/help', '/phones', '/watches', '/airpods', '/macbooks', '/ipads']
        self.pos = 'back'
        self.active_database = None

    def change_pos(self, new_pos: str):
        new_pos = new_pos.replace("/", "")
        self.pos = new_pos if '/' + new_pos in self.start_buttons[1:] else 'back'
        self.active_database = databases[new_pos] if '/' + new_pos in self.start_buttons[1:] else None
        if self.active_database:
            return f'База данных успешно выбрана: {new_pos}'
        elif new_pos == 'back':
            return 'Вы были перемещены на стартовую позицию'
        else:
            return 'Ввод был не правильный, вы были перемещены на стартовую позицию'

    def generate_keyboard(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        row = list()
        buttons = self.start_buttons if self.pos == 'back' else self.active_buttons
        for i in range(len(buttons)):
            row.append(KeyboardButton(text=buttons[i]))
            if i % 3 == 0:
                keyboard.row(*row)
                row = []
        if len(row) != 0:
            keyboard.row(*row)
        return keyboard
