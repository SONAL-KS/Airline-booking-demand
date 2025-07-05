import sqlite3
import pandas as pd
import os
import random

DB_PATH = "data/data.db"

def init_db():
    # Ensure directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            flight_date TEXT,
            dep_iata TEXT,
            arr_iata TEXT,
            airline TEXT,
            flight_number TEXT,
            status TEXT,
            price REAL
        )
    ''')
    # Try to add price column if missing (for upgrades)
    try:
        conn.execute('ALTER TABLE flights ADD COLUMN price REAL')
    except Exception:
        pass  # Ignore if already exists
    conn.commit()
    conn.close()
    print("✅ Database initialized and table ensured.")


def save_flights(json_data):
    if not json_data or "data" not in json_data:
        print("❌ No valid 'data' in response JSON.")
        return

    try:
        raw_data = json_data["data"]
        if not raw_data:
            print("⚠️ No flight data returned from API.")
            return

        df = pd.json_normalize(raw_data)
        print("✅ Raw data columns:", df.columns.tolist())

        # Define required columns
        required = [
            "flight_date",
            "departure.iata",
            "arrival.iata",
            "airline.name",
            "flight.number",
            "flight_status"
        ]

        # Check for missing columns
        missing = [col for col in required if col not in df.columns]
        if missing:
            print(f"❌ Missing expected columns in API data: {missing}")
            return

        # Rename columns for database
        df = df[required]
        df.columns = ["flight_date", "dep_iata", "arr_iata", "airline", "flight_number", "status"]

        # Add mock price column (random price between 100 and 500)
        df["price"] = [random.uniform(100, 500) for _ in range(len(df))]

        conn = sqlite3.connect(DB_PATH)
        df.to_sql("flights", conn, if_exists="append", index=False)
        conn.close()

        print(f"✅ Saved {len(df)} flights to database.")

    except Exception as e:
        print("❌ Error while processing/saving flights:", e)


def get_route_frequencies():
    """
    Returns a DataFrame of popular Australian domestic routes (origin → destination) with flight counts.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT dep_iata, arr_iata FROM flights", conn)
        conn.close()

        if df.empty:
            print("ℹ️ No routes found in database.")
            return None

        # Get Australian airports list
        australian_airports = [airport["code"] for airport in get_australian_airports()]
        
        # Filter for domestic flights only (both origin and destination are Australian airports)
        domestic_flights = df[
            (df['dep_iata'].isin(australian_airports)) & 
            (df['arr_iata'].isin(australian_airports))
        ]
        
        if domestic_flights.empty:
            print("ℹ️ No domestic routes found in database.")
            return None

        route_counts = (
            domestic_flights.groupby(["dep_iata", "arr_iata"])
            .size()
            .reset_index()
        )
        route_counts.columns = ["dep_iata", "arr_iata", "count"]
        route_counts["route"] = route_counts["dep_iata"] + " → " + route_counts["arr_iata"]
        sorted_routes = route_counts.sort_values(by="count", ascending=False)

        print(f"✅ Domestic route frequencies computed: {len(sorted_routes)} routes found.")
        return sorted_routes

    except Exception as e:
        print("❌ Error reading domestic routes from database:", e)
        return None


def get_flight_counts_by_date():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT flight_date FROM flights", conn)
    conn.close()
    
    if df.empty:
        return None
    
    date_counts = df.value_counts("flight_date").reset_index()
    date_counts.columns = ["flight_date", "count"]
    return date_counts.sort_values(by="flight_date")

def get_airline_counts():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT airline FROM flights", conn)
    conn.close()

    if df.empty:
        return None

    airline_counts = df.value_counts("airline").reset_index(name="count")
    return airline_counts.sort_values(by="count", ascending=False)

def get_price_trends():
    """Get price trends for Australian domestic flights only."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT flight_date, dep_iata, arr_iata, price FROM flights", conn)
    conn.close()
    
    if df.empty:
        return None
    
    # Get Australian airports list
    australian_airports = [airport["code"] for airport in get_australian_airports()]
    
    # Filter for domestic flights only
    domestic_flights = df[
        (df['dep_iata'].isin(australian_airports)) & 
        (df['arr_iata'].isin(australian_airports))
    ]
    
    if domestic_flights.empty:
        return None
    
    price_trends = domestic_flights.groupby("flight_date")["price"].mean().reset_index()
    price_trends.columns = ["flight_date", "avg_price"]
    return price_trends.sort_values(by="flight_date")

def get_price_range_stats():
    """Get comprehensive price range statistics for Australian domestic flights in AUD."""
    try:
        conn = sqlite3.connect(DB_PATH)
        # Get flights with both origin and destination to filter domestic routes
        df = pd.read_sql_query("SELECT dep_iata, arr_iata, price FROM flights WHERE price IS NOT NULL", conn)
        conn.close()
        
        if df.empty:
            return None
        
        # Get Australian airports list
        australian_airports = [airport["code"] for airport in get_australian_airports()]
        
        # Filter for domestic flights only (both origin and destination are Australian airports)
        domestic_flights = df[
            (df['dep_iata'].isin(australian_airports)) & 
            (df['arr_iata'].isin(australian_airports))
        ]
        
        if domestic_flights.empty:
            print("⚠️ No domestic flight data found.")
            return None
        
        prices = domestic_flights['price']
        
        # Calculate unique routes
        unique_routes = domestic_flights[['dep_iata', 'arr_iata']].drop_duplicates()
        
        stats = {
            'min_price': round(float(prices.min()), 2),
            'max_price': round(float(prices.max()), 2),
            'avg_price': round(float(prices.mean()), 2),
            'median_price': round(float(prices.median()), 2),
            'total_flights': len(prices),
            'total_routes': len(unique_routes),
            'price_ranges': {
                'Budget (Under $150)': len(prices[prices < 150]),
                'Economy ($150-$250)': len(prices[(prices >= 150) & (prices < 250)]),
                'Standard ($250-$350)': len(prices[(prices >= 250) & (prices < 350)]),
                'Premium ($350-$450)': len(prices[(prices >= 350) & (prices < 450)]),
                'Luxury ($450+)': len(prices[prices >= 450])
            }
        }
        
        print(f"✅ Domestic price stats: {len(prices)} flights across {stats['total_routes']} routes")
        return stats
        
    except Exception as e:
        print("❌ Error getting domestic price range stats:", e)
        return None

def get_australian_airports():
    """Return a list of major Australian airports with IATA codes and names."""
    airports = [
        {"code": "ADL", "name": "Adelaide Airport"},
        {"code": "ASP", "name": "Alice Springs Airport"},
        {"code": "AYQ", "name": "Ayers Rock Airport"},
        {"code": "BDB", "name": "Bundaberg Airport"},
        {"code": "BNE", "name": "Brisbane Airport"},
        {"code": "BNK", "name": "Ballina Byron Gateway Airport"},
        {"code": "BME", "name": "Broome Airport"},
        {"code": "BWT", "name": "Burnie Airport"},
        {"code": "CBR", "name": "Canberra Airport"},
        {"code": "CFS", "name": "Coffs Harbour Airport"},
        {"code": "CNS", "name": "Cairns Airport"},
        {"code": "DBO", "name": "Dubbo Airport"},
        {"code": "DRW", "name": "Darwin Airport"},
        {"code": "EMD", "name": "Emerald Airport"},
        {"code": "GFF", "name": "Griffith Airport"},
        {"code": "GLT", "name": "Gladstone Airport"},
        {"code": "HBA", "name": "Hobart Airport"},
        {"code": "HTI", "name": "Hamilton Island Airport"},
        {"code": "ISA", "name": "Mount Isa Airport"},
        {"code": "KGI", "name": "Kalgoorlie Airport"},
        {"code": "LST", "name": "Launceston Airport"},
        {"code": "LRE", "name": "Longreach Airport"},
        {"code": "MCY", "name": "Sunshine Coast Airport"},
        {"code": "MEL", "name": "Melbourne Airport"},
        {"code": "MKY", "name": "Mackay Airport"},
        {"code": "MRZ", "name": "Moree Airport"},
        {"code": "NTL", "name": "Newcastle Airport"},
        {"code": "OOL", "name": "Gold Coast Airport"},
        {"code": "PER", "name": "Perth Airport"},
        {"code": "PQQ", "name": "Port Macquarie Airport"},
        {"code": "ROK", "name": "Rockhampton Airport"},
        {"code": "SYD", "name": "Sydney Airport"},
        {"code": "TMW", "name": "Tamworth Airport"},
        {"code": "TSV", "name": "Townsville Airport"},
        {"code": "WGA", "name": "Wagga Wagga Airport"},
        {"code": "WOL", "name": "Wollongong Airport"},
        {"code": "ZNE", "name": "Newman Airport"}
    ]
    
    return sorted(airports, key=lambda x: x["name"])
