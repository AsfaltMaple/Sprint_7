import requests
import helpers

def test_exiested_courier_login_with_mandatory_fields():
    
    login_pass = helpers.register_new_courier_and_return_login_password()
    payload = {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }
    response_login = requests.post(f'{helpers.URL_COURIER}/login', data=payload)

    assert response_login.status_code == 200
    assert "id" in response_login.json()

def test_login_doesnt_exist():
    login, password, first_name = helpers.generate_courier_data()
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f'{helpers.URL_COURIER}/login', data=payload)
    assert response.status_code == 404
    assert response.json()["message"] == "Учетная запись не найдена"

def test_login_without_login():
    login_pass = helpers.register_new_courier_and_return_login_password()
    payload = {
        "password": login_pass[1],
        "firstName": login_pass[2]
    }
    response_login = requests.post(f'{helpers.URL_COURIER}/login', data=payload)
    assert response_login.status_code == 400
    assert response_login.json()["message"] == "Недостаточно данных для входа"

def test_login_without_password():
    login_pass = helpers.register_new_courier_and_return_login_password()
    payload = {
        "login": login_pass[0]
    }
    response_login = requests.post(f'{helpers.URL_COURIER}/login', json=payload)
    
    assert response_login.status_code == 400
    assert response_login.json()["message"] == "Недостаточно данных для входа" #хоть в описании и ожидается ошибка 400, но и тест тут, и постман выдают 504!

def test_login_with_wrong_login(): # тест пункта в задании на логин курьера "система вернёт ошибку, если неправильно указать логин или пароль;"
    login_pass1 = helpers.register_new_courier_and_return_login_password() #создаем 2 пользователей
    login_pass2 = helpers.register_new_courier_and_return_login_password()
    payload1 = {
        "login": login_pass1[0],
        "password": login_pass1[1],
        "firstName": login_pass1[2]
    }
    payload2 = {
            "login": login_pass1[0], # для логина второго берем "чужой" логин
            "password": login_pass2[1],
            "firstName": login_pass2[2]
    }
    response = requests.post(f'{helpers.URL_COURIER}/login', data=payload2)
    assert response.status_code == 404
    assert response.json()["message"] == "Учетная запись не найдена"