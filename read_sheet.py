import gspread
import psycopg2
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import time
from notifiers import get_notifier
from TOKEN import token, chatId

# Чтобы запустить программу введите в терминал powershell: python3 read_sheet.py run. Убедитесь что у вас установлен python3. 

# Импортирую все нужные модули. Для получения данных использовал Google Drive и Google Sheets API и модули как: gspread,
# BeautifulSoap, urllib.request. Для отправки сообщений в Телеграме использовал модуль notifiers и в отдельном файле внес токен бота.

# Нужно в pgAdmin создать БД с именем "supplymanagement", и таблицу с именем sheet_data где будет 5 колонок:
# 1) №,
# 2) order_№,
# 3) price_in_dollars,
# 4) delivery_date,
# 5) price_in_rubles
# Или, вы можете изменить свои данные в коде как захотите.


conn = psycopg2.connect(dbname="supplymanagement", user="postgres", password="12345678")
cur = conn.cursor()  # Коннектим БД Postgres 

passed_dates = ['2000-01-01',
                '2001-01-01']  # Это нужно для того, чтобы в программе где есть SELECT (снизу) не было никаких ошибок.
# Необходимо для проверки условии.

# Запускаем бесконечный цикл (Программа будет работать в режиме рального времени)
check_updating = 0
while True:
    cur.execute("SELECT COUNT(№) FROM sheet_data")  # Нужно для того, чтобы проверить запускалась ли раньше программа. Иначе данные дублируются.
    data = cur.fetchone()
    for i in data:
        if i > 1:
            check_updating = 1

    now = date.today()
    today_date = now.strftime("%d/%m/%Y")
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={today_date}'  # Вставляем в ссылку текущую дату, и получаем актуальную информацию по валютам.
    lst = []
    req = urllib.request.urlopen(url)
    xml = BeautifulSoup(req, "xml")
    for item in xml.find_all('Valute')[10]:
        lst.append(item.text)  # С помощью библиотек urllib, BeautifulSoap получаем данные с xml файла
    str_current_course = lst[4]
    current_course = int(str_current_course[:2])

    service_acc = gspread.service_account(filename="keys.json")  # Модуль gspread для подключения Sheets API к Python.
    # keys.json который нам сгенерировал Гугл вставляем в качестве аргумента
    sheet = service_acc.open("Supply management")

    scrap_prices_lst = []
    ruble_prices_lst = []
    work_sheet = sheet.worksheet("Supply Data")  # Открываем нашу таблицу
    dollar_prices = work_sheet.get('C2:C51')

    for lst_scrap in dollar_prices:
        for price in lst_scrap:
            scrap_prices_lst.append(price)  # Данные в виде listed list закидываем в for, чтобы получить чистый int.

    e_cloumn = 2  # В таблице данные нужны с колонки номер 2.
    for dol_price in scrap_prices_lst:
        ruble_price = int(dol_price) * float(current_course)
        work_sheet.update(f'E{e_cloumn}', ruble_price)
        ruble_prices_lst.append(ruble_price)
        e_cloumn += 1  # С помощью for и команды update мы обноваляем данные в таблице в Столбик E.

    all_data = work_sheet.get('B2:D51')
    counting = 1
    if check_updating == 0:
        for column_data in all_data:
            cur.execute(
                "INSERT INTO sheet_data (order_№, price_in_dollars, delivery_date, price_in_rubles) VALUES (%s, %s, %s, %s)",
                (column_data[0], int(column_data[1]), column_data[2], int(ruble_prices_lst[0])))
            conn.commit()
            ruble_prices_lst.pop(0)  # Берем все данные кроме столбца А т.к это type serial, и распаковываем листы, вставляем данные в нашу Таблицу в БД.
    else: # Если цикл уже был один раз, то следующие разы нужно не вставлять новые значения, а обновлять. Поэтому было сделано условие.
        for column_data in all_data:
            date_time_obj = datetime.strptime(column_data[2], "%d.%m.%Y")
            date_time_obj = date_time_obj.strftime("%Y-%m-%d")  # Форматируем дату с таблицы.
            cur.execute(f"UPDATE sheet_data SET order_№ = {column_data[0]}, price_in_dollars = {int(column_data[1])}, delivery_date = '{date_time_obj}',price_in_rubles = {int(ruble_prices_lst[0])} WHERE № = {counting}")
            conn.commit()
            ruble_prices_lst.pop(0)
            counting += 1

    now = date.today()
    today_date = now.strftime("%Y-%m-%d")  # Еще раз создаем текущую дату, потому что тут нужен другой формат даты (с -)
    message = 'Срок поставки прошел.'
    check_len = len(passed_dates)
    for_len = len(passed_dates)  # Нужно для сравнения, стало ли больше просроченных заказов.
    cur.execute(
        f"SELECT delivery_date FROM sheet_data WHERE delivery_date <= '{today_date}' AND delivery_date NOT IN {tuple(passed_dates)}")

    # Делаем выборку SELECT с проверкой просроченности.

    past_dates = cur.fetchall()
    for past_date in past_dates:
        passed_dates.append(str(past_date[0]))  # Забираем новые результаты.
        for_len = len(passed_dates)  # Задаем новое значение длины листа просроченных заказов. Если стало больше, то отправится сообщение в ТГ.
    conn.commit()
    if for_len > check_len:
        telegram = get_notifier('telegram')
        telegram.notify(token=token, chat_id=chatId, message=message)  # Отправляем сообщение в ТГ.
        time.sleep(200)
    else:
        time.sleep(200)  # Ждем несколько минут, и цикл опять повторится. Нужно чтобы не перегружать систему.