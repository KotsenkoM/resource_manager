import os
import configparser
import psycopg2


def create_connection():
    current_directory = os.getcwd()
    config_file_path = os.path.join(current_directory, '../config.ini')
    config = configparser.ConfigParser()
    config.read(config_file_path)

    connection = psycopg2.connect(
        database=config['database']['DbName'],
        user=config['database']['DbUser'],
        password=config['database']['DbPass'],
        host=config['database']['DbHost'],
        port=config['database']['DbPort']
    )

    return connection
