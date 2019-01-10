import requests
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser


config = ConfigParser()
config.read('file_config.conf')


def get_conf_param(selection, parametr, default_value):
    result = config.get(selection, parametr)
    return result or default_value


user = get_conf_param('DEFAULT', 'user', '')
password = get_conf_param('DEFAULT', 'password', '')
host = get_conf_param('DEFAULT', 'host', 'http://127.0.0.1:7000')


def get(url, cookies=None, auth_data=None, params=None):
    result = requests.get(url, cookies=cookies, auth=auth_data, params=params)

    print('GET request to {0}'.format(url))
    print('Status code: {0}'.format(result.status_code))
    print('RESPONSE: {0}'.format(result.text))

    return result


def post(url, cookies=None, body=None):
    result = requests.post(url, cookies=cookies, data=body)

    print('POST request to {0}'.format(url))
    print('Status code: {0}'.format(result.status_code))
    print('RESPONSE: {0}'.format(result.text))

    return result


def put(url, cookies=None, body=None):
    result = requests.put(url, cookies=cookies, data=body)

    print('PUT request to {0}'.format(url))
    print('Status code: {0}'.format(result.status_code))
    print('RESPONSE: {0}'.format(result.text))

    return result


def delete(url, cookies=None):
    result = requests.delete(url, cookies=cookies)

    print('DELETE request to {0}'.format(url))
    print('Status code: {0}'.format(result.status_code))
    print('RESPONSE: {0}'.format(result.text))

    return result


def auth():
    url = '{0}/login'.format(host)

    auth_data = HTTPBasicAuth(user, password)

    response = get(url, auth_data=auth_data)
    data = response.json()

    return {'my_cookie': data['auth_cookie']}


def get_list_books(params=None):
    """ Получаем и возвращаем список книг"""

    result = get('{0}/books'.format(host), cookies=auth(), params=params)

    return result.json()


def get_book(book_id):

    result = get('{0}/books/{1}'.format(host, book_id), cookies=auth())

    return result.json()


def add_book(book):
    """ Добавляем и возращаем книгу"""

    result = post('{0}/add_book'.format(host), cookies=auth(), body=book)

    return result.json()


def update_book(book_id, book):

    result = put('{0}/books/{1}'.format(host, book_id), cookies=auth(), body=book)

    return result.json()


def delete_book(book_id):

    delete('{0}/books/{1}'.format(host, book_id), cookies=auth())



