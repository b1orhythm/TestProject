import pytest
import requests
from requests.auth import HTTPBasicAuth
import random

# CFG
host = 'http://127.0.0.1:7000'
user = 'test_user'
password = 'test_password'


@pytest.fixture
def auth_cookie():
    result = requests.get(host + "/login", auth=HTTPBasicAuth(user, password))
    data = result.json()
    yield data['auth_cookie']


def list_books(auth_cookie):
    """ Получаем и возвращаем список книг"""

    result = requests.get(host + "/books", cookies={'my_cookie': auth_cookie})
    list_books = result.json()
    return list_books


def add_book(a, b):
    """ Добавляем и возращаем книгу"""

    result = requests.post(host + "/add_book", cookies={'my_cookie': a}, data=b)
    data = result.json()
    return data


def test_check_login():
    url = host + "/login"

    # Авторизация с валидными данными
    result = requests.get(url, auth=HTTPBasicAuth(user, password))
    assert result.status_code == 200

    # Попытка авторизации без данных
    result = requests.get(url, auth=HTTPBasicAuth('', ''))
    assert result.status_code == 401

    # Попытка авторизации без пароля
    result = requests.get(url, auth=HTTPBasicAuth(user, ''))
    assert result.status_code == 401

    # Попытка авторизации с некорректным паролем
    result = requests.get(url, auth=HTTPBasicAuth(user, 'test_Password'))
    assert result.status_code == 401

    # Попытка авторизации с некорректным логином
    result = requests.get(url, auth=HTTPBasicAuth('Test_User', password))
    assert result.status_code == 401


def test_check_list_books(auth_cookie):
    result = requests.get(host + '/books', cookies={'my_cookie': auth_cookie})
    data = result.json()

    assert result.status_code == 200
    assert len(data) >= 0


def test_add_book(auth_cookie):
    # Запрашиваем текущий список книг
    amount = len(list_books(auth_cookie))

    new_book = {'title': 'First book', 'author': 'unknown'}

    # Добавляем книгу
    new_book['id'] = add_book(auth_cookie, new_book)['id']

    assert new_book['id'] != ''

    # Повторно запрашиваем список книг
    list_b = list_books(auth_cookie)

    assert len(list_b) > amount
    assert new_book in list_b


def test_delete_book(auth_cookie):
    new_book = {'title': 'Book for delete', 'author': 'unknown'}

    # Добавляем книгу
    new_book['id'] = add_book(auth_cookie, new_book)['id']

    # Получаем текущее кол-во книг
    amount = len(list_books(auth_cookie))

    # Удаляем книгу
    requests.delete(host + "/books/" + new_book['id'], cookies={'my_cookie': auth_cookie})

    # Повторно получаем список книг
    list_b = list_books(auth_cookie)

    assert amount > len(list_b)
    assert new_book['id'] not in list_b


def test_open_book(auth_cookie):
    # Получаем список книг
    list_b = list_books(auth_cookie)

    # Проверяем, что список книг не пустой
    if len(list_b) != 0:
        # Выбираем случайный id книги из списка
        r_book_id = list_b[random.randint(0, len(list_b)-1)]['id']

        # Получаем данные выбранной книги
        result = requests.get(host+"/books/"+r_book_id, cookies={'my_cookie': auth_cookie})
        data = result.json()

        assert result.status_code == 200
        assert 'title' in data, "ERROR: Book title not found!"
        assert 'author' in data, "ERROR: Book author not found!"
    else:
        new_book = {'title': 'Good book', 'author': 'Human'}

        # Создаем новую книгу
        new_book['id'] = (auth_cookie, new_book)['id']

        # Получаем данные созданной книги
        result = requests.get(host+"/books/"+new_book['id'], cookies={'my_cookie': auth_cookie})
        data = result.json()

        assert result.status_code == 200
        assert 'title' in data, "ERROR: Book title not found!"
        assert 'author' in data, "ERROR: Book author not found!"

def test_update_book(auth_cookie):
    new_book = {'title': 'Book for update', 'author': 'Human'}

    new_title = 'Book for update II'
    new_author = 'Russian Human'

    # Добавляем книгу
    new_book['id'] = add_book(auth_cookie, new_book)['id']

    # Обновляем данные в ранее добавленной книге
    requests.put(host+"/books/"+new_book['id'], cookies={'my_cookie': auth_cookie}, data={'title': new_title, 'author': new_author})

    # Повторно получаем данные текущей книги
    result = requests.get(host+"/books/"+new_book['id'], cookies={'my_cookie': auth_cookie})
    data = result.json()

    assert result.status_code == 200
    assert data['title'] == new_title, "ERROR: Book title not updated!"
    assert data['author'] == new_author, "ERROR: Book author not updated!"