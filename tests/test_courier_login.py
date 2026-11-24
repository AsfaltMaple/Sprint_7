#import requests
import helpers
import allure
import data
from samokat_api import SamokatApi

api = SamokatApi()

@allure.parent_suite("Курьеры")
@allure.suite("Авторизация курьера")
class TestCourierLogin:
    @allure.title("Авторизация курьера со всеми обязательными полями")
    def test_exiested_courier_login_with_mandatory_fields(self, cancel_courier):
        
        with allure.step("Генерация данных курьера"):
            login, password, first_name = helpers.generate_courier_data()
    
        with allure.step("Регистрация курьера"):    
                
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            api.register_courier(payload)
                
        with allure.step("Авторизация зарегистрированного курьера"):
                response_login = api.courier_auth(payload)
                courier_id = response_login.json()["id"]
                
        with allure.step("Добавление id курьера в список на удаление"):
                cancel_courier.append(courier_id)


        with allure.step("Проверка кода ответа успешной реги и наличия id в нем"):
            assert response_login.status_code == 200
            assert "id" in response_login.json()

        
    @allure.title("Авторизация с несуществующим логином")
    def test_login_doesnt_exist(self):
        with allure.step("Генерация данных курьера (без регистрации)"):
            login, password, first_name = helpers.generate_courier_data()

        with allure.step("Авторизация курьера"):
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            response = api.courier_auth(payload)

        with allure.step("Проверка кода ответа и сообщения"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"


    @allure.title("Авторизация без логина")
    def test_login_without_login(self, cancel_courier):

        with allure.step("Генерация данных курьера"):
            login, password, first_name = helpers.generate_courier_data()
            
        with allure.step("Регистрация курьера"):    
                        
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            api.register_courier(payload)

        with allure.step("Успешная авторизация для получения id"):
            response_id = api.courier_auth({"login": login, "password": password})
            courier_id = response_id.json()["id"]
        
        with allure.step("Авторизация курьера без логина"):
            payload = {
                "password": password,
                "firstName": first_name
            }
            response = api.courier_auth(payload)
            
        
        with allure.step("Добавление ID курьера в список для удаления"):
            cancel_courier.append(courier_id)
        
        with allure.step("Проверка кода ответа и сообщения"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

        
    @allure.title("Авторизация без пароля")
    def test_login_without_password(self, cancel_courier):

        with allure.step("Генерация данных курьера"):
            login, password, first_name = helpers.generate_courier_data()
                    
        with allure.step("Регистрация курьера"):    
                                
            payload = {
                    "login": login,
                    "password": password,
                    "firstName": first_name
                }
            api.register_courier(payload)


        with allure.step("Успешная авторизация для получения id"):
            response_id = api.courier_auth(payload)
            courier_id = response_id.json()["id"]
            
        with allure.step("Авторизация курьера без пароля"):
            payload = {
                "login": login
            }
            
            response_login = api.courier_auth(payload)
        
        with allure.step("Добавление ID курьера в список для удаления"):
            cancel_courier.append(courier_id)
        
        with allure.step("Проверка кода ответа и сообщения"):
            assert response_login.status_code == 400
            assert response_login.json()["message"] == data.NOT_ALL_DATA_FOR_AUTH_TEXT
            #update: и вот на 3-4 день мучений тест прошел (не менялся, просто пришла ошибка 400)

    @allure.title("Авторизация с неправильным логином")
    def test_login_with_wrong_login(self, cancel_courier): # тест пункта в задании на логин курьера "система вернёт ошибку, если неправильно указать логин или пароль;" 
        #Неясно, что значит "неправильно" - чужой или несуществующий. По документации только несуществующий есть, но формулировака нечеткая
        with allure.step("Генерация данных для 2 курьеров"):
            login1, password1, first_name1 = helpers.generate_courier_data()
            login2, password2, first_name2 = helpers.generate_courier_data()

        with allure.step("Регистрация 2 курьеров с разными данными"):
            payload1 = {
                "login" : login1,
                "password" : password1,
                "first_name" : first_name1
            }

            payload2 = {
                "login" : login2,
                "password" : password2,
                "first_name" : first_name2
           }

            api.register_courier(payload1)
            api.register_courier(payload2)

        with allure.step("Авторизация курьеров для получения их id"):
            response_id_1 = api.courier_auth(payload1)
            response_id_2 = api.courier_auth(payload2)
        
            courier_1_id = response_id_1.json()["id"]
            courier_2_id = response_id_2.json()["id"]
            
        with allure.step("Курьер 2 авторизуется с логином первого курьера"):    
            payload_wrong_pass = {
                "login": login1,
                "password": password2,
                "firstName": first_name2
            }
           
            response = api.courier_auth(payload_wrong_pass)
        
        with allure.step("Добавление ID курьера в список для удаления"):
            cancel_courier.append(courier_1_id)
            cancel_courier.append(courier_2_id)
        
        with allure.step("Проверка кода ответа и сообщения"):
            assert response.status_code == 404
            assert response.json()["message"] == data.NOT_FOUND_TEXT

    