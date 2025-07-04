from flask import Flask, request, render_template, send_file, Response
from utils.aviationstack_api import fetch_flights
from utils.data_utils import init_db, save_flights, get_route_frequencies, get_price_trends
import plotly.graph_objs as go
import os
import openai  # Add this import at the top if using OpenAI API
import io
import csv
import pandas as pd

app = Flask(__name__)
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    flights = None
    message = None

    if request.method == "POST":
        origin = request.form["origin"].upper()
        destination = request.form.get("destination", "").upper()
        date = request.form.get("date")  # optional, not used in API call

        if not origin or len(origin) != 3:
            message = "❌ Please enter a valid 3-letter IATA airport code."
            return render_template("index.html", flights=None, message=message)

        # ❗ FIX: Do not pass flight_date to fetch_flights
        data = fetch_flights(origin)

        print("🔍 Raw API JSON:")
        print(data)

        if data and "data" in data and len(data["data"]) > 0:
            save_flights(data)
            flights = data["data"]
            # Filter by destination if provided
            if destination:
                flights = [f for f in flights if f.get("arrival", {}).get("iata", "").upper() == destination]
            message = f"✅ {len(flights)} flights fetched and saved."
        else:
            message = "❌ No flight data found. Try a different IATA code."

    return render_template("index.html", flights=flights, message=message)

@app.route("/chart")
def chart():
    data = get_route_frequencies()

    if data is None or data.empty:
        print("⚠️ No data found for chart.")
        return render_template("chart.html", chart="<h3>No data to show. Please fetch flights first.</h3>")

    fig = go.Figure([go.Bar(x=data["route"], y=data["count"])])
    fig.update_layout(
        title="Most Frequent Flight Routes",
        xaxis_title="Route",
        yaxis_title="Number of Flights",
        xaxis_tickangle=-45
    )

    chart_html = fig.to_html(full_html=False)
    return render_template("chart.html", chart=chart_html)

@app.route("/demand")
def demand():
    from utils.data_utils import get_flight_counts_by_date
    data = get_flight_counts_by_date()

    if data is None or data.empty:
        return render_template("chart.html", chart="<h3>No data available to show demand trends.</h3>")

    fig = go.Figure([go.Scatter(x=data["flight_date"], y=data["count"], mode="lines+markers")])
    fig.update_layout(title="Flight Demand Over Time", xaxis_title="Date", yaxis_title="Flights per Day")

    chart_html = fig.to_html(full_html=False)
    return render_template("chart.html", chart=chart_html)

@app.route("/airlines")
def airlines():
    from utils.data_utils import get_airline_counts
    data = get_airline_counts()

    if data is None or data.empty:
        return render_template("chart.html", chart="<h3>No data to show airline frequency.</h3>")

    fig = go.Figure([go.Bar(x=data["airline"], y=data["count"])])
    fig.update_layout(title="Airline Frequencies", xaxis_title="Airline", yaxis_title="Flight Count", xaxis_tickangle=-45)

    chart_html = fig.to_html(full_html=False)
    return render_template("chart.html", chart=chart_html)

@app.route("/insights")
def insights():
    # Gather summary stats
    from utils.data_utils import get_route_frequencies, get_flight_counts_by_date, get_airline_counts
    route_data = get_route_frequencies()
    date_data = get_flight_counts_by_date()
    airline_data = get_airline_counts()

    # Prepare a summary string for the LLM
    summary = ""
    if route_data is not None and not route_data.empty:
        top_route = route_data.iloc[0]
        summary += f"Most popular route: {top_route['route']} with {top_route['count']} flights.\n"
    if date_data is not None and not date_data.empty:
        busiest_day = date_data.sort_values('count', ascending=False).iloc[0]
        summary += f"Busiest day: {busiest_day['flight_date']} with {busiest_day['count']} flights.\n"
    if airline_data is not None and not airline_data.empty:
        top_airline = airline_data.iloc[0]
        summary += f"Most frequent airline: {top_airline['airline']} with {top_airline['count']} flights.\n"
    if not summary:
        summary = "No data available for insights. Please fetch some flights first."

    # Use OpenAI or another LLM to generate insights
    ai_insight = None
    if summary != "No data available for insights. Please fetch some flights first.":
        try:
            openai.api_key = "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"
            prompt = (
                "You are an expert in airline market analysis. Based on the following stats, provide a concise, actionable summary of market demand trends for a hostel business in Australia.\n" + summary
            )
            response = openai.Client().chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                          {"role": "user", "content": prompt}]
            )
            if response and response.choices and response.choices[0].message and response.choices[0].message.content:
                ai_insight = response.choices[0].message.content.strip()
            else:
                ai_insight = "Error: No response received from AI model"
        except Exception as e:
            ai_insight = f"Error generating AI insight: {e}"
    else:
        ai_insight = summary

    return render_template("insights.html", ai_insight=ai_insight)

@app.route("/price-trends")
def price_trends():
    from utils.data_utils import get_price_trends
    data = get_price_trends()
    if data is None or data.empty:
        return render_template("price_trends.html", chart="<h3>No price data to show. Please fetch flights first.</h3>")
    fig = go.Figure([go.Scatter(x=data["flight_date"], y=data["avg_price"], mode="lines+markers")])
    fig.update_layout(title="Average Flight Price Over Time", xaxis_title="Date", yaxis_title="Average Price (AUD)")
    chart_html = fig.to_html(full_html=False)
    return render_template("price_trends.html", chart=chart_html)

@app.route("/export/flights")
def export_flights():
    import sqlite3
    conn = sqlite3.connect("data/data.db")
    df = pd.read_sql_query("SELECT * FROM flights", conn)
    conn.close()
    output = io.StringIO()
    if df is None or df.empty:
        output.write("No data available\n")
    else:
        df.to_csv(output, index=False)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=flights.csv"})

@app.route("/export/routes")
def export_routes():
    from utils.data_utils import get_route_frequencies
    df = get_route_frequencies()
    output = io.StringIO()
    if df is None or df.empty:
        output.write("No data available\n")
    else:
        df.to_csv(output, index=False)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=routes.csv"})

@app.route("/export/demand")
def export_demand():
    from utils.data_utils import get_flight_counts_by_date
    df = get_flight_counts_by_date()
    output = io.StringIO()
    if df is None or df.empty:
        output.write("No data available\n")
    else:
        df.to_csv(output, index=False)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=demand.csv"})

@app.route("/export/airlines")
def export_airlines():
    from utils.data_utils import get_airline_counts
    df = get_airline_counts()
    output = io.StringIO()
    if df is None or df.empty:
        output.write("No data available\n")
    else:
        df.to_csv(output, index=False)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=airlines.csv"})

@app.route("/export/price-trends")
def export_price_trends():
    from utils.data_utils import get_price_trends
    df = get_price_trends()
    output = io.StringIO()
    if df is None or df.empty:
        output.write("No data available\n")
    else:
        df.to_csv(output, index=False)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=price_trends.csv"})

if __name__ == "__main__":
    app.run(debug=True)
