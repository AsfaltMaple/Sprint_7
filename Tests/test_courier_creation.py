import requests
import helpers

def test_courier_creation_with_all_mandatory_fields():
    login, password, first_name = helpers.generate_courier_data()
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(helpers.URL_COURIER, data=payload)

    assert response.status_code == 201
    assert response.json() == {"ok": True}

def test_create_courueir_with_the_same_data():
    login, password, first_name = helpers.generate_courier_data()
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
       } 
    response_1 = requests.post(helpers.URL_COURIER, data=payload)
    response_2 = requests.post(helpers.URL_COURIER, data=payload)

    assert response_2.status_code == 409
    assert response_2.json()["message"] == 'Этот логин уже используется. Попробуйте другой.'

def test_courier_creation_with_login_and_firstName():
    login, password, first_name = helpers.generate_courier_data()
    payload = {
            "password": password,
            "firstName": first_name
           }
    response = requests.post(helpers.URL_COURIER, data=payload)
    assert response.status_code == 400
    assert response.json()["message"] == 'Недостаточно данных для создания учетной записи'

def test__courier_creation_with_password_and_firstName():
    login, password, first_name = helpers.generate_courier_data()
    payload = {
            "login": login,
            "firstName": first_name
            }
    response = requests.post(helpers.URL_COURIER, data=payload)
    assert response.status_code == 400
    assert response.json()["message"] == 'Недостаточно данных для создания учетной записи'