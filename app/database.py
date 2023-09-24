import configparser
import psycopg2

config = configparser.ConfigParser()
config.read('config.ini')

CONNECTION = psycopg2.connect(
            database=config['database']['DATABASE_NAME'],
            user=config['database']['DATABASE_USER'],
            password=config['database']['DATABASE_PASSWORD'],
            host=config['database']['DATABASE_HOST'],
            port=config['database']['DATABASE_PORT']
        )

def db_connection(func):
    def wrapper(*args, **kwargs):
        connection = psycopg2.connect(
            database=config['database']['DATABASE_NAME'],
            user=config['database']['DATABASE_USER'],
            password=config['database']['DATABASE_PASSWORD'],
            host=config['database']['DATABASE_HOST'],
            port=config['database']['DATABASE_PORT']
        )
        cursor = connection.cursor()
        result = func(*args, cursor=cursor, connection=connection, **kwargs)
        cursor.close()
        return result
    return wrapper
