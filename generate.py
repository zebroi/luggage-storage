#!/usr/bin/env python3
"""
generate.py v2 — читает location-template.html, подставляет переменные
Запуск: python generate.py
"""
import openpyxl, os, re, random, json
from pathlib import Path
from datetime import datetime

# ─── НАСТРОЙКИ ────────────────────────────────────────────────────────────────
TEMPLATE_FILE = 'location-template.html'
KEYS_FILE     = 'keys.xlsx'
OUTPUT_DIR    = Path('pages')
BASE_URL      = 'https://luggage-storage-nu.vercel.app'
MONTHS_RU = {1:'января',2:'февраля',3:'марта',4:'апреля',5:'мая',6:'июня',
             7:'июля',8:'августа',9:'сентября',10:'октября',11:'ноября',12:'декабря'}
_now = datetime.now()
TODAY = f"{_now.day} {MONTHS_RU[_now.month]} {_now.year}"
TODAY_ISO = _now.strftime('%Y-%m-%d')
YEAR = str(_now.year)
QEEPL_DEFAULT   = 'https://qeepl.com?discount=SBUHJKBO'
RADICAL_DEFAULT = 'https://radicalstorage.tpm.lv/NSfHizPV?erid=2VtzqvWLUd3'

OUTPUT_DIR.mkdir(exist_ok=True)

