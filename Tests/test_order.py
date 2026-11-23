import pytest
import requests
import helpers



@pytest.mark.parametrize('color_for_order', [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
def test_order_created(color_for_order, cancel_order):
    response = helpers.create_order(color_for_order)
    track = response.json()["track"]
    assert response.status_code == 201
    assert "track" in response.json()

    cancel_order.append(track)


@pytest.mark.parametrize('color_for_order', [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
def test_return_order_list(color_for_order,cancel_order):
    response_create = helpers.create_order(color_for_order)
    track = response_create.json()["track"]

    response_list = requests.get(helpers.URL_ORDER)
    
    assert response_list.status_code == 200
    assert "orders" in response_list.json()

    cancel_order.append(track)
   