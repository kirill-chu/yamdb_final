[![yamdb_workflow](https://github.com/kirill-chu/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=main)](https://github.com/kirill-chu/yamdb_final/actions/workflows/yamdb_workflow.yml)

# api_yamdb

Учебный проект от яндекс.практикум. Спринт 13.

### Как запустить проект на тестовом сервере django:
- Клонировать репозиторий и перейти в него в командной строке.
- Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv 
source env/bin/activate
```

- Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

- Выполнить миграции:
```
python3 manage.py migrate
```

-  Создать супер-пользователя для администоирования
```
python3 manage.py createsuperuser
```

- Запустить проект:
```
python3 manage.py runserver
```
- Для администрирования пройдите по ссылке `http://127.0.0.1:8000/admin/` и воспользуйтесь ранее созданной учетной записью супер-пользователя.
- По ссылке `http://127.0.0.1/redoc:8000/` располагается Документация к проекту в которой вы можете посмотреть стандарнтные HTTP-запросы и ответы.

### Как запустить проект в контейнере
- Клонировать репозиторий и перейти в него в командной строке.
- Перейдите в дирректоию `infra` в ней располагается `docker-compose.yaml` файл.
- Переименуйте файл `example.env` в `.env`.
- В дирректории выполните команду
```
docker-compose up -d
```
Проект запущен и готов, но для полноценной работы выполните миграции и предварительные настройки:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
- Для администрирования пройдите по ссылке `http://127.0.0.1/admin/` и воспользуйтесь ранее созданной учетной записью супер-пользователя.
- По ссылке `http://127.0.0.1/redoc/` располагается Документация к проекту в которой вы можете посмотреть стандарнтные HTTP-запросы и ответы.

### Настройки для подключения к базе данных
В директории infra находится пример файла `.env` `example.env` внесите в него необходимые учетные данные для подключения к БД, переименуйте в `.env` и пересобирите проект.

Шаблон `.env`
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 

Для остановки сервисов и удаления контейнеров выполните команду:
```
docker-compose down -v
```

```
Для пересборки проекта используйте команду:
```
docker-compose -up -d --build
```

### Заполнение базы тестовыми данными
В директории `infra` располагается файл `fixtures.json` в нем находятся тестовые данные. Чтобы внести их в базу выполните команду:
```
cat  fixtures.json | docker-compose exec -T web python manage.py loaddata --format=json -
```

### Deploy при помощи git actions
Форкните проект.
Подготовьте сервер для деплоя.
Установить на него docker.io и docker compose официальная документация доступна здесь: https://docs.docker.com/compose/install/
Скопируйте все данные из `infra` в `home/<ваш_username>/` на подготовленном сервере.
Создайте необходимые secrets в проекте, которые встречаются в `yamdb_workflow.yml`.
После пуша в ветку `main` будет происходить yamdb_workflow деплой, и телеграм оповещение.
