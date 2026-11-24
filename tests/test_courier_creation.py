import requests
import helpers
import allure


class TestCourierCreation:

    @allure.title("Регистрация курьера со всеми обязательными полями")
    def test_courier_creation_with_all_mandatory_fields(cancel_courier):
        with allure.step("Генерация данных курьера"):
            login, password, first_name = helpers.generate_courier_data()

        with allure.step("Регистрация курьера"):    
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            response = requests.post(helpers.URL_COURIER, data=payload)
        
        with allure.step("Авторизация зарегистрированного курьера"):
            response_login = requests.post(f'{helpers.URL_COURIER}/login',data={"login": login, "password": password})
            courier_id = response_login.json()["id"]
        
        with allure.step("Добавление id курьера в список на удаление"):
            cancel_courier.append(courier_id)

        with allure.step("Проверка успешной регистрации"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}

        
    @allure.title("Повторное создание курьера с уже использованными данными")
    def test_create_courueir_with_the_same_data(cancel_courier):
        
        with allure.step("Генерация данных курьера"):
            login, password, first_name = helpers.generate_courier_data()
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            } 

        with allure.step("Первичная регистрация курьера"):    
            response_1 = requests.post(helpers.URL_COURIER, data=payload)
        
        with allure.step("Авторизация курьера для получения его id"):
            response_login = requests.post(
                f'{helpers.URL_COURIER}/login',
                data={"login": login, "password": password}
            )
            courier_id = response_login.json()["id"]

        with allure.step("Повторная регистрация с теми же данными"):
            response_2 = requests.post(helpers.URL_COURIER, data=payload)

        with allure.step("Добавление ID курьера в список на удаление"):
            cancel_courier.append(courier_id)
    
        with allure.step("Проверка ошибки повторной регистрации"):
            assert response_2.status_code == 409
            assert response_2.json()["message"] == 'Этот логин уже используется. Попробуйте другой.'

        
    @allure.title("Создание курьера только с паролем и именем без логина")
    def test_courier_creation_with_login_and_firstName():

        with allure.step("Генерация данных курьера"):
            login, password, first_name = helpers.generate_courier_data()
        
        with allure.step("Отправка запроса на регистрацию без логина"):
            payload = {
                    "password": password,
                    "firstName": first_name
                }
            response = requests.post(helpers.URL_COURIER, data=payload)

        with allure.step("Проверка ошибки из-за отсутствия логина"):    
            assert response.status_code == 400
            assert response.json()["message"] == 'Недостаточно данных для создания учетной записи'

    @allure.title("Создание курьера только с логином и именем без пароля")
    def test__courier_creation_with_password_and_firstName():
        
        with allure.step("Генерация данных курьера"):
            login, password, first_name = helpers.generate_courier_data()
        
        with allure.step("Отправка запроса на регистрацию без пароля"):
            payload = {
                    "login": login,
                    "firstName": first_name
                    }
            response = requests.post(helpers.URL_COURIER, data=payload)
        
        with allure.step("Проверка ошибки из-за отсутствия пароля"):
            assert response.status_code == 400
            assert response.json()["message"] == 'Недостаточно данных для создания учетной записи'