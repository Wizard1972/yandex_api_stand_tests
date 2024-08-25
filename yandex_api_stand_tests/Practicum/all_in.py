import requests

URL_SERVICE = "https://39d99445-a8ce-45ce-9bc0-9e93d1904466.serverhub.praktikum-services.ru/"
DOC_PATH = "/docs/"
LOG_MAIN_PATH = "/api/logs/main"
USERS_TABLE_PATH = "/api/db/resources/user_model.csv"
CREATE_USER_PATH = "/api/v1/users/"
PRODUCTS_KITS_PATH = "/api/v1/products/kits/"

headers = {
    "Content-Type": "application/json"
}

user_body = {
    "firstName": "Aa",
    "phone": "+79684640044",
    "address": "г. Москва, ул. Пушкина, д. 10"
}

def post_new_user(body):
   return requests.post(URL_SERVICE + CREATE_USER_PATH,
                         json=body,
                         headers=headers)

response = post_new_user(user_body)


def get_users_table():
    return requests.get(URL_SERVICE + USERS_TABLE_PATH)

response = get_users_table()


def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body



def positive_assert(first_name):
    # В переменную user_body сохраняется обновленное тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1

def test_create_user_number_type_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(12)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    response = post_new_user(user_body)

    # Проверка кода ответа
    assert response.status_code == 400