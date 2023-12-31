# Resource Manager API

Resource Manager API - это веб-приложение, которое предоставляет API для управления данными о ресурсах и типах ресурсов. Приложение использует PostgreSQL и psycopg2 в качестве базы данных и разработано на Python без использования фреймворков и сторонних библиотек.

## Установка и запуск

1. Убедитесь, что PostgreSQL установлен на вашем компьютере. Если он не установлен, вы можете скачать и установить его с официального сайта PostgreSQL: https://www.postgresql.org/download/

2. После установки PostgreSQL, создайте базу данных. Например, используя командную строку или интерфейс администратора PostgreSQL:
```angular2html
createdb <название БД>
```

3. В корневой директории создайте файд config.ini.
Файл config.ini содержит параметры подключения к базе данных. А также путь до файлов миграций. Пример содержимого файла:
```
[database]
DB_NAME = resource_manager_api
DB_USER = postgres
DB_PASS = postgres
DB_HOST = localhost
DB_PORT = 5432

[migrations]
MIGRATION_PATH = /Users/user/Dev/resource_manager/app/migrations
```
4. Затем установите зависимости Python, указанные в файле requirements.txt

```angular2html
pip install -r requirements.txt
```
5. Запустите скрипт для применения миграций:

```angular2html
python migrations.py
```
6. Теперь вы можете запустить ваше приложение:

```angular2html
python main.py
```
Приложение должно быть доступно по адресу http://localhost:8000/

### После запуска приложения, вы можете использовать следующие эндпоинты API:

- GET /resource/{id}: Получить информацию о ресурсе по ID.
- POST /resource: Создать новый ресурс. Принимает json следущего формата:
```angular2html
{
    "type_id": 1,
    "name": 104,
    "current_speed": 35
}
```
- PUT /resource/{id}: Обновить информацию о ресурсе по ID.Принимает json следущего формата:
```angular2html
{
    "type_id": 1,
    "name": 105,
    "current_speed": 37
}
```
- DELETE /resource/{id}: Удалить ресурс по ID.
- GET /type/{id}: Получить информацию о типе ресурса по ID.
- POST /type: Создать новый тип ресурса. Принимает json следущего формата:
```angular2html
{
    "name": "Авто",
    "max_speed": 200
}
```
- PUT /type/{id}: Обновить информацию о типе ресурса по ID.Принимает json следущего формата:
```angular2html
{
    "name": "Мото",
    "max_speed": 377
}
```
- DELETE /type/{id}: Удалить тип ресурса по ID.
- GET /resource/filter_by_type/{type_id}: Получить список ресурсов, отфильтрованных по типу.



### SQL-скрипты с фикстурами
Вы можете создать SQL-скрипты с фикстурами для вашей базы данных. Примеры SQL-скриптов для таблиц resource_type и resource представлены в разделе проекте. Можно использовать и их для наполнения БД.


## Запуск в Docker
### Для запуска приложения и базы данных в контейнерах Docker:
1. Убедитесь, что Docker установлен на вашем компьютере.

2. Создайте файл `config.ini` с параметрами подключения к базе данных (см. раздел "config.ini" выше).

3. Создайте SQL-скрипты с фикстурами для вашей базы данных (см. раздел "SQL-скрипты с фикстурами" выше).

4. Выполните следующие команды в командной строке:

```bash
docker-compose up --build
```
Ваше приложение будет доступно по адресу http://localhost:8000