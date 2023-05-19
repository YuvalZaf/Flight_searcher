from data_manager import DataManager
from flight_search import FlightSearch


ORIGIN = "TLV"


data_manager = DataManager()  # create new list that will contain all our data.
sheet_data = data_manager.get_data()
flight_search = FlightSearch()
flight_search.get_country(destinations=sheet_data, manager=data_manager)
flight_search.search_for_flights(origin=ORIGIN, flight_list=sheet_data, manager=data_manager)