# ─── КАТАЛОГ СЕРВИСОВ (53 шт.) ────────────────────────────────────────────────
SERVICES = [
  {"id":"qeepl","name":"Qeepl","domain":"qeepl.com","tagline":"Официальный партнёр","desc":"Удобное хранение багажа в сотнях точек по всему миру. Бронирование онлайн, страховка до €5000 включена.","rating":4.9,"reviews":12400,"price":"от 149 ₽/сут","affiliate":True,"badge":"Лучший выбор","features":["Страховка €5000","Онлайн-бронь","Поддержка 24/7","Без предоплаты"]},
  {"id":"radical","name":"Radical Storage","domain":"radicalstorage.com","tagline":"Официальный партнёр","desc":"Международная сеть хранения в 75+ странах. Гарантия цены, страховка €3000, мгновенное подтверждение.","rating":4.8,"reviews":9800,"price":"от €4/сут","affiliate":True,"badge":"Топ-партнёр","features":["Страховка €3000","75+ стран","Гарантия цены","Моб. приложение"]},
  {"id":"luggagehero","name":"LuggageHero","domain":"luggagehero.com","tagline":"Хранение рядом с вами","desc":"Хранение вещей в магазинах, кафе и отелях города. Почасовая и суточная оплата.","rating":4.7,"reviews":7200,"price":"от €2/ч","affiliate":False,"badge":"","features":["Почасовая оплата","600+ городов","Быстрый check-in"],"url":"https://luggagehero.com"},
  {"id":"stasher","name":"Stasher","domain":"stasher.com","tagline":"Надёжные точки в городе","desc":"Сеть проверенных точек хранения: отели, магазины, рестораны. Работает в 600+ городах.","rating":4.6,"reviews":5400,"price":"от £5/сут","affiliate":False,"badge":"","features":["600+ городов","Страховка","Проверенные точки"],"url":"https://stasher.com"},
  {"id":"bounce","name":"Bounce","domain":"usebounce.com","tagline":"Хранение за 5 минут","desc":"Самое быстрое бронирование. Мобильное приложение, тысячи точек, страховка $10 000.","rating":4.7,"reviews":8100,"price":"от $5.90/сут","affiliate":False,"badge":"","features":["Страховка $10000","Мобильное приложение","Тысячи точек"],"url":"https://usebounce.com"},
  {"id":"nannybag","name":"Nannybag","domain":"nannybag.com","tagline":"Проверенные точки хранения","desc":"Партнёрская сеть кафе и отелей для хранения чемоданов. 35+ стран.","rating":4.5,"reviews":4300,"price":"от €6/сут","affiliate":False,"badge":"","features":["35+ стран","Отели и кафе","Страховка"],"url":"https://nannybag.com"},
  {"id":"vertoe","name":"Vertoe","domain":"vertoe.com","tagline":"Хранение у местных","desc":"Платформа хранения у проверенных местных хостов. Страховка до $5000.","rating":4.6,"reviews":3800,"price":"от $5/сут","affiliate":False,"badge":"","features":["Страховка $5000","Местные хосты","Гибкое расписание"],"url":"https://vertoe.com"},
  {"id":"mybaggage","name":"MyBaggage","domain":"mybaggage.com","tagline":"Хранение с доставкой","desc":"Комплексный сервис: хранение + доставка по всему миру. Удобно для студентов.","rating":4.5,"reviews":2800,"price":"от £12.99/сут","affiliate":False,"badge":"","features":["Доставка","Студентам скидка","Международный"],"url":"https://mybaggage.com"},
  {"id":"airportlocker","name":"AirportLocker","domain":"airportlocker.com","tagline":"Аэропортовые ячейки","desc":"Официальный агрегатор ячеек хранения в аэропортах 120 стран.","rating":4.6,"reviews":4500,"price":"от $4/сут","affiliate":False,"badge":"","features":["120 стран","Аэропорты","Официальный агрег."],"url":"https://airportlocker.com"},
  {"id":"raillocker","name":"RailLocker","domain":"raillocker.com","tagline":"У каждого вокзала","desc":"Агрегатор камер хранения у железнодорожных вокзалов Европы и СНГ.","rating":4.5,"reviews":3800,"price":"от €3/сут","affiliate":False,"badge":"","features":["Вокзалы Европы","СНГ","Онлайн-бронь"],"url":"https://raillocker.com"},
  {"id":"luggage-forward","name":"Luggage Forward","domain":"luggageforward.com","tagline":"Доставка и хранение","desc":"Международный сервис с хранением и доставкой прямо к отелю.","rating":4.6,"reviews":5600,"price":"от $25","affiliate":False,"badge":"","features":["Доставка к отелю","Международный","Трекинг"],"url":"https://luggageforward.com"},
  {"id":"safestay","name":"SafeStay","domain":"safestay.com","tagline":"Безопасное хранение","desc":"Хранение вещей в проверенных точках с видеонаблюдением и страховкой.","rating":4.4,"reviews":1700,"price":"от €5/сут","affiliate":False,"badge":"","features":["Видеонаблюдение","Страховка","Проверенные точки"],"url":"https://safestay.com"},
  {"id":"travelsafe","name":"TravelSafe","domain":"travelsafe.com","tagline":"Хранение с гарантией","desc":"Застрахованное хранение с гарантией возврата. 50+ городов.","rating":4.4,"reviews":1900,"price":"от €5/сут","affiliate":False,"badge":"","features":["Гарантия возврата","50+ городов","Страховка"],"url":"https://travelsafe.com"},
  {"id":"wanderstore","name":"WanderStore","domain":"wanderstore.com","tagline":"Для путешественников","desc":"Хранение для туристов с онлайн-поддержкой 24/7 и страховкой.","rating":4.4,"reviews":2100,"price":"от $5/сут","affiliate":False,"badge":"","features":["Поддержка 24/7","Страховка","Туристам"],"url":"https://wanderstore.com"},
  {"id":"tripcase","name":"TripCase","domain":"tripcase.com","tagline":"Хранение для трипа","desc":"Ориентирован на туристические маршруты. Точки у достопримечательностей.","rating":4.4,"reviews":1700,"price":"от $5/сут","affiliate":False,"badge":"","features":["У достопримечательностей","Туристические маршруты","Онлайн-бронь"],"url":"https://tripcase.com"},
  {"id":"stashbee","name":"StashBee","domain":"stashbee.com","tagline":"Хранение у соседей","desc":"P2P платформа хранения вещей у частных лиц. Страховка включена.","rating":4.2,"reviews":1100,"price":"от £4/сут","affiliate":False,"badge":"","features":["P2P","Страховка","Частные хосты"],"url":"https://stashbee.com"},
  {"id":"citylocker","name":"CityLocker","domain":"citylocker.com","tagline":"Городские ячейки","desc":"Автоматические городские ячейки хранения без очередей и регистрации.","rating":4.3,"reviews":1600,"price":"от 60 ₽/ч","affiliate":False,"badge":"","features":["Автоматические ячейки","Без регистрации","Почасовая оплата"],"url":"https://citylocker.com"},
  {"id":"smartlocker","name":"SmartLocker","domain":"smartlocker.com","tagline":"Умные ячейки","desc":"IoT-ячейки с управлением через смартфон. Открытие по QR-коду.","rating":4.5,"reviews":2300,"price":"от 70 ₽/ч","affiliate":False,"badge":"","features":["QR-открытие","IoT","Смартфон"],"url":"https://smartlocker.com"},
  {"id":"locktote","name":"LockTote","domain":"locktote.com","tagline":"Безопасные ячейки","desc":"Автоматические ячейки хранения в аэропортах и ТЦ. Защита PIN-кодом.","rating":4.4,"reviews":2200,"price":"от €3/ч","affiliate":False,"badge":"","features":["PIN-код","Аэропорты","ТЦ"],"url":"https://locktote.com"},
  {"id":"hubhag","name":"HubBag","domain":"hubbag.com","tagline":"Хабы хранения","desc":"Крупные хабы хранения рядом с транспортными узлами. Любой размер багажа.","rating":4.3,"reviews":1700,"price":"от €5/сут","affiliate":False,"badge":"","features":["Транспортные узлы","Любой размер","Онлайн-бронь"],"url":"https://hubbag.com"},
  {"id":"baghotel","name":"BagHotel","domain":"baghotel.com","tagline":"При отеле","desc":"Хранение вещей в отелях класса 3-4 звезды. Доступ 24/7.","rating":4.3,"reviews":1400,"price":"от €6/сут","affiliate":False,"badge":"","features":["Отели 3-4★","Доступ 24/7","Страховка"],"url":"https://baghotel.com"},
  {"id":"baggagestar","name":"BaggageStar","domain":"baggagestar.com","tagline":"Хранение у звёзд","desc":"Сеть точек в центрах туристических городов. Рейтинги проверены туристами.","rating":4.5,"reviews":2700,"price":"от $5/сут","affiliate":False,"badge":"","features":["Центр города","Проверенные отзывы","Онлайн-бронь"],"url":"https://baggagestar.com"},
  {"id":"stationlocker","name":"StationLocker","domain":"stationlocker.com","tagline":"Вокзальные ячейки","desc":"Официальные ячейки хранения на железнодорожных вокзалах 25 стран.","rating":4.4,"reviews":2900,"price":"от €3/сут","affiliate":False,"badge":"","features":["25 стран","Ж/д вокзалы","Официальные ячейки"],"url":"https://stationlocker.com"},
  {"id":"daytripbag","name":"DaytripBag","domain":"daytripbag.com","tagline":"На день в город","desc":"Идеален для однодневных экскурсий. Сдай вещи утром — забери вечером.","rating":4.3,"reviews":1300,"price":"от €4/сут","affiliate":False,"badge":"","features":["Однодневные туры","Удобный центр","Гибкие часы"],"url":"https://daytripbag.com"},
  {"id":"citystasher","name":"CityStasher","domain":"citystasher.com","tagline":"Мгновенное бронирование","desc":"Онлайн-бронирование в тысячах точек. Почасовая оплата, без минимального срока.","rating":4.5,"reviews":3200,"price":"от £3/ч","affiliate":False,"badge":"","features":["Тысячи точек","Без минимума","Почасовая"],"url":"https://citystasher.com"},
  {"id":"urbinetorbi","name":"Urbi et Orbi","domain":"urbi-locker.ru","tagline":"Городские камеры хранения","desc":"Автоматические камеры хранения в центрах городов России. Без предоплаты.","rating":4.3,"reviews":1200,"price":"от 80 ₽/ч","affiliate":False,"badge":"","features":["Россия","Без предоплаты","Автоматические"],"url":"https://urbi-locker.ru"},
  {"id":"bagpoint","name":"Bagpoint","domain":"bagpoint.ru","tagline":"Точки у вокзалов","desc":"Специализируется на хранении у ж/д вокзалов. Ячейки и живые точки.","rating":4.2,"reviews":1500,"price":"от 120 ₽/сут","affiliate":False,"badge":"","features":["Вокзалы России","Ячейки","Живые точки"],"url":"https://bagpoint.ru"},
  {"id":"moybagazh","name":"Мойбагаж","domain":"moybagazh.ru","tagline":"Хранение в Москве","desc":"Российский сервис хранения с точками у московского метро и вокзалов.","rating":4.3,"reviews":890,"price":"от 100 ₽/сут","affiliate":False,"badge":"","features":["Москва","У метро","У вокзалов"],"url":"https://moybagazh.ru"},
  {"id":"kladovaya","name":"Кладовая","domain":"kladovaya-spb.ru","tagline":"Хранение вещей СПб","desc":"Петербургский сервис хранения у станций метро. Работает круглосуточно.","rating":4.2,"reviews":740,"price":"от 90 ₽/ч","affiliate":False,"badge":"","features":["Санкт-Петербург","Круглосуточно","У метро"],"url":"https://kladovaya-spb.ru"},
  {"id":"chemodanchik","name":"Чемоданчик","domain":"chemodanchik.ru","tagline":"Хранение в России","desc":"Российский сервис хранения чемоданов у вокзалов и в туристических зонах.","rating":4.1,"reviews":670,"price":"от 100 ₽/сут","affiliate":False,"badge":"","features":["Россия","Вокзалы","Туристические зоны"],"url":"https://chemodanchik.ru"},
  {"id":"safetrunk","name":"SafeTrunk","domain":"safetrunk.com","tagline":"Сейф в кармане","desc":"Защищённое хранение ценных вещей и документов. Видеонаблюдение 24/7.","rating":4.6,"reviews":1800,"price":"от €7/сут","affiliate":False,"badge":"","features":["Видеонаблюдение 24/7","Ценности","Документы"],"url":"https://safetrunk.com"},
  {"id":"urbanvault","name":"UrbanVault","domain":"urbanvault.com","tagline":"Городское хранилище","desc":"Хранение в центре города с удобным доступом. 80+ мегаполисов.","rating":4.5,"reviews":3400,"price":"от €5/сут","affiliate":False,"badge":"","features":["80+ мегаполисов","Центр города","Удобный доступ"],"url":"https://urbanvault.com"},
  {"id":"trunkclub","name":"TrunkClub","domain":"trunkclub-storage.com","tagline":"Клуб путешественников","desc":"Хранение + доступ к клубному пространству с Wi-Fi и кофе. Удобно в транзите.","rating":4.4,"reviews":2600,"price":"от €8/сут","affiliate":False,"badge":"","features":["Wi-Fi","Кофе включён","Транзит"],"url":"https://trunkclub-storage.com"},
  {"id":"bagkeeper","name":"BagKeeper","domain":"bagkeeper.com","tagline":"Хранитель вещей","desc":"Хранение у проверенных партнёров в жилых кварталах. Удобно для Airbnb-туристов.","rating":4.2,"reviews":980,"price":"от €4/сут","affiliate":False,"badge":"","features":["Жилые кварталы","Airbnb-туристам","Страховка"],"url":"https://bagkeeper.com"},
  {"id":"luggagelab","name":"LuggageLab","domain":"luggagelab.com","tagline":"Инновационное хранение","desc":"Технологичный сервис с автоматическим взвешиванием и описанием вещей при сдаче.","rating":4.5,"reviews":1500,"price":"от $6/сут","affiliate":False,"badge":"","features":["Авто-взвешивание","Фото при сдаче","Технологичный"],"url":"https://luggagelab.com"},
  {"id":"cluclu","name":"CluClu","domain":"cluclu.com","tagline":"Хранение в Азии","desc":"Специализируется на Японии, Таиланде, Сингапуре. Поддержка на русском.","rating":4.5,"reviews":2100,"price":"от ¥500/сут","affiliate":False,"badge":"","features":["Япония","Таиланд","Поддержка на RU"],"url":"https://cluclu.com"},
  {"id":"bagtrans","name":"BagTrans","domain":"bagtrans.ru","tagline":"Трансфер и хранение","desc":"Комбинирует трансфер из аэропорта с хранением багажа.","rating":4.3,"reviews":980,"price":"от 200 ₽/сут","affiliate":False,"badge":"","features":["Трансфер","Аэропорт","Россия"],"url":"https://bagtrans.ru"},
  {"id":"zipbag","name":"ZipBag","domain":"zipbag.com","tagline":"Быстро и дёшево","desc":"Бюджетный сервис хранения для путешественников. Без скрытых платежей.","rating":4.1,"reviews":780,"price":"от €3/сут","affiliate":False,"badge":"","features":["Бюджетный","Без скрытых плат.","Простой"],"url":"https://zipbag.com"},
  {"id":"dropbag","name":"DropBag","domain":"dropbag.com","tagline":"Оставь и иди","desc":"Простой сервис хранения у проверенных партнёров. 30+ городов.","rating":4.1,"reviews":870,"price":"от €4/сут","affiliate":False,"badge":"","features":["30+ городов","Проверенные точки","Без регистрации"],"url":"https://dropbag.com"},
  {"id":"baggagebuddy","name":"BaggageBuddy","domain":"baggagebuddy.com","tagline":"Друг путешественника","desc":"Хранение с персональным сервисом. Рекомендует точки рядом с маршрутом.","rating":4.3,"reviews":1200,"price":"от $6/сут","affiliate":False,"badge":"","features":["Персональный сервис","По маршруту","Рекомендации"],"url":"https://baggagebuddy.com"},
  {"id":"gostore","name":"GoStore","domain":"gostore.com","tagline":"Хранение в движении","desc":"Мобильные точки хранения в туристических зонах. Сезонный сервис.","rating":4.0,"reviews":430,"price":"от €4/сут","affiliate":False,"badge":"","features":["Мобильные точки","Туристические зоны","Сезонный"],"url":"https://gostore.com"},
  {"id":"storagking","name":"StorageKing","domain":"storageking.com","tagline":"Долгосрочное хранение","desc":"Специализируется на долгосрочном хранении вещей. Удобно при переезде.","rating":4.1,"reviews":650,"price":"от €8/сут","affiliate":False,"badge":"","features":["Долгосрочное","При переезде","Крупные вещи"],"url":"https://storageking.com"},
  {"id":"cabinbag","name":"CabinBag","domain":"cabinbag.com","tagline":"Ручная кладь в надёжных руках","desc":"Специализируется на хранении ручной клади и небольших рюкзаков. Почасовая оплата.","rating":4.3,"reviews":1100,"price":"от €2/ч","affiliate":False,"badge":"","features":["Ручная кладь","Рюкзаки","Почасовая"],"url":"https://cabinbag.com"},
  {"id":"holdmybag","name":"HoldMyBag","domain":"holdmybag.com","tagline":"Держим ваш багаж","desc":"Простое и дешёвое хранение у местных партнёров. Бронирование за 2 минуты.","rating":4.2,"reviews":890,"price":"от £3/сут","affiliate":False,"badge":"","features":["Дешёвое","2 минуты","Местные партнёры"],"url":"https://holdmybag.com"},
  {"id":"travelbox","name":"TravelBox","domain":"travelbox.com","tagline":"Хранение по пути","desc":"Точки хранения на туристических маршрутах. Партнёр крупных туроператоров.","rating":4.3,"reviews":1400,"price":"от $5/сут","affiliate":False,"badge":"","features":["Туроператоры","Маршруты","Онлайн-бронь"],"url":"https://travelbox.com"},
  {"id":"oversize","name":"Oversize Baggage","domain":"oversizebaggage.com","tagline":"Крупногабаритный багаж","desc":"Специализируется на хранении крупных вещей: лыжи, велосипеды, детские коляски.","rating":4.4,"reviews":1600,"price":"от €8/сут","affiliate":False,"badge":"","features":["Лыжи","Велосипеды","Коляски"],"url":"https://oversizebaggage.com"},
  {"id":"packpoint","name":"PackPoint","domain":"packpoint.ru","tagline":"Умная упаковка и хранение","desc":"Поможет упаковать и сохранить вещи. Упаковочные материалы включены.","rating":4.2,"reviews":950,"price":"от 150 ₽/сут","affiliate":False,"badge":"","features":["Упаковка включена","Россия","Хрупкие вещи"],"url":"https://packpoint.ru"},
  {"id":"luggagelock","name":"LuggageLock","domain":"luggagelock.com","tagline":"Надёжный замок","desc":"Точки хранения у проверенных партнёров с электронными замками.","rating":4.2,"reviews":1100,"price":"от €4/сут","affiliate":False,"badge":"","features":["Электронный замок","Проверенные точки","Страховка"],"url":"https://luggagelock.com"},
  {"id":"deposito","name":"Deposito","domain":"deposito.com","tagline":"Хранение у партнёров","desc":"Итальянская сеть хранения вещей в магазинах и отелях по всей Европе.","rating":4.4,"reviews":2900,"price":"от €5/сут","affiliate":False,"badge":"","features":["Европа","Магазины и отели","Итальянская сеть"],"url":"https://deposito.com"},
  {"id":"konsierge","name":"Консьерж-хранение","domain":"concierge-storage.ru","tagline":"Премиум-хранение","desc":"VIP-сервис хранения с личным консьержем. Для делового и премиум-туризма.","rating":4.8,"reviews":520,"price":"от 500 ₽/сут","affiliate":False,"badge":"Premium","features":["VIP-сервис","Личный консьерж","Деловой туризм"],"url":"https://concierge-storage.ru"},
  {"id":"bagsaway","name":"BagsAway","domain":"bagsaway.com","tagline":"Умное хранение","desc":"Хранение багажа с доставкой и трекингом в реальном времени.","rating":4.4,"reviews":2100,"price":"от $7/сут","affiliate":False,"badge":"","features":["Трекинг real-time","Доставка","Умное хранение"],"url":"https://bagsaway.com"},
  {"id":"travelcloak","name":"TravelCloak","domain":"travelcloak.com","tagline":"Безопасно и быстро","desc":"Хранение в проверенных точках с видеонаблюдением. Страховка до €3000.","rating":4.4,"reviews":2000,"price":"от €5/сут","affiliate":False,"badge":"","features":["Видеонаблюдение","Страховка €3000","Быстрый check-in"],"url":"https://travelcloak.com"},
  {"id":"locallocker","name":"LocalLocker","domain":"locallocker.com","tagline":"Местные камеры хранения","desc":"Подборка официальных камер хранения на вокзалах и в аэропортах города.","rating":4.0,"reviews":620,"price":"от 80 ₽/ч","affiliate":False,"badge":"","features":["Вокзалы","Аэропорты","Официальные"],"url":"https://locallocker.com"},
]

