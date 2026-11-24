import pytest
import requests
import helpers



class TestOrder:

    @pytest.mark.parametrize('color_for_order', [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_order_created(color_for_order, cancel_order):
        response = helpers.create_order(color_for_order)
        track = response.json()["track"]

        cancel_order.append(track)

        assert response.status_code == 201
        assert "track" in response.json()



    @pytest.mark.parametrize('color_for_order', [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_return_order_list(color_for_order,cancel_order):
        response_create = helpers.create_order(color_for_order)
        track = response_create.json()["track"]

        response_list = requests.get(helpers.URL_ORDER)

        cancel_order.append(track)
        
        assert response_list.status_code == 200
        assert "orders" in response_list.json()