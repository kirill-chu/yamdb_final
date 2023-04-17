api_yamdb

Как запустить проект:
- Клонировать репозиторий и перейти в него в командной строке.
- Cоздать и активировать виртуальное окружение:
    python3 -m venv venv source env/bin/activate

- Установить зависимости из файла requirements.txt:
    python3 -m pip install --upgrade pip pip install -r requirements.txt

- Выполнить миграции:
    python3 manage.py migrate

- Для заполнения базы данных из CSV-файлов выполните команду:
    python3 manage.py filldatabase

- Запустить проект:
    python3 manage.py runserver


По ссылке http://127.0.0.1:8000/redoc/ располагается Документация к проекту в которой вы можете посмотреть стандарнтные HTTP-запросы и ответы.