# ─── МАППИНГИ ──────────────────────────────────────────────────────────────────
CITY_RU = {
    'moscow':'Москва','saint-petersburg':'Санкт-Петербург','sochi':'Сочи',
    'yekaterinburg':'Екатеринбург','kazan':'Казань','krasnodar':'Краснодар',
    'novosibirsk':'Новосибирск','krasnoyarsk':'Красноярск','irkutsk':'Иркутск',
    'vladivostok':'Владивосток','murmansk':'Мурманск','omsk':'Омск',
    'khabarovsk':'Хабаровск','perm':'Пермь','yaroslavl':'Ярославль',
    'tula':'Тула','voronezh':'Воронеж','saratov':'Саратов','volgograd':'Волгоград',
    'barnaul':'Барнаул','kaliningrad':'Калининград','stavropol':'Ставрополь',
    'belgorod':'Белгород','vladimir':'Владимир','ryazan':'Рязань','tomsk':'Томск',
    'pyatigorsk':'Пятигорск','makhachkala':'Махачкала','astrakhan':'Астрахань',
    'taganrog':'Таганрог','novorossiysk':'Новороссийск','gelendzhik':'Геленджик',
    'anapa':'Анапа','surgut':'Сургут','petrozavodsk':'Петрозаводск',
    'sortavala':'Сортавала','pskov':'Псков','kostroma':'Кострома','rybinsk':'Рыбинск',
    'vologda':'Вологда','smolensk':'Смоленск','arkhangelsk':'Архангельск',
    'ivanovo':'Иваново','kaluga':'Калуга','izhevsk':'Ижевск','cheboksary':'Чебоксары',
    'yoshkar-ola':'Йошкар-Ола','veliky-novgorod':'Великий Новгород',
    'orenburg':'Оренбург','penza':'Пенза','kirov':'Киров','novokuznetsk':'Новокузнецк',
    'kemerovo':'Кемерово','chelyabinsk':'Челябинск','blagoveshchensk':'Благовещенск',
    'ussuriysk':'Уссурийск','kirovsk':'Кировск','kaspiysk':'Каспийск',
    'vladikavkaz':'Владикавказ','nizhny-novgorod':'Нижний Новгород',
    'rostov-on-don':'Ростов-на-Дону','samara':'Самара','tumen':'Тюмень','ufa':'Уфа',
    'minsk':'Минск','dubai':'Дубай','abu-dhabi':'Абу-Даби','bangkok':'Бангкок',
    'phuket':'Пхукет','bali':'Бали','kuala-lumpur':'Куала-Лумпур','singapore':'Сингапур',
    'tbilisi':'Тбилиси','batumi':'Батуми','yerevan':'Ереван','baku':'Баку',
    'astana':'Астана','almaty':'Алматы','tashkent':'Ташкент','stanbul':'Стамбул',
    'beijing':'Пекин','guangzhou':'Гуанчжоу','shanghai':'Шанхай','hong-kong':'Гонконг',
    'tokyo':'Токио','paris':'Париж','nice':'Ницца','barcelona':'Барселона',
    'rome':'Рим','milan':'Милан','berlin':'Берлин','munich':'Мюнхен',
    'frankfurt':'Франкфурт','lisbon':'Лиссабон','belgrade':'Белград',
    'athens':'Афины','vilnius':'Вильнюс','riga':'Рига','manila':'Манила',
}
LOCATION_RU = {
    'sheremetyevo-airport':'Аэропорт Шереметьево','kazansky-railway-station':'Казанский вокзал',
    'paveletsky-railway-station':'Павелецкий вокзал','belorussky-station':'Белорусский вокзал',
    'yaroslavsky-railway-station':'Ярославский вокзал','moskovsky-railway-station':'Московский вокзал',
    'sochi-airport':'Аэропорт Сочи','vnukovo-airport-vko':'Аэропорт Внуково',
    'leningradsky-railway-station':'Ленинградский вокзал','domodedovo-airport':'Аэропорт Домодедово',
    'pulkovo':'Аэропорт Пулково','krasnodar-train-station':'ЖД вокзал',
    'kiyevsky-railway-station':'Киевский вокзал','koltsovo-airport':'Аэропорт Кольцово',
    'dubai-mall':'Дубай Молл','saint-petersburg-center':'Центр города',
    'kazan-airport':'Аэропорт Казань','kazan-station':'ЖД вокзал',
    'kursky-railway-station':'Курский вокзал','greenwich-yekaterinburg':'ТЦ Гринвич',
    'fontanka':'Фонтанка','y-station-rosa-khutor':'Роза Хутор','bangkok-airport':'Аэропорт Бангкока',
    'sochi-city-center':'Центр города','adler':'Адлер','minsk-passazhirskij':'ЖД вокзал',
    'kuala-lumpur-airport':'Аэропорт КЛ','ladozhskiy-vokzal':'Ладожский вокзал',
    'international-astana':'Аэропорт Астана','krasnaya-polyana':'Красная Поляна',
    'abu-dhabi-international-airport':'Аэропорт Абу-Даби',
    'kaliningrad-severny-northern-station':'Северный вокзал','dream-island':'Остров Мечты',
    'tashkent-airport':'Аэропорт Ташкент','krasnodar-city-bus-station':'Автовокзал',
    'novosibirsk-railway-station':'ЖД вокзал','adler-railway-station':'ЖД вокзал Адлер',
    'aviapark':'Авиапарк','dubai-airport':'Аэропорт Дубай','yekaterinburg-passazhirskiy':'ЖД вокзал',
    'moscow-city-center':'Центр Москвы','vitebsk-railway-station':'Витебский вокзал',
    'hermitage':'Эрмитаж','zelenogradsk':'Зеленоградск','zvartnots-airport':'Аэропорт Звартноц',
    'rostov-railway-station':'ЖД вокзал','baku-airport':'Аэропорт Баку','vdnh':'ВДНХ',
    'moscow-city':'Москва-Сити','tbilisi-station':'ЖД вокзал',
    'krasnodar-2-railway-station':'Краснодар-2','baltic-railway-station':'Балтийский вокзал',
    'samara-railway-station':'ЖД вокзал','ufa-railway-station':'ЖД вокзал',
    'airport-ufa':'Аэропорт Уфа','sochi-railway-station':'ЖД вокзал Сочи',
    'airport-omsk':'Аэропорт Омск','railway-station':'ЖД вокзал',
    'fiumicino-airport':'Аэропорт Фьюмичино','gorky-park':'Парк Горького',
    'ninoy-aquino-airport':'Аэропорт Манилы','sanur':'Санур',
    'moscow-rizhsky-railway-station':'Рижский вокзал','milano-centrale':'Милано Централе',
    'murmansk-airport':'Аэропорт Мурманск','murmansk-railway-station':'ЖД вокзал',
    'port-of-sochi':'Морской порт','moremall':'МореМолл',
    'severny-bus-station-yekaterinburg':'Северный автовокзал','tverskaya-street':'Тверская улица',
    'yuzhny-bus-station-yekaterinburg':'Южный автовокзал','afimall-city':'Афимолл',
    'sergiyev-posad':'Сергиев Посад','kotelniki':'Котельники','changi-airport':'Аэропорт Чанги',
    'airport-khrabrovo':'Аэропорт Храброво','tbilisi-airport':'Аэропорт Тбилиси',
    'hotel-cosmos-moscow':'Гостиница Космос','okhotny-ryad':'Охотный Ряд',
    'almaty-airport':'Аэропорт Алматы','almaty-2-station':'Алматы-2',
    'mineralnye-vody-railway-station':'ЖД вокзал Мин.Воды',
    'mineralnye-vody-airport':'Аэропорт Мин.Воды','mineralnye-vody':'Минеральные Воды',
    'pyatigorsk-railway-station':'ЖД вокзал','national-airport-minsk':'Аэропорт Минск',
    'yaroslavl-railway-station':'ЖД вокзал','sochi-bus-station':'Автовокзал',
    'sochi-promenade':'Набережная','sochi-olympic-park':'Олимпийский парк',
    'imeretinsky-kurort-station':'Имеретинский курорт','imeretinskiy-kurort':'Имеретинский курорт',
    'loo':'Лоо','tuapse':'Туапсе','galata':'Галата','istanbul-airport':'Аэропорт Стамбул',
    'sabiha-gokcen-airport':'Аэропорт Сабиха Гёкчен','istanbul-ataturk-airport':'Аэропорт Ататюрк',
    'barcelona-airport':'Аэропорт Барселона','athens-airport':'Аэропорт Афины',
    'nice-airport':'Аэропорт Ницца','frankfurt-airport':'Аэропорт Франкфурт',
    'munich-central':'Центральный вокзал','vilnius-international-airport':'Аэропорт Вильнюс',
    'riga-bus-station':'Автовокзал','minsk-bus-station':'Автовокзал',
    'toshkent-station':'ЖД вокзал','petrozavodsk-railway-station':'ЖД вокзал',
    'vyborg':'Выборг','kronstadt':'Кронштадт','peterhof':'Петергоф',
    'finland-station':'Финляндский вокзал','nevsky-prospect':'Невский проспект',
    'obninsk':'Обнинск','kislovodsk':'Кисловодск','essentuki':'Ессентуки',
    'zheleznovodsk':'Железноводск','odintsovo':'Одинцово','kolomna':'Коломна',
    'mytishchi':'Мытищи','serpukhov':'Серпухов','zvenigorod':'Звенигород',
    'red-square':'Красная площадь','alexandrovsky-garden':'Александровский сад',
    'kremlin':'Кремль','luzhniki':'Лужники','sokolniki':'Сокольники',
    'state-historical-museum':'Исторический музей','bauman-street':'Улица Баумана',
    'kaliningrad-center':'Центр Калининграда','kaliningrad-passazhirskij':'Южный вокзал',
    'kaliningrad-bus-station':'Автовокзал','svetlogorsk':'Светлогорск',
    'batumi-station':'ЖД вокзал','nizhny-novgorod-railway-station':'ЖД вокзал',
    'river-port':'Речной вокзал','samara-airport':'Аэропорт Самара',
    'pskov-railway-station':'ЖД вокзал','obvodny-kanal-bus-station':'Автовокзал Обводный канал',
    'metro-ploshchad-vosstaniya':'Площадь Восстания','kanavinsky-bus-terminal':'Автовокзал',
    'mytishchi':'Мытищи',
}
COUNTRY_MAP = {
    'moscow':'Россия','saint-petersburg':'Россия','sochi':'Россия','yekaterinburg':'Россия',
    'kazan':'Россия','krasnodar':'Россия','novosibirsk':'Россия','krasnoyarsk':'Россия',
    'irkutsk':'Россия','vladivostok':'Россия','murmansk':'Россия','omsk':'Россия',
    'khabarovsk':'Россия','perm':'Россия','yaroslavl':'Россия','tula':'Россия',
    'voronezh':'Россия','saratov':'Россия','volgograd':'Россия','barnaul':'Россия',
    'kaliningrad':'Россия','stavropol':'Россия','belgorod':'Россия','vladimir':'Россия',
    'ryazan':'Россия','tomsk':'Россия','pyatigorsk':'Россия','makhachkala':'Россия',
    'astrakhan':'Россия','taganrog':'Россия','novorossiysk':'Россия','gelendzhik':'Россия',
    'anapa':'Россия','surgut':'Россия','petrozavodsk':'Россия','sortavala':'Россия',
    'pskov':'Россия','kostroma':'Россия','rybinsk':'Россия','vologda':'Россия',
    'smolensk':'Россия','arkhangelsk':'Россия','ivanovo':'Россия','kaluga':'Россия',
    'izhevsk':'Россия','cheboksary':'Россия','yoshkar-ola':'Россия',
    'veliky-novgorod':'Россия','orenburg':'Россия','penza':'Россия','kirov':'Россия',
    'novokузnetsk':'Россия','kemerovo':'Россия','chelyabinsk':'Россия',
    'blagoveshchensk':'Россия','ussuriysk':'Россия','kirovsk':'Россия','kaspiysk':'Россия',
    'vladikavkaz':'Россия','nizhny-novgorod':'Россия','rostov-on-don':'Россия',
    'samara':'Россия','tumen':'Россия','ufa':'Россия','novokuznetsk':'Россия',
    'minsk':'Беларусь','dubai':'ОАЭ','abu-dhabi':'ОАЭ','bangkok':'Таиланд',
    'phuket':'Таиланд','bali':'Индонезия','kuala-lumpur':'Малайзия','singapore':'Сингапур',
    'tbilisi':'Грузия','batumi':'Грузия','yerevan':'Армения','baku':'Азербайджан',
    'astana':'Казахстан','almaty':'Казахстан','tashkent':'Узбекистан','stanbul':'Турция',
    'beijing':'Китай','guangzhou':'Китай','shanghai':'Китай','hong-kong':'Китай',
    'tokyo':'Япония','paris':'Франция','nice':'Франция','barcelona':'Испания',
    'rome':'Италия','milan':'Италия','berlin':'Германия','munich':'Германия',
    'frankfurt':'Германия','lisbon':'Португалия','belgrade':'Сербия','athens':'Греция',
    'vilnius':'Литва','riga':'Латвия','manila':'Филиппины',
}
FLAG_MAP = {
    'Россия':'🇷🇺','ОАЭ':'🇦🇪','Беларусь':'🇧🇾','Таиланд':'🇹🇭','Индонезия':'🇮🇩',
    'Малайзия':'🇲🇾','Сингапур':'🇸🇬','Грузия':'🇬🇪','Армения':'🇦🇲',
    'Азербайджан':'🇦🇿','Казахстан':'🇰🇿','Узбекистан':'🇺🇿','Турция':'🇹🇷',
    'Китай':'🇨🇳','Япония':'🇯🇵','Франция':'🇫🇷','Испания':'🇪🇸','Италия':'🇮🇹',
    'Германия':'🇩🇪','Португалия':'🇵🇹','Сербия':'🇷🇸','Греция':'🇬🇷',
    'Литва':'🇱🇹','Латвия':'🇱🇻','Филиппины':'🇵🇭',
}
COUNTRY_SLUG = {
    'Россия':'russia','ОАЭ':'uae','Беларусь':'belarus','Таиланд':'thailand',
    'Индонезия':'indonesia','Малайзия':'malaysia','Сингапур':'singapore',
    'Грузия':'georgia','Армения':'armenia','Азербайджан':'azerbaijan',
    'Казахстан':'kazakhstan','Узбекистан':'uzbekistan','Турция':'turkey',
    'Китай':'china','Япония':'japan','Франция':'france','Испания':'spain',
    'Италия':'italy','Германия':'germany','Португалия':'portugal','Сербия':'serbia',
    'Греция':'greece','Литва':'lithuania','Латвия':'latvia','Филиппины':'philippines',
}

def city_in(city_ru):
    custom = {
        'Москва':'в Москве','Санкт-Петербург':'в Санкт-Петербурге',
        'Казань':'в Казани','Астана':'в Астане','Алматы':'в Алматы',
        'Сочи':'в Сочи','Дубай':'в Дубае','Бангкок':'в Бангкоке',
        'Пхукет':'на Пхукете','Бали':'на Бали','Сингапур':'в Сингапуре',
        'Тбилиси':'в Тбилиси','Батуми':'в Батуми','Ереван':'в Ереване',
        'Баку':'в Баку','Ташкент':'в Ташкенте','Минск':'в Минске',
        'Стамбул':'в Стамбуле','Токио':'в Токио','Париж':'в Париже',
        'Барселона':'в Барселоне','Рим':'в Риме','Милан':'в Милане',
        'Берлин':'в Берлине','Мюнхен':'в Мюнхене','Франкфурт':'во Франкфурте',
        'Лиссабон':'в Лиссабоне','Белград':'в Белграде','Афины':'в Афинах',
        'Вильнюс':'в Вильнюсе','Рига':'в Риге','Манила':'в Маниле',
        'Екатеринбург':'в Екатеринбурге','Краснодар':'в Краснодаре',
        'Новосибирск':'в Новосибирске','Красноярск':'в Красноярске',
        'Иркутск':'в Иркутске','Владивосток':'во Владивостоке',
        'Мурманск':'в Мурманске','Омск':'в Омске','Хабаровск':'в Хабаровске',
        'Пермь':'в Перми','Ярославль':'в Ярославле','Калининград':'в Калининграде',
        'Нижний Новгород':'в Нижнем Новгороде','Ростов-на-Дону':'в Ростове-на-Дону',
        'Самара':'в Самаре','Уфа':'в Уфе','Воронеж':'в Воронеже',
        'Волгоград':'в Волгограде','Саратов':'в Саратове',
        'Пятигорск':'в Пятигорске','Геленджик':'в Геленджике',
        'Анапа':'в Анапе','Новороссийск':'в Новороссийске',
        'Тула':'в Туле','Рязань':'в Рязани','Псков':'в Пскове',
        'Кострома':'в Костроме','Смоленск':'в Смоленске','Вологда':'в Вологде',
        'Томск':'в Томске','Барнаул':'в Барнауле','Кемерово':'в Кемерово',
        'Челябинск':'в Челябинске','Тюмень':'в Тюмени','Иваново':'в Иванове',
        'Калуга':'в Калуге','Ижевск':'в Ижевске','Петрозаводск':'в Петрозаводске',
        'Пекин':'в Пекине','Шанхай':'в Шанхае','Гонконг':'в Гонконге',
        'Куала-Лумпур':'в Куала-Лумпуре','Ницца':'в Ницце',
    }
    if city_ru in custom:
        return custom[city_ru]
    if city_ru.endswith('а'): return f'в {city_ru[:-1]}е'
    if city_ru.endswith('я'): return f'в {city_ru[:-1]}е'
    if city_ru.endswith('ь'): return f'в {city_ru[:-1]}и'
    return f'в {city_ru}'

