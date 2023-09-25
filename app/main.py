import json
import psycopg2
import re

from wsgiref.simple_server import make_server
from database import create_connection


class ResourceApp:
    def __init__(self):
        self.conn = create_connection()

    def get_data(self, id=None):
        with self.conn.cursor() as cursor:
            try:
                if id:
                    cursor.execute(
                        'SELECT r.*, t.max_speed FROM resource r '
                        'INNER JOIN resource_type t ON r.type_id = t.id '
                        'WHERE r.id = %s',
                        (id,)
                    )
                else:
                    cursor.execute(
                        'SELECT r.*, t.max_speed FROM resource r '
                        'INNER JOIN resource_type t ON r.type_id = t.id'
                    )
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                json_data = []
                for row in rows:
                    resource = dict(zip(columns, row))
                    resource['exceed_percentage'] = (
                            (resource['current_speed'] - resource['max_speed']) / resource['max_speed'] * 100
                    )
                    json_data.append(resource)
                return json_data
            except (Exception, psycopg2.DatabaseError) as e:
                return {'error': str(e)}

    def get_data_filtered_by_type(self, type_id):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute('SELECT * FROM resource WHERE type_id = %s', (type_id,))
                columns = [desc[0] for desc in cursor.description]
                json_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return json_data
            except (Exception, psycopg2.DatabaseError) as e:
                return {'error': str(e)}

    def create_data(self, data):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(
                    'INSERT INTO resource (type_id, name, current_speed) VALUES (%s, %s, %s)',
                    (data['type_id'], data['name'], data['current_speed'])
                )
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as e:
                return {'error': str(e)}

    def update_data(self, id, data):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(
                    'UPDATE resource SET type_id = %s, name = %s, current_speed = %s WHERE id = %s',
                    (data['type_id'], data['name'], data['current_speed'], id)
                )
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as e:
                return {'error': str(e)}

    def delete_data(self, id):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute('DELETE FROM resource WHERE id = %s', (id,))
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as e:
                return {'error': str(e)}


class TypeApp:
    def __init__(self):
        self.conn = create_connection()

    def get_data(self, id=None):
        with self.conn.cursor() as cursor:
            try:
                if id:
                    cursor.execute('SELECT * FROM resource_type WHERE id = %s', (id,))
                else:
                    cursor.execute('SELECT * FROM resource_type')
                columns = [desc[0] for desc in cursor.description]
                json_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return json_data
            except (Exception, psycopg2.DatabaseError) as e:
                return {'error': str(e)}

    def create_data(self, data):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(
                    'INSERT INTO resource_type (name, max_speed) VALUES (%s, %s)',
                    (data['name'], data['max_speed'])
                )
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as e:
                return {'error': str(e)}

    def update_data(self, id, data):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(
                    'UPDATE resource_type SET name = %s, max_speed = %s WHERE id = %s',
                    (data['name'], data['max_speed'], id)
                )
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as e:
                return {'error': str(e)}

    def delete_data(self, id):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute('DELETE FROM resource_type WHERE id = %s', (id,))
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as e:
                return {'error': str(e)}


resource_app = ResourceApp()
type_app = TypeApp()

routes = [
    ('GET', r'/resource/(\d+)', resource_app, 'get_data'),
    ('POST', r'/resource', resource_app, 'create_data'),
    ('PUT', r'/resource/(\d+)', resource_app, 'update_data'),
    ('DELETE', r'/resource/(\d+)', resource_app, 'delete_data'),
    ('GET', r'/type/(\d+)', type_app, 'get_data'),
    ('POST', r'/type', type_app, 'create_data'),
    ('PUT', r'/type/(\d+)', type_app, 'update_data'),
    ('DELETE', r'/type/(\d+)', type_app, 'delete_data'),
    ('GET', r'/resource/filter_by_type/(\d+)', resource_app, 'get_data_filtered_by_type'),
]


def application(environ, start_response):
    response_body = {}
    status = '200 OK'
    response_headers = [('Content-type', 'application/json')]

    path = environ['PATH_INFO']
    request_method = environ['REQUEST_METHOD']

    for method, pattern, class_instance, func_name in routes:
        if request_method == 'GET' and re.match(r'/resource/filter_by_type/(\d+)', path):
            try:
                match = re.match(r'/resource/filter_by_type/(\d+)', path)
                type_id = int(match.group(1))
                handler = resource_app.get_data_filtered_by_type
                response_body = json.dumps(handler(type_id))
            except ValueError as ve:
                response_body = json.dumps({'error': str(ve)})
                status = '400 Bad Request'
            except Exception as e:
                response_body = json.dumps({'error': str(e)})
                status = '500 Internal Server Error'
        if request_method == method and re.match(pattern, path):
            try:
                match = re.match(pattern, path)
                if match.groups():
                    args = [int(arg) for arg in match.groups()]
                    handler = getattr(class_instance, func_name)
                    response_body = json.dumps(handler(*args))
                else:
                    data = json.loads(environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))))
                    handler = getattr(class_instance, func_name)
                    response_body = json.dumps(handler(data))
            except ValueError as ve:
                response_body = json.dumps({'error': str(ve)})
                status = '400 Bad Request'
            except Exception as e:
                response_body = json.dumps({'error': str(e)})
                status = '500 Internal Server Error'
            break
    else:
        response_body = json.dumps({'error': 'Invalid request method or path'})
        status = '400 Bad Request'

    start_response(status, response_headers)
    return [response_body.encode('utf-8')]


if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()
