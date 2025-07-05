# utils/skyscanner_api.py

import requests

API_KEY = "dabba5c077msh833b43885712b0ap1e4852jsna987a0b257bd"
API_HOST = "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

def get_flight_quotes(origin, destination, date):
    """
    Fetch flight quotes using Skyscanner API.
    """
    url = f"https://{API_HOST}/apiservices/browsequotes/v1.0/US/USD/en-US/{origin}/{destination}/{date}"

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
