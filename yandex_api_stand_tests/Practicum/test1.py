import sender_stand_request
import data

 # эта функция меняет значения в параметре firstName в теле запроса
def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Имя пользователя введено некорректно. Имя может содержать только русские или " \
                                "латинские буквы, длина должна быть не менее 2 и не более 15 символов"

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")