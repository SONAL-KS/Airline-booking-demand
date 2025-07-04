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
    Returns a DataFrame of popular routes (origin → destination) with flight counts.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT dep_iata, arr_iata FROM flights", conn)
        conn.close()

        if df.empty:
            print("ℹ️ No routes found in database.")
            return None

        route_counts = (
            df.groupby(["dep_iata", "arr_iata"])
            .size()
            .reset_index()
        )
        route_counts.columns = ["dep_iata", "arr_iata", "count"]
        route_counts["route"] = route_counts["dep_iata"] + " → " + route_counts["arr_iata"]
        sorted_routes = route_counts.sort_values(by="count", ascending=False)

        print("✅ Route frequencies computed.")
        return sorted_routes

    except Exception as e:
        print("❌ Error reading routes from database:", e)
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
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT flight_date, price FROM flights", conn)
    conn.close()
    if df.empty:
        return None
    price_trends = df.groupby("flight_date")["price"].mean().reset_index()
    price_trends.columns = ["flight_date", "avg_price"]
    return price_trends.sort_values(by="flight_date")
