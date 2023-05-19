import requests
import os

SHEETY_API = os.environ.get("sheety_api")


class DataManager:

    def __init__(self):  # constructor
        self.destinations = {}

    def get_data(self):
        response = requests.get(url=SHEETY_API)
        data = response.json()
        self.destinations = data["flights"]
        return self.destinations

    def update_data(self):
        for i in self.destinations:
            id = i["id"]
            new = {  # what is the update?
                "flight": {
                    "iataCode": i["iataCode"]
                }
            }
            update_key = os.environ.get("sheety_update")
            UPDATE = f"{update_key}{id}"
            response = requests.put(url=UPDATE, json=new)

    def update_flights(self):
        for i in self.destinations:
            id=i["id"]
            new_data= {
                "flight": {
                    "price": i["price"],
                    "landing":  i["landing"],
                    "date": i["date"],
                    "flightNum": i["flightNum"],
                    "link": i["link"]
                }
            }
            update_key = os.environ.get("sheety_update")
            UPDATE = f"{update_key}{id}"
            response = requests.put(url=UPDATE, json=new_data)





