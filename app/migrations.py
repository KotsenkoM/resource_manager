import os
import configparser
from database import create_connection

current_directory = os.getcwd()
config_file_path = os.path.join(current_directory, '../config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)


def apply_migrations():
    connection = create_connection()
    cursor = connection.cursor()
    migration_dir = config['migrations']['MIGRATION_PATH']
    migration_files = sorted(f for f in os.listdir(migration_dir) if f.endswith('.sql'))

    for migration_file in migration_files:
        migration_name = os.path.splitext(migration_file)[0]
        with open(os.path.join(migration_dir, migration_file), 'r') as f:
            migration_sql = f.read()
            cursor.execute(migration_sql)
        connection.commit()
        print(f'Applied migration: {migration_name}')

    cursor.close()
    connection.close()


if __name__ == '__main__':
    apply_migrations()
