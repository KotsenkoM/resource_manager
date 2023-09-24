import psycopg2
import json
from wsgiref.simple_server import make_server
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# import re
# pattern = r'\s*([А-Яа-яЁё]+)(\d+)\s*'
# string = r'---   Опять45   ---'
# match = re.search(pattern, string)

class MyApp:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=config['database']['DATABASE_NAME'],
            user=config['database']['DATABASE_USER'],
            password=config['database']['DATABASE_PASSWORD'],
            host=config['database']['DATABASE_HOST'],
            port=config['database']['DATABASE_PORT']
        )

    def __del__(self):
        self.conn.close()

    def get_type(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM resource_type')
        json_data = []

        columns = [desc[0] for desc in cursor.description]

        for row in cursor.fetchall():
            row_data = dict(zip(columns, row))
            json_data.append(row_data)
        cursor.close()

        return json_data


# dict = {
#     type: 'resourse_type',
#     resource: 'resource'
# }
    def create_type(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO {} (id, name, max_speed) VALUES (%s, %s, %s)',
            (data['id'], data['name'], data['max_speed'])
        )
        print(cursor.execute(
            'INSERT INTO {} (id, name, max_speed) VALUES (%s, %s, %s)',
            (data['id'], data['name'], data['max_speed'])
        ))
        self.conn.commit()

        return self.conn.close()

    def update_type(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE resource_type SET name = %s, max_speed = %s WHERE id = %s',
            (data['name'], data['max_speed'], data['id'])
        )
        self.conn.commit()
        cursor.close()

    def delete_type(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            'DELETE FROM resource_type WHERE id = %s',
            (data['id'],)
        )
        self.conn.commit()
        cursor.close()

# urls = [
#     r'/type/<id>','GET', route - типизиваронная вьюха. Кидает 400, если тип не сошелся
# ]

def application(environ, start_response):


    # for path,method, route in:
    # environ['PATH_INFO'] == path and method == environ['REQUEST_METHOD']
    # match = re.search(path,environ['PATH_INFO'])
    # route(match) получить кварги
    app = MyApp()
    response_body = {}
    status = '200 OK'

    request_method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    if request_method == 'GET':
        if path == '/get_type':
            data = app.get_type()
            response_body = json.dumps(data)
            # status = '200 OK'

    elif request_method == 'POST':
        if path == '/create_type':
            request_body = environ['wsgi.input'].read()
            data = json.loads(request_body.decode('utf-8'))
            app.create_type(data)
            response_body = json.dumps({'message': 'New type created successfully'})
            status = '201 Created'

    elif request_method == 'PUT':
        if path == '/update_data':
            request_body = environ['wsgi.input'].read()
            data = json.loads(request_body.decode('utf-8'))
            app.update_type(data)
            response_body = json.dumps({'message': 'Type updated successfully'})

    elif request_method == 'DELETE':
        if path == '/delete_type':
            request_body = environ['wsgi.input'].read()
            data = json.loads(request_body.decode('utf-8'))
            app.delete_type(data)
            response_body = json.dumps({'message': 'Type deleted successfully'})

    else:
        response_body = json.dumps({'error': 'Invalid request method'})
        status = '400 Bad Request'

    response_headers = [('Content-type', 'application/json')]
    start_response(status, response_headers)
    return response_body


if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()


class MyDB:
    def __init__(self,name):
        self.name = name
        self.conn = psycopg2.connect(
            database=config['database']['DATABASE_NAME'],
            user=config['database']['DATABASE_USER'],
            password=config['database']['DATABASE_PASSWORD'],
            host=config['database']['DATABASE_HOST'],
            port=config['database']['DATABASE_PORT']
        )

    def __del__(self):
        self.conn.close()

    def get_type(self,**filters):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM resource_type')
        json_data = []

        columns = [desc[0] for desc in cursor.description]

        for row in cursor.fetchall():
            row_data = dict(zip(columns, row))
            json_data.append(row_data)
        cursor.close()

        return json_data


    def create(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            f'INSERT INTO {self.name} ({data.keys().join(",")}) VALUES ({data.values().join(",")})',
            (data.keys().join(','),data.values().join(','))
        )
        self.conn.commit()

        return self.conn.close()

    def update_type(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE resource_type SET name = %s, max_speed = %s WHERE id = %s',
            (data['name'], data['max_speed'], data['id'])
        )
        self.conn.commit()
        cursor.close()

    def update_many(self, data):
            cursor = self.conn.cursor()
            cursor.execute(
                'UPDATE resource_type SET name = %s, max_speed = %s WHERE id = %s',
                (data['name'], data['max_speed'], data['id'])
            )
            self.conn.commit()
            cursor.close()

    def delete_type(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            'DELETE FROM resource_type WHERE id = %s',
            (data['id'],)
        )
        self.conn.commit()
        cursor.close()



type = MyDB('resource_type')

