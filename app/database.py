import os
import configparser
import psycopg2


def create_connection():
    current_directory = os.getcwd()
    config_file_path = os.path.join(current_directory, '../config.ini')
    config = configparser.ConfigParser()
    config.read(config_file_path)

    connection = psycopg2.connect(
        database='postgres',
        user='postgres',
        password='postgres',
        host='db',
        port='5432'
    )

    return connection
