
import random
import string



def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

def generate_courier_data(): #без пост-запроса, просто вырезан кусочек с генерацией юзера с 3 полями

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return login, password, first_name

def generate_order_data():
    
    firstName = generate_random_string(7)
    lastName = generate_random_string(7)
    address = generate_random_string(10) + " 123"
    metroStation = 5
    phone = "12345678901"
    rentTime = 3
    deliveryDate = "2027-12-12"
    return firstName, lastName, address, metroStation, phone, rentTime, deliveryDate
