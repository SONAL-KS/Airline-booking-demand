# utils/aviationstack_api.py

import requests

API_KEY = "9d6a8de5693054f19bd0be129d67633e"
BASE_URL = "http://api.aviationstack.com/v1"

def fetch_flights(origin_iata):
    """
    Fetch flights using only dep_iata (origin) — Free Plan compatible.
    """
    params = {
        "access_key": API_KEY,
        "dep_iata": origin_iata
    }

    try:
        response = requests.get(f"{BASE_URL}/flights", params=params)
        response.raise_for_status()
        json_data = response.json()
        print(f"✅ API request successful. Flights received: {len(json_data.get('data', []))}")
        return json_data

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err} - {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request failed: {req_err}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return None
