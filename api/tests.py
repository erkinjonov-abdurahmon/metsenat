from django.test import TestCase
import requests


data = {
    "full_name": "Johon",
    "phone_number": "+998922222222",
    "amount": 10000,
    "type": "legal"
}

response = requests.post(
    url = "http://127.0.0.1:8000/api/v1/sponser-create/",
    data=data
)


print(response.status_code)