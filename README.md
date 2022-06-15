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

# Для управления Web scraping and autoupdating of data from sheet.

You need to download the zip file and unpack for using this.
You need VSCode, pgAdmin and Docker (if you want) for running this application. Also, please, install the python and pip if you didn't.

cd Folder (supplymanagement and valute_website, for each of these folders)
--> Create a virtual environment :

# Let's install virtualenv first in folders (supplymanagement and valute_website, for each of these folders)
pip install virtualenv

# Then we create our virtual environment
virtualenv envname
--> Activate the virtual environment :

envname\scripts\activate
--> Install the requirements :

# For supplymanagement:

Then, please, install all the libraries from the code (pip install "module"):
gspread
psycopg2
datetime
bs4
urllib.request
time
notifiers
docker

In the code, I commented some things that you should do (For example, in file TOKEN, you need to insert your own bot). Please, follow them before run the program.

Running the App
--> To run the App, we use :
You can run app with command python read_sheet.py run or just click the run button in right top of VS Code.
Also, you can run with docker. You need to build image with: docker build -t imagename .
Then, for running: docker run imagename
You can watch the changes in google sheets (link on the top of README) and in pgAdmin. 

# For valute_website

Running the App
--> To run the App, we use :

python manage.py runserver
⚠ Then, the development server will be started at http://127.0.0.1:8000/:
