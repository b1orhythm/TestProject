import pytest
import requests
from requests.auth import HTTPBasicAuth
import random
from utils import get_list_books
from utils import get_book
from utils import add_book
from utils import update_book
from utils import delete_book

"""

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

"""

@pytest.mark.parametrize('sort', ['', 'by_title'])
@pytest.mark.parametrize('limit', [-1, 0, 2, 5, 10, 50, 100])
def test_check_list_books(sort, limit):

    add_book({'author': '', 'title': ''})
    add_book({'author': 'Author', 'title': 'Z'})
    add_book({'author': 'D-author', 'title': 'M'})
    add_book({'author': 'L-author', 'title': 'B'})

    params = {'sort': sort, 'limit': limit}

    data = get_list_books(params)

    print(data)

    for book in data:
        assert 'title' in book
        assert 'author' in book
        assert 'id' in book

    if (limit != -1 and limit !=0):
        assert len(data) <= limit
    else:
        assert len(data) >= 4

    if sort == 'by_title':
        assert data[0]['title'] == ''


@pytest.mark.parametrize('title', ['', 'Book with title', u'Книга с интересным названием', '$^&%@&(*!_+=', '*(&ADIG!7213'*100])
@pytest.mark.parametrize('author', ['', 'book Author', u'Автор книги', '$^&%@&(*!_+=', '*(&ADIG!7213'*100])
def test_add_book(title, author):
    # Запрашиваем текущее кол-во книг
    amount = len(get_list_books())

    new_book = {'title': title, 'author': author}

    # Добавляем книгу
    new_book['id'] = add_book(new_book)['id']

    # Повторно запрашиваем список книг
    list_b = get_list_books()

    assert len(list_b) > amount
    assert new_book in list_b


def test_open_book():
    # Получаем список книг
    list_b = get_list_books()

    # Проверяем, что список книг не пустой
    if len(list_b) != 0:
        # Выбираем случайный id книги из списка
        r_book_id = list_b[random.randint(0, len(list_b)-1)]['id']

        # Получаем данные выбранной книги
        data = get_book(r_book_id)

        assert 'title' in data, "ERROR: Book title not found!"
        assert 'author' in data, "ERROR: Book author not found!"
    else:
        new_book = {'title': 'Good book', 'author': 'Human'}

        # Создаем новую книгу
        new_book['id'] = add_book(new_book)['id']

        # Получаем данные созданной книги
        data = get_book(new_book['id'])

        assert 'title' in data, "ERROR: Book title not found!"
        assert 'author' in data, "ERROR: Book author not found!"


def test_delete_book():
    new_book = {'title': 'Book for delete', 'author': 'unknown'}

    # Добавляем книгу
    new_book['id'] = add_book(new_book)['id']

    # Получаем текущее кол-во книг
    amount = len(get_list_books())

    # Удаляем книгу
    delete_book(new_book['id'])

    # Повторно получаем список книг
    list_b = get_list_books()

    assert amount > len(list_b)
    assert new_book not in list_b, "ERROR: Книга не была удалена и присутствует в списке!"


@pytest.mark.parametrize('title', ['', 'Book with title', u'Книга с интересным названием', '$^&%@&(*!_+=', '*(&ADIG!7213'*100])
@pytest.mark.parametrize('author', ['', 'book Author', u'Автор книги', '$^&%@&(*!_+=', '*(&ADIG!7213'*100])
def test_update_book(title, author):
    new_book = {'title': 'Book for update', 'author': 'Human'}

    new_data_book = {'title': title, 'author': author}

    # Добавляем книгу
    new_book['id'] = add_book(new_book)['id']

    # Обновляем данные в ранее добавленной книге
    update_book(new_book['id'], new_data_book)

    # Повторно получаем данные текущей книги
    data = get_book(new_book['id'])

    assert data['title'] == title, "ERROR: Book title not updated!"
    assert data['author'] == author, "ERROR: Book author not updated!"
