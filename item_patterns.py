COLORS = ["titanium olive", "black white", "deep purple", "light pink", "red", "purple", "green", "blue", "bluе", "midnight", "starlight",
          "pink", "orange", "yellow", "gold", "silver", "white", "titanium", "titan", "natural", "black", 'space gray', 'space', 'grey', 'gray', 'night', 'star'] # В макбуках серый написан как gray

'''
    Далее идут классы, описывающие свойства, которые могут быть у каждого из товаров.
    Использую я это в парсерах для того, чтобы можно было удобно пользоваться этим
    данными, а также, чтобы параметры можно было удобно добавлять/менять
'''


class Phones:
    MODELS = ["se3", "11", "12", "13", "14", "15", '16']
    VERSIONS = ["plus", "pro max", "pro", "mini", "max"]
    STORAGE = ["64", "128", "256", "512", "1024", "1tb", "1тб", "1 тб", "1 tb"]
    COUNTRIES = ['🇺🇳🇦🇫🇦🇽🇦🇱🇩🇿🇦🇸🇦🇩🇦🇴🇦🇮🇦🇶🇦🇿🇦🇹🇦🇺🇦🇼🇦🇲🇦🇷🇦🇬🇧🇸🇧🇭🇧🇩🇧🇧🇧🇾🇧🇪🇧🇿🇧🇷🇧🇼🇧🇦🇧🇴🇧🇹🇧🇲🇧🇯🇻🇬🇧🇳🇧🇬🇧🇫🇧🇮🇰🇭🇨🇲🇹🇩🇨🇫🇰🇾🇧🇶🇨🇻🇮🇨🇨🇦🇮🇴🇨🇱🇨🇳🇨🇽🇨🇨🇨🇴🇰🇲🇨🇺🇭🇷🇨🇮🇨🇷🇨🇰🇨🇩🇨🇬🇨🇼🇨🇾🇨🇿🇩🇰🇩🇯🇩🇲🇩🇴🇸🇿🇪🇪🇪🇷🇬🇶🇸🇻🇪🇬🇪🇨🇪🇹🇪🇺🇫🇰🇫🇴🇫🇯🇫🇮🇫🇷🇩🇪🇬🇪🇬🇲🇬🇦🇹🇫🇵🇫🇬🇫🇬🇭🇬🇮🇬🇷🇬🇱🇬🇩🇬🇵🇬🇺🇭🇳🇭🇹🇬🇾🇬🇼🇬🇳🇬🇬🇬🇹🇭🇰🇭🇺🇮🇸🇮🇳🇮🇩🇮🇷🇮🇶🎌🇯🇵🇯🇲🇮🇹🇮🇱🇮🇲🇮🇪🇯🇪🇯🇴🇰🇿🇰🇪🇰🇮🇽🇰🇰🇼🇱🇾🇱🇷🇱🇸🇱🇧🇱🇻🇱🇦🇰🇬🇱🇮🇱🇹🇱🇺🇲🇴🇲🇬🇲🇼🇲🇾🇲🇺🇲🇷🇲🇶🇲🇭🇲🇹🇲🇱🇲🇻🇾🇹🇲🇽🇫🇲🇲🇩🇲🇨🇲🇳🇲🇪🇳🇵🇳🇷🇳🇦🇲🇲🇲🇿🇲🇦🇲🇸🇳🇱🇳🇨🇳🇿🇳🇮🇳🇪🇳🇬🇳🇺🇵🇰🇴🇲🇲🇵🇳🇴🇲🇰🇰🇵🇳🇫🇵🇼🇵🇸🇵🇦🇵🇬🇵🇾🇵🇪🇵🇭🇷🇴🇷🇪🇶🇦🇵🇷🇵🇹🇵🇱🇵🇳🇷🇺🇷🇼🇼🇸🇸🇲🇸🇹🇸🇦🇸🇳🇸🇮🇸🇰🇸🇽🇸🇬🇸🇱🇸🇨🇷🇸🇬🇸🇸🇧🇸🇴🇿🇦🇰🇷🇸🇸🇪🇸🇻🇨🇵🇲🇱🇨🇰🇳🇸🇭🇧🇱🇱🇰🇸🇩🇸🇷🇸🇪🇨🇭🇸🇾🇹🇼🇹🇯🇹🇹🇹🇴🇹🇰🇹🇬🇹🇱🇹🇭🇹🇿🇹🇳🇹🇷🇹🇲🇹🇨🇹🇻🇺🇬🇺🇦🇺🇾🇺🇸🏴󠁧󠁢󠁷󠁬󠁳󠁿🏴󠁧󠁢󠁳󠁣󠁴󠁿🏴󠁧󠁢󠁥󠁮󠁧󠁿🇬🇧🇦🇪🇻🇮🇺🇿🇻🇺🇻🇦🇻🇪🇻🇳🇼🇫🇿🇼🇿🇲🇾🇪🇪🇭🇦🇪🇮🇳🇮🇳India']
    COUNTRY_GROUPS = {"sim🇺🇸mini🇺🇸": "", "mini🇭🇰sim🇭🇰mini🇨🇳sim🇨🇳": "", "others": ""}


