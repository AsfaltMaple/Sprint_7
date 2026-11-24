import requests
import helpers
import allure


class TestCourierLogin:
    @allure.title("Авторизация курьера со всеми обязательными полями")
    def test_exiested_courier_login_with_mandatory_fields(cancel_courier):
        with allure.step("Регистрация курьера"):
            login_pass = helpers.register_new_courier_and_return_login_password()
            
        with allure.step("Авторизация курьера"):
            payload = {
                "login": login_pass[0],
                "password": login_pass[1],
                "firstName": login_pass[2]
            }
            response_login = requests.post(f'{helpers.URL_COURIER}/login', data=payload)
            courier_id = response_login.json()["id"]

        with allure.step("Добавление ID курьера в список для удаления"):
            cancel_courier.append(courier_id)

        with allure.step("Проверка кода ответ и наличия id в нем"):
            assert response_login.status_code == 200
            assert "id" in response_login.json()

        
    @allure.title("Авторизация с несуществующим логином")
    def test_login_doesnt_exist():
        with allure.step("Генерация данных курьера (без регистрации)"):
            login, password, first_name = helpers.generate_courier_data()

        with allure.step("Авторизация курьера"):
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            response = requests.post(f'{helpers.URL_COURIER}/login', data=payload)

        with allure.step("Проверка кода ответа и сообщения"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"


    @allure.title("Авторизация без логина")
    def test_login_without_login(cancel_courier):

        with allure.step("Регистрация курьера"):
            login_pass = helpers.register_new_courier_and_return_login_password()
        
        with allure.step("Авторизация курьера"):
            payload = {
                "password": login_pass[1],
                "firstName": login_pass[2]
            }
            response_id = requests.post(f'{helpers.URL_COURIER}/login', data={"login": login_pass[0], "password": login_pass[1]})
            courier_id = response_id.json()["id"]

            response_login = requests.post(f'{helpers.URL_COURIER}/login', data=payload)
        
        with allure.step("Добавление ID курьера в список для удаления"):
            cancel_courier.append(courier_id)
        
        with allure.step("Проверка кода ответа и сообщения"):
            assert response_login.status_code == 400
            assert response_login.json()["message"] == "Недостаточно данных для входа"

        
    @allure.title("Авторизация без пароля")
    def test_login_without_password(cancel_courier):

        with allure.step("Регистрация курьера"):
            login_pass = helpers.register_new_courier_and_return_login_password()
        
        with allure.step("Авторизация курьера"):
            payload = {
                "login": login_pass[0]
            }
            response_id = requests.post(f'{helpers.URL_COURIER}/login', data={"login": login_pass[0], "password": login_pass[1]})
            courier_id = response_id.json()["id"]
            
            response_login = requests.post(f'{helpers.URL_COURIER}/login', data=payload)
        
        with allure.step("Добавление ID курьера в список для удаления"):
            cancel_courier.append(courier_id)
        
        with allure.step("Проверка кода ответа и сообщения"):
            assert response_login.status_code == 400
            assert response_login.json()["message"] == "Недостаточно данных для входа" #хоть в описании и ожидается ошибка 400, но и тест тут, и постман выдают 504!
            #update: и вот на 3-4 день мучений тест прошел (не менялся, просто пришла ошибка 400)

    @allure.title("Авторизация с неправильным логином")
    def test_login_with_wrong_login(cancel_courier): # тест пункта в задании на логин курьера "система вернёт ошибку, если неправильно указать логин или пароль;" 
        #Неясно, что значит "неправильно" - чужой или несуществующий. По документации только несуществующий есть, но формулировака нечеткая
        
        with allure.step("Регистрация 2 курьеров с разными данными"):
            login_pass1 = helpers.register_new_courier_and_return_login_password() #создаем 2 пользователей
            login_pass2 = helpers.register_new_courier_and_return_login_password()

        with allure.step("Авторизация курьеров для получения их id"):
            response_id_1 = requests.post(f'{helpers.URL_COURIER}/login', data={"login": login_pass1[0], "password": login_pass1[1]})
            response_id_2 = requests.post(f'{helpers.URL_COURIER}/login', data={"login": login_pass2[0], "password": login_pass2[1]})
        
            courier_1_id = response_id_1.json()["id"]
            courier_2_id = response_id_2.json()["id"]
            
        with allure.step("Курьер 2 авторизуется с логином первого курьера"):    
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
        
        with allure.step("Добавление ID курьера в список для удаления"):
            cancel_courier.append(courier_1_id)
            cancel_courier.append(courier_2_id)
        
        with allure.step("Проверка кода ответа и сообщения"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"

        