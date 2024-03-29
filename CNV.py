# Файлик с цветами(C), именами(N) и версиями(V) телефонов
# Он вспомогательный, используется для того, чтобы сделать парсинг телефонов более гибким
# !!! Позже добавил ещё список STORAGE для функции command_funcs.get_data_from_string

COLORS = ["titanium olive", "black white", "deep purple", "light pink", "red", "purple", "green", "blue", "midnight", "starlight",
          "pink", "yellow", "gold", "silver", "white", "titanium", "titan", "natural", "black", 'grey', 'gray'] # В макбуках серый написан как gray

'''
    Далее идут классы, описывающие свойства, которые могут быть у каждого из товаров.
    Использую я это в парсерах для того, чтобы можно было удобно пользоваться этим
    данными, а также, чтобы параметры можно было удобно добавлять/менять
'''


class Phones:
    NAMES = ["se3", "11", "12", "13", "14", "15"]
    VERSIONS = ["plus", "pro max", "pro", "mini", "max"]
    STORAGE = ["64", "128", "256", "512", "1024", "1tb", "1тб", "1"]
    COUNTRIES = ["""🇺🇳🇦🇫🇦🇽🇦🇱🇩🇿🇦🇸🇦🇩🇦🇴🇦🇮🇦🇶🇦🇿🇦🇹🇦🇺🇦🇼🇦🇲🇦🇷🇦🇬🇧🇸🇧🇭🇧🇩🇧🇧🇧🇾🇧🇪🇧🇿🇧🇷🇧🇼🇧🇦🇧🇴🇧🇹🇧🇲🇧🇯🇻🇬🇧🇳🇧🇬🇧🇫🇧🇮🇰🇭🇨🇲🇹🇩🇨🇫🇰🇾🇧🇶🇨🇻🇮🇨🇨🇦🇮🇴🇨🇱🇨🇳🇨🇽🇨🇨🇨🇴
                 🇰🇲🇨🇺🇭🇷🇨🇮🇨🇷🇨🇰🇨🇩🇨🇬🇨🇼🇨🇾🇨🇿🇩🇰🇩🇯🇩🇲🇩🇴🇸🇿🇪🇪🇪🇷🇬🇶🇸🇻🇪🇬🇪🇨🇪🇹🇪🇺🇫🇰🇫🇴🇫🇯🇫🇮🇫🇷🇩🇪🇬🇪🇬🇲🇬🇦🇹🇫🇵🇫🇬🇫🇬🇭🇬🇮🇬🇷🇬🇱🇬🇩🇬🇵🇬🇺🇭🇳🇭🇹🇬🇾🇬🇼🇬🇳🇬🇬🇬🇹🇭🇰
                 🇭🇺🇮🇸🇮🇳🇮🇩🇮🇷🇮🇶🎌🇯🇵🇯🇲🇮🇹🇮🇱🇮🇲🇮🇪🇯🇪🇯🇴🇰🇿🇰🇪🇰🇮🇽🇰🇰🇼🇱🇾🇱🇷🇱🇸🇱🇧🇱🇻🇱🇦🇰🇬🇱🇮🇱🇹🇱🇺🇲🇴🇲🇬🇲🇼🇲🇾🇲🇺🇲🇷🇲🇶🇲🇭🇲🇹🇲🇱🇲🇻🇾🇹🇲🇽🇫🇲🇲🇩🇲🇨🇲🇳🇲🇪🇳🇵🇳🇷🇳🇦
                 🇲🇲🇲🇿🇲🇦🇲🇸🇳🇱🇳🇨🇳🇿🇳🇮🇳🇪🇳🇬🇳🇺🇵🇰🇴🇲🇲🇵🇳🇴🇲🇰🇰🇵🇳🇫🇵🇼🇵🇸🇵🇦🇵🇬🇵🇾🇵🇪🇵🇭🇷🇴🇷🇪🇶🇦🇵🇷🇵🇹🇵🇱🇵🇳🇷🇺🇷🇼🇼🇸🇸🇲🇸🇹🇸🇦🇸🇳🇸🇮🇸🇰🇸🇽🇸🇬🇸🇱🇸🇨🇷🇸🇬🇸🇸🇧🇸🇴🇿🇦🇰🇷
                 🇸🇸🇪🇸🇻🇨🇵🇲🇱🇨🇰🇳🇸🇭🇧🇱🇱🇰🇸🇩🇸🇷🇸🇪🇨🇭🇸🇾🇹🇼🇹🇯🇹🇹🇹🇴🇹🇰🇹🇬🇹🇱🇹🇭🇹🇿🇹🇳🇹🇷🇹🇲
                 🇹🇨🇹🇻🇺🇬🇺🇦🇺🇾🇺🇸🏴󠁧󠁢󠁷󠁬󠁳󠁿🏴󠁧󠁢󠁳󠁣󠁴󠁿🏴󠁧󠁢󠁥󠁮󠁧󠁿🇬🇧🇦🇪🇻🇮🇺🇿🇻🇺🇻🇦🇻🇪🇻🇳🇼🇫🇿🇼🇿🇲🇾🇪🇪🇭"""]
    COUNTRY_GROUPS = {"sim🇺🇸mini🇺🇸": "", "mini🇭🇰sim🇭🇰mini🇨🇳sim🇨🇳": "", "others": ""}


class Watches:
    models = ['se', 's8', 's9', 'series 9', 'ultra 2', 'ultra']
    sizes = ['40', '41', '44', '45', '49']
    colors = COLORS
    strap_sizes = ['s/m', 'm/l', 'sm', 'ml', 'sport loop', 's']
    year = [str(year) for year in range(2020, 2025)]
    # Страну игнорируем


class Airpods:
    models = ['pro 2 lightning', 'pro 2 type c', 'pro 2', 'max', 'pro', '2', '3']
    # !!! max = pro, pro 2 lightning = 2022, pro 2 type c = 2023
    cases = ['magsafe', 'charging']
    year = [str(year) for year in range(2018, 2024)]
    # Страну игнорируем


class Macbooks:
    models = ['13', '14', '15', '16'] # Разделяются на pro и air, это проверяется в парсере
    cpus = ['m1', 'm2', 'm3']
    color = COLORS
    storages = ['256', '512', '1024', '2048', '1tb', '1тб', '1', '2tb', '2тб', '2', '4tb', '4тб', '4']
    # Страну игнорируем


class Ipads:
    models = ['pro 12', 'pro 11', 'air 5', '9', '10']
    storages = ['64', '128', '256', '512', '1tb', '1тб', '1']
    color = COLORS
    networks = ['wifi', 'wi-fi', 'wi fi', 'lte']
    # Страну игнорируем


def delete_flag(data: str) -> str:
    for el in Phones.COUNTRIES[0]:
        data = data.replace(el, "")
    return data
