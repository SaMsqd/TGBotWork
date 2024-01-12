# Файлик с цветами(C), именами(N) и версиями(V) телефонов
# Он вспомогательный, используется для того, чтобы сделать парсинг телефонов более гибким
# !!! Позже добавил ещё список STORAGE для функции command_funcs.get_data_from_string

COLORS = ["black white", "deep purple", "red", "purple", "green", "blue", "midnight", "starlight",
          "pink", "yellow", "gold", "silver", "white", "titan", "titanium", "natural", "black"]

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
    models = ['se', 's8', 's9', 'series 9']
    sizes = ['40', '41', '44', '45']
    colors = COLORS
    strap_sizes = ['s/m', 'm/l', 'sm', 'ml']
    year = [str(year) for year in range(2000, 2025)]
    # Страну игнорируем


class Airpods:
    models = ['2', '3', 'pro 2 lightning', '2022', 'pro 2 type c', '2023', 'max', 'pro']
    # !!! max = pro, pro 2 lightning = 2022, pro 2 type c = 2023
    cases = ['magsafe', 'charging']
    # Страну игнорируем


class Macbooks:
    models = ['air 13', 'air 15', 'pro 13', 'pro 14', 'pro 16']
    cpus = ['m1', 'm2', 'm3']
    color = COLORS
    storages = ['256', '512', '1024', '2048', '1tb', '1тб', '1', '2tb', '2тб', '2']
    # Страну игнорируем


class Ipads:
    models = ['9', '10', 'air 5', 'pro 11', 'pro 12']
    storages = ['64', '128', '256', '512', '1tb', '1тб', '1']
    color = COLORS
    networks = ['wifi', 'wi-fi', 'wi fi', 'lte']
    # Страну игнорируем


def delete_flag(data: str) -> str:
    for el in Phones.COUNTRIES[0]:
        data = data.replace(el, "")
    return data