INFO_VARIANTS = [
    lambda city, loc: f"""<h2>Камеры хранения {city}: полный гид</h2>
<p>{city} — один из городов, где вопрос хранения багажа стоит особенно остро в туристический сезон. 
Независимо от того, прилетели вы в {city} транзитом или только что заселились в отель, 
сервисы хранения позволят вам свободно перемещаться по городу без чемоданов.</p>
<p>На этой странице собраны лучшие сервисы хранения {city if not loc else loc}, 
отсортированные по рейтингу и отзывам реальных пользователей.</p>
<h3>Где хранить чемодан в {city}?</h3>
<ul>
<li>Автоматические ячейки на вокзалах и в аэропортах</li>
<li>Партнёрские точки в магазинах, кафе и отелях</li>
<li>Специализированные пункты хранения с персоналом</li>
<li>P2P хосты через приложение (дешевле всего)</li>
</ul>""",
    lambda city, loc: f"""<h2>Как выбрать камеру хранения в {city}?</h2>
<p>При выборе сервиса хранения багажа в {city} обратите внимание на расстояние до вашего маршрута, 
режим работы и наличие страховки. Онлайн-сервисы обычно выгоднее и удобнее классических камер хранения на вокзале.</p>
<h3>Что важно при бронировании?</h3>
<ul>
<li>Страховка — минимум €1000 на случай кражи или потери</li>
<li>Режим работы — убедитесь, что точка открыта в нужное время</li>
<li>Расстояние от вашего маршрута — выбирайте ближайшую точку</li>
<li>Отзывы — смотрите рейтинг конкретной точки, не только сервиса</li>
<li>Оплата — большинство сервисов принимают карты и PayPal</li>
</ul>
<p>Рекомендуем бронировать заранее, особенно в сезон: в {city} популярные точки быстро заполняются.</p>""",
]

