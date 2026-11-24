import pytest
import allure
from samokat_api import SamokatApi

api = SamokatApi()

@allure.parent_suite("Заказы")
@allure.suite("Создание заказа и получение списка заказов")
class TestOrder:
    @allure.title("Успешное создание заказа")
    @pytest.mark.parametrize('color_for_order', [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_order_created(self, color_for_order, cancel_order):
        response = api.create_order(color_for_order)
        track = response.json()["track"]

        cancel_order.append(track)

        assert response.status_code == 201
        assert "track" in response.json()


    @allure.title("Получение списка заказов")
    @pytest.mark.parametrize('color_for_order', [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_return_order_list(self, color_for_order,cancel_order):
        response_create = api.create_order(color_for_order)
        track = response_create.json()["track"]

        response_list = api.get_orders()

        cancel_order.append(track)
        
        assert response_list.status_code == 200
        assert "orders" in response_list.json()