import os
import configparser
import psycopg2


def create_connection():
    current_directory = os.getcwd()
    config_file_path = os.path.join(current_directory, '../config.ini')
    config = configparser.ConfigParser()
    config.read(config_file_path)

    connection = psycopg2.connect(
        database=config['database']['DB_NAME'],
        user=config['database']['DB_USER'],
        password=config['database']['DB_PASS'],
        host=config['database']['DB_HOST'],
        port=config['database']['DB_PORT']
    )

    return connection