TIPS_VARIANTS = [
    lambda city: f"""<h3>Советы по хранению багажа в {city}</h3>
<ul>
<li>Бронируйте за несколько часов до прибытия — это гарантирует место</li>
<li>Сфотографируйте вещи перед сдачей на хранение</li>
<li>Уточните режим работы точки при онлайн-бронировании</li>
<li>Выбирайте сервисы со страховкой на случай форс-мажора</li>
<li>Для крупного багажа (лыжи, велосипеды) выбирайте специализированные точки</li>
</ul>""",
    lambda city: f"""<h3>Цены на хранение в {city}</h3>
<ul>
<li>Почасовая оплата — от 60–80 ₽/час (или €2–3/час)</li>
<li>Суточный тариф — от 150–300 ₽/сутки (или €4–6/сутки)</li>
<li>Автоматические ячейки на вокзале — обычно дороже на 20–30%</li>
<li>P2P-сервисы (StashBee, BagKeeper) — дешевле всего</li>
<li>Партнёрские сервисы (Qeepl, Radical) — лучшее соотношение цены и надёжности</li>
</ul>""",
]

def parse_qeepl_slug(url):
    m = re.search(r'/luggage-storage/([^?&#]+)', str(url))
    return m.group(1) if m else ''

def load_pages():
    wb = openpyxl.load_workbook(KEYS_FILE)
    ws = wb.active
    pages = []
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if not r[0]:
            continue
        qurl = str(r[1] or QEEPL_DEFAULT)
        rurl = str(r[2] or RADICAL_DEFAULT)
        qslug = parse_qeepl_slug(qurl)
        parts = qslug.split('/')
        city_slug = parts[0] if parts else ''
        loc_slug  = parts[1] if len(parts) > 1 else ''
        city_ru   = CITY_RU.get(city_slug, city_slug.replace('-',' ').title())
        loc_ru    = LOCATION_RU.get(loc_slug, loc_slug.replace('-',' ').title() if loc_slug else '')
        country   = COUNTRY_MAP.get(city_slug, 'Неизвестно')
        page_slug = f"{city_slug}-{loc_slug}" if loc_slug else city_slug
        pages.append({
            'query': r[0], 'city': city_ru, 'location': loc_ru,
            'city_slug': city_slug, 'loc_slug': loc_slug, 'page_slug': page_slug,
            'country': country, 'flag': FLAG_MAP.get(country,'🌍'),
            'country_slug': COUNTRY_SLUG.get(country, country.lower()),
            'qeepl_url': qurl, 'radical_url': rurl,
        })
    return pages

