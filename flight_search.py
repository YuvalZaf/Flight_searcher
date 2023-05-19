import requests
import datetime
from dateutil import parser
import os


URL = "https://tequila-api.kiwi.com/locations/query"
TEQUILA_SEARCH_URL = "https://api.tequila.kiwi.com/v2/search"
API_KEY = os.environ.get("tequila_api_key")


class FlightSearch:
    def __init__(self):
        self.today =datetime.datetime.now().strftime("%d/%m/%Y")  # today date ant time
        self.six_months = (datetime.datetime.now() + datetime.timedelta(days=6 * 30)).strftime(
            "%d/%m/%Y")  # search for flights in six months period

    def get_country(self, destinations, manager): # search for city/airport code in kiwi web.
        headers = {"apikey": API_KEY}
        for i in destinations:
            name = i["iataCode"]
            if name == "":
                query = {"term": i["city"], "location_types": "city"}
                response = requests.get(url=URL, headers=headers, params=query)
                updated = response.json()  # change the data to json format to read it
                final = updated["locations"][0]["code"]  # need to take specific field from the response(only IATA)
                i["iataCode"] = final
        manager.update_data()

    def search_for_flights(self, origin, flight_list, manager):
        headers = {"apikey": API_KEY}
        for i in flight_list:
            parsed_date = parser.parse(i["fromDate"])
            parsed_date2 = parser.parse(i["toDate"])
            query = {
                "fly_from": origin,
                "fly_to": i["iataCode"],
                "date_from": parsed_date.strftime("%d/%m/%Y"),
                "date_to": parsed_date2.strftime("%d/%m/%Y"),
                "nights_in_dst_from": i["lbNights"],
                "nights_in_dst_to": i["ubNights"],
                "one_for_city": 1,
                "flight_type": "round",
                "max_stopovers": 0,
                "curr": "ILS"
            }
            response = requests.get(url=TEQUILA_SEARCH_URL, headers=headers, params=query)
            response.raise_for_status()
            try:
                data = response.json()["data"][0]
                i['landing'] = data["flyTo"]
                i['price'] = data["price"]
                i['date'] = data["local_departure"].split("T")[0]
                i['flightNum'] = data["route"][0]["flight_no"]
                i['link'] = data["deep_link"]
            except IndexError:
                print(f"No flights found for city.")
        manager.update_flights()





