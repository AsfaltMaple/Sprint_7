import requests
import random
import string
import pytest



# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post('https://qa-scooter.education-services.ru/api/v1/courier', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass

def generate_courier_data(): #без пост-запроса, просто вырезан кусочек с генерацией юзера с 3 полями
    
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    return login, password, first_name

def delete_courier(courier_id):
    response = requests.delete(f'{URL_COURIER}/{courier_id}')
    return response


def generate_order_data():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    firstName = generate_random_string(7)
    lastName = generate_random_string(7)
    address = generate_random_string(10) + " 123"
    metroStation = 5
    phone = "12345678901"
    rentTime = 3
    deliveryDate = "2027-12-12"

    return firstName, lastName, address, metroStation, phone, rentTime, deliveryDate

def create_order(color_for_order):
    firstName, lastName, address, metroStation, phone, rentTime, deliveryDate = generate_order_data()

    payload = {
        "firstName": firstName,
        "lastName": lastName,
        "address": address,
        "metroStation": metroStation,
        "phone": phone,
        "rentTime": rentTime,
        "deliveryDate": deliveryDate,
        "color": color_for_order
    }

    response = requests.post(URL_ORDER, json=payload)

    return response

def cancel_order(track):
    response = requests.put(f'{URL_ORDER}', params={"track": track})
    return response


URL_COURIER = 'https://qa-scooter.education-services.ru/api/v1/courier'
URL_ORDER = 'https://qa-scooter.education-services.ru/api/v1/orders'