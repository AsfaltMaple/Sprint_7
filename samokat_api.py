import requests
import data
import helpers

class SamokatApi:

    def register_courier(self, body, **kwargs):

        return requests.post(data.URL_COURIER_CREATION, json=body, **kwargs)


    def courier_auth(self, body):
        return requests.post(data.URL_COURIER_LOGIN, json=body)


    def delete_courier(self, courier_id):
        return requests.delete(f'{data.URL_COURIER_CREATION}/{courier_id}')


    def create_order(self, color_for_order):
        firstName, lastName, address, metroStation, phone, rentTime, deliveryDate = helpers.generate_order_data()

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
        return requests.post(data.URL_ORDERS, json=payload)

    def get_orders(self):
        return requests.get(data.URL_ORDERS)


    def cancel_order(self, track):
        return requests.put(data.URL_ORDER_CANCEL, params={"track": track})

    