def make_stars(rating):
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return '★' * full + ('½' if half else '') + '☆' * empty

def build_service_cards(page, count=None):
    rnd = random.Random(hash(page['page_slug']))
    if count is None:
        count = rnd.randint(14, 20)
    aff_services = [s for s in SERVICES if s.get('affiliate')]
    pool = [s for s in SERVICES if not s.get('affiliate')]
    chosen = rnd.sample(pool, min(count - len(aff_services), len(pool)))
    services = []
    for s in aff_services:
        sc = s.copy()
        sc['ref_url'] = page['qeepl_url'] if sc['id'] == 'qeepl' else page['radical_url']
        services.append(sc)
    for s in chosen:
        sc = s.copy()
        sc['ref_url'] = sc.get('url', '#')
        services.append(sc)

    cards = []
    for i, s in enumerate(services, 1):
        is_aff = s.get('affiliate', False)
        aff_cls = ' is-affiliate' if is_aff else ''
        badge_html = ''
        if s.get('badge'):
            badge_html += f'<span class="badge badge-primary">{s["badge"]}</span>'
        if is_aff:
            badge_html += '<span class="badge badge-accent">Партнёр</span>'
        features_html = ''
        if s.get('features'):
            features_html = '<div class="service-features" style="display:flex;flex-wrap:wrap;gap:4px;margin-top:8px;">'
            for feat in s['features']:
                features_html += f'<span class="tag" style="font-size:0.7rem;padding:2px 8px;">{feat}</span>'
            features_html += '</div>'
        discount_html = '<span class="service-discount">Скидка по партнёрской ссылке</span>' if is_aff else ''
        btn_cls = 'btn-primary btn-lg' if is_aff else 'btn-ghost'
        btn_label = 'Забронировать →' if is_aff else f'На сайт {s["domain"]} →'
        rel = 'noopener sponsored' if is_aff else 'noopener noreferrer'
        link_attr = f'data-href="{s["ref_url"]}" href="{s["ref_url"]}"' if is_aff else f'href="{s["ref_url"]}"'
        cards.append(f'''<article class="service-card{aff_cls}">
  <div class="service-num">{i}</div>
  <div class="service-body">
    <div class="service-head">
      <span class="service-name">{s["name"]}</span>{badge_html}
    </div>
    <p class="service-tagline">{s["tagline"]}</p>
    <p class="service-desc">{s["desc"]}</p>
    {features_html}
    <div class="service-meta">
      <span class="rating">{make_stars(s["rating"])} {s["rating"]}
        <span class="rating-count">({s["reviews"]:,} отзывов)</span>
      </span>
      <span class="service-price">{s["price"]}</span>
      {discount_html}
    </div>
  </div>

  <div class="service-cta">
    <a {link_attr} class="btn {btn_cls}" target="_blank" rel="{rel}">{btn_label}</a>
  </div>
</article>''')
    return '\n'.join(cards), len(services)

def build_nearby_cards(page, all_pages):
    if page['loc_slug']:
        pool = [p for p in all_pages
                if p['city_slug'] == page['city_slug']
                and p['page_slug'] != page['page_slug']]
    else:
        pool = [p for p in all_pages
                if p['country'] == page['country']
                and p['city_slug'] != page['city_slug']]

    rnd = random.Random(hash(page['page_slug']))
    rnd.shuffle(pool)
    chosen = pool[:12]

    if not chosen:
        return ''

    cards = []
    for p in chosen:
        label = p['location'] if p['location'] else p['city']
        price = 'от 149 ₽' if p['country'] == 'Россия' else 'от €4'
        cards.append(f'''<a href="/pages/{p["page_slug"]}" class="city-card">
  <span class="city-card-flag">{p["flag"]}</span>
  <div class="city-card-body">
    <span class="city-card-name">{label}</span>
    <span class="city-card-country">{p["country"]}</span>
    <span class="city-card-count">14 сервисов</span>
  </div>
  <span class="city-card-price">{price}</span>
  <svg class="city-card-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
</a>''')

    return '\n'.join(cards)

def build_city_tags(page, all_pages):
    cities = {}
    for p in all_pages:
        if p['city_slug'] not in cities:
            cities[p['city_slug']] = {'name': p['city']}

    tags = []
    for city_slug, info in sorted(cities.items(), key=lambda x: x[1]['name']):
        active = ' aria-current="true"' if city_slug == page['city_slug'] and not page['loc_slug'] else ''
        tags.append(
            f'<a href="/pages/{city_slug}" class="tag tag-link"{active}>{info["name"]}</a>'
        )

    return '<div class="tags">' + '\n'.join(tags) + '</div>'
def build_nearby_city_links(page, allpages):
    seen = set()
    tags = []
    for p in allpages:
        slug = p['city_slug']
        if slug == page['city_slug']:
            continue
        if slug in seen:
            continue
        seen.add(slug)
        tags.append(
            f'<a href="/pages/{slug}" class="tag tag-link">{p["city"]}</a>'
        )
        if len(tags) >= 20:
            break
    return f'<div class="tags">{"".join(tags)}</div>'
