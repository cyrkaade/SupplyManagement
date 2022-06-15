Google Sheets: https://docs.google.com/spreadsheets/d/1V4Dw4olHogEPwhoD4bMy52kn0GUYQdf2Fgj7HzUNmO0/edit#gid=0

Web Scraping и Автообновление данных.

Для использования этого вам необходимо загрузить zip-файл и распаковать его.
Для запуска этого приложения вам нужны VSCode, pgAdmin и Docker (если хотите). Кроме того, пожалуйста, установите python и pip, если вы этого не сделали.

папка cd (supplymanagement и valute_website для каждой из этих папок)
--> Создать виртуальную среду :

# Давайте сначала установим virtualenv в папки (supplymanagement и valute_website для каждой из этих папок)
pip install virtualenv

# Затем мы создаем нашу виртуальную среду
virtualenv envname
--> Активировать виртуальную среду :

envname\Scripts\activate
--> Установите требования :

# Для управления поставками:

# Затем, пожалуйста, установите все библиотеки из кода (pip install "module"):
gspread
psycopg2
datetime
bs4
urllib.
time
notifiers
docker

В коде я прокомментировал некоторые вещи, которые вы должны сделать (например, в file TOKEN вам нужно вставить своего собственного бота). Пожалуйста, следуйте им, прежде чем запускать программу.

Запуск приложения
--> Для запуска приложения мы используем :
Вы можете запустить приложение с помощью команды python read_sheet.py run или просто нажмите кнопку run в правом верхнем углу VS Code.
Кроме того, вы можете работать с docker. Вам нужно создать образ с помощью: docker build -t imagename .
Затем для запуска: docker run imagename
Вы можете следить за изменениями в Google таблицах (ссылка вверху README) и в pgAdmin. 

# Для valute_website

Запуск приложения
--> Для запуска приложения мы используем :

python manage.py runserver
⚠ Затем сервер разработки будет запущен по адресу http://127.0.0.1:8000/