class Watches:
    models = ['se', 's8', 's9', 'series 9', 'ultra 2', 'ultra', '9']
    sizes = ['40', '41', '44', '45', '49']
    colors = COLORS
    strap_sizes = ['s/m', 'm/l', 'sm', 'ml', 'sport loop', 'alpine loop', 's', 'm']
    year = [str(year) for year in range(2020, 2025)]
    # Страну игнорируем


class Airpods:
    colors = COLORS
    models = ['pro 2', 'pro 2 type c', 'pro 2', 'max', 'pro', '2', '3']
    # !!! max = pro, pro 2 lightning = 2022, pro 2 type c = 2023
    cases = ['magsafe', 'lightning']
    year = [str(year) for year in range(2018, 2024)]
    # Страну игнорируем


class Macbooks:
    models = ['13', '14', '15', '15', '16']     # Разделяются на pro и air, это проверяется в парсере
    cpus = ['m1', 'm2', 'm3', 'м1', 'м2', 'м3']
    color = COLORS
    # serial_numbers = ['mgn63', 'mgn93', 'mlxw3', 'mlxy3', 'mly33', 'z1600000b', 'z1500000b', 'z15W0000b',
    #                   'z1600000l', 'z15s0000p', 'MQKU3', 'MQKP3', 'MQKR3', 'MQKW3', 'MQKX3', 'MQKQ3', 'MQKV3',
    #                   'MQKT3', 'Z18T0000D', 'Z18P0000', 'Z18L0000F', 'Z18R0000H', 'MNEP3', 'MNEH3', 'MNEQ3', 'MNEJ3',
    #                   'MKGP3RU', 'Z15G000DY', 'MR7J3', 'MTL73', 'MTL73', 'MTL73', 'MRX33', 'MRX63', 'MRX43', 'MRX43',
    #                   'MRX53', 'MRX83', 'MK183', 'MK193', 'MRW13', 'MRW43', 'MRW23', 'MRW63', 'MRW63', 'MRW63', 'MUW63',
    #                   'MUW73']
    serial_numbers = {
        'air 13': [x.lower() for x in ['mly13', 'z18t0000d', 'z18p0000k', 'Z1600000B', 'Z15S0000B', 'Z1600000L', 'Z15S0000P', 'Z15T00314', 'MLY33', 'MLY13', 'MLXW3', 'MLXY3', 'MLY43', 'MGN63', 'MRXN3', 'MRXQ3', 'MQKU3', 'MQKP3', 'MQKR3', 'MQKW3', 'MQKX3', 'MQKQ3', 'MQKV3', 'MQKT3', 'Z18T0', 'Z18P0']],
        'pro 13': [x.lower() for x in['MNEH3', 'MNEQ3']],
        'pro 14': [x.lower() for x in ['MPHG3ZP/A', 'MR7J3', 'MTL73', 'MR7K3', 'MTL83', 'MRX33', 'MRX63', 'MRX43', 'MRX73', 'MRX53', 'MRX83']],
        'pro 16': [x.lower() for x in ['MRW13', 'MRW43', 'MRW23', 'MRW63', 'MRW73', 'MRW33', 'MUW63', 'MUW73']]
    }
    storages = ['256', '512', '1024', '2048', '1tb', '1тб', '1', '2tb', '2тб', '2', '4tb', '4тб', '4']
    # Страну игнорируем


class Ipads:
    models = ['mini 6', 'pro 12', 'pro 11', 'air 5', '5', '9', '10', '102', '129', 'air 13', 'pro 13']
    storages = ['64', '128', '256', '512', '1tb', '1тб', '1']
    COLORS = COLORS
    networks = ['wifi', 'wi-fi', 'wi fi', 'lte']
    # Страну игнорируем


class Playstation:
    play_station_models = ['slim digital', 'slim', '1208a', 'xbox x']
    headphones = ['puls 3d']
    gamepads = ['edge', 'white', 'black', 'red', 'blue', 'camouflage', 'purple', 'чёрный', 'белый', 'gold shadow',
                'красный', 'голубой', 'камуфляж', 'розовый', 'фиолетовый']
    stations = ['док станция']
    wheels = ['g29']
    vrs = ['vr2']


def delete_flag(data: str) -> str:
    for el in Phones.COUNTRIES[0]:
        data = data.replace(el, "")
    return data
