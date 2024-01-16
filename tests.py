import unittest
import main


# Декоратор для красивого вывода
def beautiful_output(func):
    print('\n', "=" * 30, '\n')
    func()
    print('\n', "=" * 30, '\n')


class TestingParsers(unittest.TestCase):
    def setUp(self):
        self.phones = '''
15 128 Black -77.500🇮🇳
15 128 Black -76.200🇨🇳 
15 128 Blue-76.200🇨🇳
15 128 Blue -76.500🇺🇸
15 128 Pink -74.500🇨🇳
15 128 Pink -76.000🇺🇸 
15 128 Green-74.500🇨🇳
14 Pro Max 256 Black -109.800🇺🇸
14 Pro Max 256 Purple -115.500🇦🇪
14 Pro Max 256 Purple-120.500🇯🇴(3🛡️месяцев доп гарантия) 
14 Pro Max 256 Purple -112.000🇺🇸
14 Pro Max 256 Gold-116.000🇨🇳 
14 Pro Max 256 Gold-109.000🇺🇸
14 Pro Max 512 Silver-120.500🇯🇴
14 Pro Max 512 Black -124.500🇯🇴
14 Pro Max 512 Black-120.500🇺🇸
14 Pro Max 512 Gold -123.800🇯🇵
14 Pro Max 512 Gold -120.500🇺🇸
14 Pro Max 1TB Silver - 133.500🇯🇵
14 Pro Max 1Tb Black -135.500🇯🇴
14 Pro Max 1Tb Gold-133.500🇯🇴
'''.lower()
        self.watches = '''
Watch SE 40 Starlight SM 2023-25.200🇺🇸
Watch SE 2023 40 White ML-23.800🇺🇸
Watch SE 2023 40 Midnight S/M-23.800🇺🇸
Watch SE 2023 44 Midnight ML-25.200🇺🇸
Watch SE 2023 44 Midnight SM-25.200🇺🇸
Watch SE 2023 44 Starlight ML-25.000🇺🇸
Watch SE 2022 44 Silver M/L-24.000🇺🇸
Watch S8 45 Sport RED M/L-33.700🇺🇸
Watch S9 41 Pink ML -36.700🇺🇸
Watch S9 41 Pink Sport Loop-37.000🇺🇸
Watch S9 41 Midnight (S/M)-37.500🇺🇸
Watch S9 41 Midnight Sport Loop-37.000
Watch S9 41 Starlight SM -39.300🇺🇸
Watch S9 41 Starlight Loop-39.000🇺🇸
Watch S9 41 Silver  -37.800🇺🇸
Watch S9 41 Silver Loop-36.500🇺🇸
Watch S9 45 Pink (M/L)-40.400🇺🇸
Watch S9 45 Pink Sport Loop-40.800🇺🇸
WatchS9 45 Midnight M/L-40.300🇺🇸
WatchS9 45 Midnight S/M-40.300🇺🇸
WatchS9 45 Midnight Loop-40.300🇺🇸
Watch S9 45 White M/L-40.800🇺🇸
Watch S9 45 White Sport  (S/M)-40.900🇺🇸
Watch S9 45 White Sport Loop-41.000🇺🇸
Apple Watch Ultra Orange Alpine Loop M-64.000
Apple Watch Ultra Yellow/Beige TrailLoop (S/M)-64.000
Apple  Ultra 49 White Ocean -64.000
Watch Ultra 2 49 Titanium Olive Alpine Loop (S)-75.500🇺🇸
Watch Ultra 2 49 Titanium White Ocean Band -76.000🇺🇸
Watch Ultra 2 49 Titanium Blue ocean -79.900🇺🇸
Watch Ultra 2 49 Titanium Blue/Black trail M/L -79.500🇺🇸
Watch Ultra 2 49 Titanium Ingigo alpine M -76.500🇺🇸
Watch Ultra 2 49 Olive alpine M -76.500🇺🇸
🇺🇸AW 9 45mm Pink M/L - 38,500   
🇺🇸AW S9 41mm Pink S/M - 36,000
S9 41 Midnight (S/M) - 39.000
S9 41 Red Sport Band (M/L) - 39.000 
S9 45 Midnight AL (S/M) - 42.000
S9 45 Pink AL Lihgt Pink (M/L) - 42.000
S9 45 Pink AL Lihgt Pink (S/M) - 42.000
'''.lower()
        self.airpods = '''
AirPods Max Gray-59.000
AirPods 2-9.800🇪🇺
AirPods (3rd Gen) with MagSafe Case-17.300🇪🇺
AirPods pro 2 (2022) MagSafe-20.400🇪🇺 
AirPods pro 2 (2023) MagSafe-21.500🇪🇺
AirPods pro 2 - 19,500
AirPods 2 9700🇪🇺
AirPods 3 MagSafe 17000🇪🇺
AirPods Pro 2 20000🇪🇺
AirPods Pro 2 2023 21500🇪🇺
Airpods 3 Magsafe - 17.000 
AirPods Pro 2 - 19.800
AirPods 2 9.500 (Lightning 2019 год)
AirPods 3 Lightning 16.600
AirPods Pro 2 Lightning 2022 -  19.700
AirPods Pro 2 USB-c & MagSafe 2023 - 21.300
        '''.lower()
        self.macbooks = '''
Air 13 MGN63 (M1,8/256) Gray -75.500🇮🇳(с гравировкой) 
Air 13 MGND3 (M1,8/256) Gold -78.000🇺🇸🇮🇳
Air 13 MGN93 (M1,8/256) Silver-75.500🇮🇳 ( с гравировкой) 
MacBook MLY33 Air 13 Midnight (M2, 8GB, 256GB) 2022-99.300🇺🇸 
MacBook MLXW3 (M2-8/256) Gray -100.000🇺🇸 
MacBook MLY13 (M2-8/256) Starlight - 100.500🇺🇸
MacBook MLXY3(M2-8/256) Silver -101.500🇺🇸  
Air 15 MQKP3 (M2,8/256) Gray-111.000🇺🇸
Air 15 MQKW3 (M2,8/256) Midnight-112.000🇺🇸
Air 15 MQKR3 (M2,8/256) Silver -115.500🇺🇸
Air 15 MQKU3 (M2,8/256) Starlight-115.800🇺🇸
Air 15 MQKQ3 (M2,8/512) Gray-153.000🇺🇸
Air 15 MQKX3 (M2,8/512) Midnight-152.000🇺🇸
Air 15 MQKV3(M2,8/512) Starlight -153.000🇺🇸
Air 15 MQKT3 (M2,8/512) Silver-153.000🇺🇸 
Pro 13 MNEP3(M2,8/256)Silver-109.500🇺🇸
Pro 13 MNEH3(M2,8/256)Gray-109.500🇺🇸
Pro 13 MNEJ3 (M2,8/512)Gray-131.000🇺🇸
Pro 13 MNEQ3(M2,8/512)Silver-131.000🇺🇸
Pro 13 (M2,24/1TB) Silver-198.000🇺🇸RFB 
Pro 14 MKGP3(M1,16/512)Gray-146.500🇷🇺 
Pro 14 MKGR3 (M1,16/512)Silver -146.500🇷🇺
Pro 14 MPHF3(M2,16/1TB)Gray-224.000🇺🇸
Pro MTL73 14 513 (2023) Grey (M3 , 8 Gb, 512Gb SSD) -183.000🇺🇸 
Pro MTL83 14 1 Tb (2023) Grey (M3 , 8 Gb, 1Tb SSD)-201.000🇺🇸
MacBook MRX33  Pro 14 M3 512GB Space Gray -191.000🇺🇸
MacBook MRX63  Pro 14 M3 512GB Silver -191.000🇺🇸
Pro 16 (MK183) M1/16/512 gray -166.500🇷🇺
Pro 16 MMQW3 (M1 Max 10/32/64/4TB) Silver -418.00🇺🇸
Pro 16 MNW83 (M2,16/512) Gray -222.500🇺🇸
Pro 16 Z1760005S (M2 Max 12/38/32/2TB) Gray -414.000🇺🇸
Pro 16 Z1760005V (M2 Max 12/38/64/1TB) Gray -436.700🇺🇸 
Pro 16 MRW13 Space Black (M3 Pro 12-Core, GPU 18-Core, 18GB, 512GB) - 236.500🇺🇸
Pro 16 MRW23 Space Black (M3 Pro 12-Core, GPU 18-Core, 36GB, 512GB)- 275.000🇺🇸
Pro MRW33 16 1 Tb (2023) Black M3 PRO MAX -445.000🇺🇸
🇻🇳Macbook Air M1 8/256 MGN63 Black (С гравировкой.АНГЛ/РУС, БЕЗ ПЛЁНКИ) - 74,000    
🇻🇳Macbook Air M1 8/256 MGND3 Gold (С гравировкой.АНГЛ/РУС, БЕЗ ПЛЁНКИ) - 74,000    
🇻🇳Macbook Air M1 8/256 MGN93 silver (С гравировкой.АНГЛ/РУС, БЕЗ ПЛЁНКИ) - 74,000    
🇺🇸MQKU3 (Air 15 M2 8/256 Starlight) - 114,000
MGN63 (Air 13 M1 8/256 Sp.Grey) - 77000
MGN93 (Air 13 M1 8/256 Silver) - 77000🇸🇬с гравировкой 
MGND3 (Air 13 M1 8/256 Gold)  -  77000🇮🇳 с гравировкой
MLXY3 (Air 13 M2 8/256 Silver) - 103000🇺🇸
MLXW3 (Air 13 M2 8/256 Sp.Gray) - 103000🇺🇸
'''.lower()
        self.ipads = '''
IPad 9 64 Gray WIFI -28.700🇺🇸
IPad 9 64 Silver WIFI-28.700🇺🇸
IPad 9 64 Gray LTE -41.000🇺🇸
IPad 9 64 White LTE -41.000🇺🇸
IPad 9 256 Gray WIFI -44.000🇺🇸
IPad 9 256 Silver WIFI-44.000🇺🇸
IPad 10 64 Yellow WIFI -42.000🇺🇸
IPad 10 64 Blue WIFI -42.000🇺🇸
IPad 10 64 Silver WIFI -42.000🇺🇸
IPad 10 64 Pink WIFI -42.000🇺🇸
iPad 10 256 Wi-Fi Blue-56.000🇺🇸
iPad 10 256 Wi-Fi Silver-55.500🇺🇸
iPad 10 256 Wi-Fi Yellow -55.000🇺🇸
iPad Air 5 64 Wi-Fi PINK -56.500🇺🇸
iPad PRO 11 M2 128 Gray Wi-Fi-80.000🇺🇸
IPad Pro 11 128 Gray LTE (2022)-88.500🇺🇸
iPad Pro 11 (Wi-Fi , 512GB) Gray -112.000🇺🇸
iPad Pro 11 (Wi-Fi , 512GB) Silver-112.000🇺🇸
iPad Pro 12.9 2022 M2 LTE 128 Gray - 102.000🇺🇸 
iPad Pro 12.9 2022 M2 LTE 128 Silver - 102.800🇺🇸 
IPad Pro 12 256 Gray WI-FI (2022)-117.500🇺🇸
IPad Pro 12 256 Silver WI-FI (2022)-117.900🇺🇸
iPad Pro 12.9 2022 M2 LTE 256 Silver - 128.500🇺🇸
iPad Pro 12.9 2022 M2 LTE 256 Grey  - 128.800🇺🇸
IPad Pro 12 512GB Gray WI-FI (2022)-141.000🇺🇸
iPad Pro 12.9 2022 M2 LTE 512 Gray - 146.000🇺🇸
iPad Pro 12.9 2022 M2 LTE 512 Silver - 146.000🇺🇸
iPad 10.2 64GB Silver WIFI 28500 2021🇺🇸
iPad 10 64GB Blue WIFI 41000 🇺🇸
iPad 10 64GB Pink WIFI 41000🇺🇸
iPad 10 64GB Silver WIFI 41000🇺🇸
iPad 10 64GB Yellow WIFI 41000🇺🇸
iPad 10 256GB Blue WIFI 55000🇺🇸
iPad 10 256GB Pink WIFI 56000🇺🇸
iPad 10 256GB Yellow WIFI 55000🇺🇸
IPad pro 11 128GB Silver WIFI  83000🇺🇸
IPad pro 11 128GB Gray WIFI  83000🇺🇸
        '''.lower()
        self.everything = (self.phones + self.watches + self.airpods + self.macbooks + self.ipads).lower()
        while '\n\n' in self.everything:
            self.everything = self.everything.replace('\n\n', '\n')
        while '  ' in self.everything:
            self.everything = self.everything.replace('  ', ' ')
        self.everything = self.everything.split('\n')
        self.everything.remove(' ')
        self.everything.remove('')
        self.parse_watches = [
            'Watch SE 40 Starlight SM 2023-25.200🇺🇸',
            'Watch SE 2023 40 White ML-23.800🇺🇸',
            'Watch SE 2023 40 Midnight S/M-23.800🇺🇸',
            'Watch S9 41 Pink Sport Loop-37.000🇺🇸',
            'Watch S9 45 Pink (M/L)-40.400🇺🇸',
            'Watch Ultra 2 49 Titanium Olive Alpine Loop (S)-75.500🇺🇸',
            '🇺🇸AW S9 45mm Pink M/L - 38,500',
            'S9 45 Pink AL Lihgt Pink (M/L) - 42.000'
        ]
        self.parse_airpods: dict = {1: 'AirPods Max Grey-59.000', 2: 'AirPods (3rd Gen) with MagSafe Case-17.300🇪🇺',
                              3: 'AirPods pro 2 (2023) MagSafe-21.500🇪🇺', 4: 'AirPods pro 2 - 19,500',
                              5: 'AirPods 2 9.500 (Lightning 2019 год)', 6: 'AirPods Pro 2 USB-c & MagSafe 2023 - 21.300'}
        self.parse_macbooks: dict = {#1: 'Air 13 MGN63 (M1,8/256) Gray -75.500🇮🇳(с гравировкой) ',
                                     2: 'MacBook MLY33 Air 13 Midnight (M2, 8GB, 256GB) 2022-99.300🇺🇸 ',
                                     3: 'Pro 13 MNEP3(M2,8/256)Silver-109.500🇺🇸',
                                     4: 'MacBook MRX33  Pro 14 M3 512GB Space Gray -191.000🇺🇸',
                                     5: 'Pro 16 MRW13 Space Black (M3 Pro 12-Core, GPU 18-Core, 18GB, 512GB) - 236.500🇺🇸',
                                     6: 'Pro MRW33 16 1 Tb (2023) Black M3 PRO MAX -445.000🇺🇸',
                                     7: 'MGN63 (Air 13 M1 8/256 Sp.Grey) - 77000'}
        self.parse_ipads: dict = {
            1: 'IPad 9 64 Gray WIFI -28.700🇺🇸',
            2: 'IPad 9 64 White LTE -41.000🇺🇸',
            3: 'IPad 10 64 Yellow WIFI -42.000🇺🇸',
            4: 'iPad PRO 11 M2 128 Gray Wi-Fi-80.000🇺🇸',
            5: 'iPad Pro 11 (Wi-Fi , 512GB) Gray -112.000🇺🇸',
            6: 'iPad Pro 12.9 2022 M2 LTE 128 Silver - 102.800🇺🇸',
            7: 'IPad Pro 12 256 Gray WI-FI (2022)-117.500🇺🇸',
            8: 'iPad 10 256GB Yellow WIFI 55000🇺🇸',
            9: 'IPad pro 11 128GB Gray WIFI  83000🇺🇸'
        }

    @unittest.skip
    def test_watches_parser(self):
        for subject in self.parse_watches:
            with self.subTest(subject=subject):
                data = main.parse_watches(subject.lower())
                if data == {'model': 'se', 'size': '40', 'color': 'starlight', 'strap_size': 'sm',
                            'year': '2023', 'price': '25200'} or \
                        data == {'model': 'se', 'year': '2023', 'size': '40', 'color': 'white', 'strap_size': 'ml',
                                 'price': '23800'} or \
                        data == {'model': 'se', 'year': '2023', 'size': '40', 'color': 'midnight', 'strap_size': 's/m',
                                 'price': '23800'} or \
                        data == {'model': 's9', 'size': '41', 'color': 'pink', 'price': '37000'} or \
                        data == {'model': 's9', 'size': '45', 'color': 'pink', 'strap_size': 'm/l',
                                 'price': '40400'} or \
                        data == {'price': '37000', 'model': 's9', 'size': '41', 'strap_size': 'sport loop', 'color': 'pink'} or \
                        data == {'price': '42000', 'model': 's9', 'size': '45', 'strap_size': 'm/l', 'color': 'pink'} or \
                        data == {'price': '75500', 'model': 'ultra 2', 'size': '49', 'strap_size': 'alpine loop s', 'color': 'titanium olive'} or \
                        data == {'price': '38500', 'model': 's9', 'size': '45', 'strap_size': 'm/l', 'color': 'pink'}:
                    pass
                else:
                    print(subject, data)

    @unittest.skip
    def test_airpods_parser(self):
        for pos, data in self.parse_airpods.items():
            with self.subTest(pos=pos, data=data):
                res = main.parse_airpods(data.lower())
                if pos == 1 and res == {'model': 'pro', 'color': 'grey', 'price': '59000'} or \
                        pos == 2 and res == {'case': 'magsafe', 'model': '3', 'price': '1700'} or \
                        pos == 3 and res == {'model': 'pro', 'year': '2023', 'case': 'magsafe', 'price': '21500'} or \
                        pos == 4 and res == {'model': 'pro 2', 'price': '19500'} or \
                        pos == 5 and res == {'model': '2', 'price': '9500'} or \
                        pos == 6 and res == {'model': 'pro 2', 'case': 'magsafe', 'year': '2023', 'price': '21300'}:
                    print(data, res)
                    pass
                else:
                    print(data, res)

    @unittest.skip
    def test_macbooks_parser(self):
        for pos, data in self.parse_macbooks.items():
            with self.subTest(pos=pos, data=data):
                data = main.parse_macbooks(data)
                if pos == 1 and data == {'price': '75500', 'model': 'air 13', 'color': 'gray', 'cpu': 'm1', 'storage': '256'} or \
                    pos == 2 and data == {'price': '99300', 'model': 'air 13', 'color': 'midnight', 'cpu': 'm2', 'storage': '256'} or \
                    pos == 3 and data == {'price': '109500', 'model': 'pro 13', 'color': 'silver', 'cpu': 'm2', 'storage': '256'} or \
                    pos == 4 and data == {'price': '191000', 'model': 'pro 14', 'color': 'gray', 'cpu': 'm3', 'storage': '512'} or \
                    pos == 5 and data == {'price': '236500', 'model': 'pro 16', 'color': 'black', 'cpu': 'm3', 'storage': '512'} or \
                    pos == 6 and data == {'price': '445000', 'model': 'pro 16', 'color': 'black', 'cpu': 'm3', 'storage': '1'} or \
                    pos == 7 and data == {'price': '77000', 'model': 'air 13', 'color': 'grey', 'cpu': 'm1', 'storage': '256'}:
                    pass
                else:
                    print(pos, data)
                    raise Exception

    def test_ipads_parser(self):
        for pos, data in self.parse_ipads.items():
            with self.subTest(pos=pos, data=data):
                data = main.parse_airpods(data)
                print(pos, data)

    # def test_is_phone(self):
    #     for item in self.everything:
    #         with self.subTest(item=item):
    #             self.assertEqual(main.is_phone(item), item in self.phones)

    @unittest.skip
    def test_is_ipad(self):
        for item in self.everything:
            with self.subTest(item=item):
                self.assertEqual(main.is_ipad(item), item in self.ipads)

    @unittest.skip
    def test_is_macbook(self):
        for item in self.everything:
            with self.subTest(item=item):
                self.assertEqual(main.is_macbook(item), item in self.macbooks)

    @unittest.skip
    def test_is_watch(self):
        for item in self.everything:
            with self.subTest(item=item):
                self.assertEqual(main.is_watch(item), item in self.watches)

    @unittest.skip
    def test_is_airpod(self):
        for item in self.everything:
            with self.subTest(item=item):
                self.assertEqual(main.is_airpod(item), item in self.airpods)
