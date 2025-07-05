# utils/aviationstack_api.py

import requests
import random
from datetime import datetime, timedelta

API_KEY = "9d6a8de5693054f19bd0be129d67633e"
BASE_URL = "http://api.aviationstack.com/v1"

def fetch_flights(origin_iata):
    """
    Fetch flights using only dep_iata (origin) — Free Plan compatible.
    Falls back to mock data if API fails.
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
        print("🔄 Falling back to mock data...")
        return generate_mock_flights(origin_iata)
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request failed: {req_err}")
        print("🔄 Falling back to mock data...")
        return generate_mock_flights(origin_iata)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("🔄 Falling back to mock data...")
        return generate_mock_flights(origin_iata)

def generate_mock_flights(origin_iata):
    """
    Generate realistic mock flight data for Australian airports.
    """
    australian_airports = [
        "SYD", "MEL", "BNE", "PER", "ADL", "CBR", "HBA", "DRW", 
        "CNS", "TSV", "NTL", "OOL", "MCY", "MKY", "ROK", "PQQ"
    ]
    
    airlines = [
        {"name": "Qantas", "iata": "QF"},
        {"name": "Virgin Australia", "iata": "VA"},
        {"name": "Jetstar", "iata": "JQ"},
        {"name": "Rex Airlines", "iata": "ZL"},
        {"name": "Regional Express", "iata": "RE"}
    ]
    
    flight_statuses = ["scheduled", "active", "landed", "cancelled"]
    
    # Generate 10-20 mock flights
    num_flights = random.randint(10, 20)
    flights = []
    
    for i in range(num_flights):
        # Random destination (different from origin)
        destination = random.choice([airport for airport in australian_airports if airport != origin_iata])
        
        # Random airline
        airline = random.choice(airlines)
        
        # Random flight date (within next 7 days)
        flight_date = (datetime.now() + timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")
        
        # Random flight number
        flight_number = f"{airline['iata']}{random.randint(100, 9999)}"
        
        flight = {
            "flight_date": flight_date,
            "departure": {
                "iata": origin_iata,
                "airport": f"{origin_iata} Airport"
            },
            "arrival": {
                "iata": destination,
                "airport": f"{destination} Airport"
            },
            "airline": {
                "name": airline["name"],
                "iata": airline["iata"]
            },
            "flight": {
                "number": flight_number,
                "iata": flight_number
            },
            "flight_status": random.choice(flight_statuses)
        }
        
        flights.append(flight)
    
    print(f"✅ Generated {len(flights)} mock flights from {origin_iata}")
    return {"data": flights}
