class ParseException(Exception):
    def __init__(self, text: str = ''):
        super().__init__(f'Ошибка в парсинге {text}')