def build_faq(city_ru, location_ru):
    city_in_form = city_in(city_ru)
    items = [
        (
            f'Как оставить багаж {city_in_form}?',
            f'Забронируйте место онлайн через Qeepl или Radical Storage, '
            f'выберите удобную точку {city_in_form} и сдайте вещи по QR-коду или коду бронирования. '
            f'Процесс занимает 2–5 минут.'
        ),
        (
            f'Сколько стоит хранение багажа {city_in_form}?',
            f'Цены начинаются от 149 ₽/сут для российских городов и от €4/сут для зарубежных. '
            f'Онлайн-сервисы, как правило, дешевле камер хранения на вокзале.'
        ),
        (
            f'Есть ли страховка при хранении {city_in_form}?',
            f'Да. Qeepl включает страховку до €5000, Radical Storage — до €3000. '
            f'Страховка входит в стоимость бронирования без доплат.'
        ),
        (
            f'Где лучше сдать чемодан {city_in_form}: на вокзале или онлайн?',
            f'Онлайн-сервисы удобнее: больше точек по городу, ниже цена, '
            f'страховка и бронирование без очередей. '
            f'Камеры на вокзале подходят, если нет времени бронировать заранее.'
        ),
        (
            f'Можно ли оставить крупный багаж {city_in_form}?',
            f'Большинство сервисов принимают чемоданы любого размера. '
            f'Для негабаритных вещей (лыжи, велосипеды, коляски) уточняйте условия '
            f'при бронировании — часть точек берёт доплату за oversized.'
        ),
    ]
    html = ''
    for i, (q, a) in enumerate(items):
        faq_id = f'faq-answer-{i}'
        html += (
            f'<div class="faq-item" itemscope itemprop="mainEntity" '
            f'itemtype="https://schema.org/Question">'
            f'<button class="faq-question" aria-expanded="false" '
            f'aria-controls="{faq_id}" itemprop="name">'
            f'{q}'
            f'<svg class="faq-icon" width="16" height="16" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="2">'
            f'<path d="M6 9l6 6 6-6"/></svg>'
            f'</button>'
            f'<div class="faq-answer" id="{faq_id}" hidden '
            f'itemscope itemprop="acceptedAnswer" '
            f'itemtype="https://schema.org/Answer">'
            f'<p itemprop="text">{a}</p>'
            f'</div></div>\n'
        )
    return html


def build_schema_items(services_data, page):

    # Получаем список сервисов для JSON-LD
    items = []
    for i, s in enumerate(services_data[:10], 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": s["name"],
            "url": s.get("ref_url", s.get("url", "#"))
        })
    return json.dumps(items, ensure_ascii=False)

# ─── ЗАГРУЗКА ШАБЛОНА ─────────────────────────────────────────────────────────
template_html = Path(TEMPLATE_FILE).read_text(encoding='utf-8')

# Вырезаем template-fragments (BEGIN ... END блоки) — они не нужны в финальном HTML
template_html = re.sub(
    r'<!--\s*BEGIN\s+\w+.*?END\s+\w+\s*-->',
    '', template_html, flags=re.DOTALL
)

def render_page(page, all_pages):
    # Собираем карточки сервисов
    cards_html, svc_count = build_service_cards(page)
    
    # Вариации контента (зависят от slug)
    rnd = random.Random(hash(page['page_slug']))
    info_fn  = rnd.choice(INFO_VARIANTS)
    tips_fn  = rnd.choice(TIPS_VARIANTS)
    
    entity     = page['location'] if page['location'] else page['city']
    title_full = f"{page['city']} — {page['location']}" if page['location'] else page['city']
    
    # Breadcrumbs
    if page['location']:
        bc_items = (
            f'<li><a href="/">Главная</a></li>'
            f'<li><span class="bc-sep"> › </span></li>'
            f'<li><a href="/pages/{page["city_slug"]}">{page["city"]}</a></li>'
            f'<li><span class="bc-sep"> › </span></li>'
            f'<li aria-current="page">{page["location"]}</li>'
        )
    else:
        bc_items = (
            f'<li><a href="/">Главная</a></li>'
            f'<li><span class="bc-sep"> › </span></li>'
            f'<li aria-current="page">{page["city"]}</li>'
        )

    # Собираем все переменные
    vars = {
        'LANG': 'ru',
        'COUNTRY_NAME': title_full,
        'META_TITLE': f'Камера хранения {title_full} — сравнение {svc_count} сервисов | КамераХранения.guide',
        'META_DESC': f'Сравните {svc_count} сервисов хранения багажа: {title_full}. Цены от 149 ₽, отзывы, страховка, онлайн-бронирование через Qeepl и Radical Storage.',
        'META_KEYWORDS': f'камера хранения {page["city"]}, хранение багажа {page["city"]}, {entity} хранение чемоданов, Qeepl {page["city"]}, Radical Storage {page["city"]}',
        'CANONICAL_URL': f'{BASE_URL}/pages/{page["page_slug"]}',
        'SCHEMA_LIST_NAME': f'Камеры хранения {title_full}',
        'SERVICE_COUNT': str(svc_count),
        'SCHEMA_ITEMS': '[]',  # заполняется ниже
        'CITY_NAME': page['city'],
        'LOCATION_NAME': page['location'] or page['city'],
        'ASSETS_PATH': '../assets/',
        'HOME_URL': '/',
        'BASE_URL': BASE_URL,
        'COUNTRY_FLAG': page['flag'],
        'H1_PART1': 'Камера хранения',
        'H1_PART2': f' {page["location"]}' if page['location'] else '',
        'HERO_LEAD': f'Сравните {svc_count} проверенных сервисов хранения багажа. Цены, отзывы и онлайн-бронирование.',
        'UPDATED_DATE': TODAY,
        'UPDATED_ISO': TODAY_ISO,
        'PRICE_FROM': '149 ₽' if page['country'] == 'Россия' else '€4',
        'AVG_RATING': '4.6',
        'LOCATIONS_NEARBY': str(min(5, len([p for p in all_pages if p['city_slug'] == page['city_slug'] and p['page_slug'] != page['page_slug']]))),
        'QEEPL_REF_URL': page['qeepl_url'],
        'RADICAL_REF_URL': page['radical_url'],
        'SERVICE_CARDS_HTML': cards_html,
        'INFO_TEXT_BLOCK': info_fn(page['city'], page['location']),
        'TIPS_TEXT_BLOCK': tips_fn(page['city']),
        'NEARBY_CITY_CARDS_HTML': build_nearby_cards(page, all_pages),
        'NEARBY_CITY_CARDS': build_nearby_cards(page, all_pages),
        'FAQ_ITEMS_HTML': '',
        'BREADCRUMB_ITEMS': bc_items,
        'YEAR': YEAR,
        'PAGE_ENTITY_NAME': entity,
        'BREADCRUMB_LAST': entity,
        'CITY_IN': city_in(page['city']),
        'CITY_TAG_LINKS_HTML': build_city_tags(page, all_pages),
        'CITY_TAG_LINKS': build_city_tags(page, all_pages),
        'NEARBY_CITY_TAG_LINKS': build_nearby_city_links(page, all_pages),
    }

    html = template_html
    for key, val in vars.items():
        html = html.replace('{{' + key + '}}', str(val))

    # Убираем незаменённые плейсхолдеры (если остались)
    html = re.sub(r'\{\{[A-Z_]+\}\}', '', html)
    return html

# ─── ЗАПУСК ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    pages = load_pages()
    print(f"📋 Загружено строк: {len(pages)}")

    generated, skipped = 0, 0
    seen_slugs = {}

    for page in pages:
        slug = page['page_slug']
        if not slug or slug in seen_slugs:
            skipped += 1
            continue
        seen_slugs[slug] = True

        html = render_page(page, pages)
        out = OUTPUT_DIR / f"{slug}.html"
        out.write_text(html, encoding='utf-8')
        generated += 1
        if generated % 50 == 0:
            print(f"  ✅ {generated} страниц...")

    print(f"\n✅ Сгенерировано: {generated} страниц → /pages/")
    print(f"⏭  Дублей пропущено: {skipped}")

    # sitemap.xml
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += f'  <url><loc>{BASE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
    for slug in seen_slugs:
        sitemap += f'  <url><loc>{BASE_URL}/pages/{slug}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
    sitemap += '</urlset>'
    Path('sitemap.xml').write_text(sitemap, encoding='utf-8')
    print(f"✅ sitemap.xml — {len(seen_slugs)+1} URL")