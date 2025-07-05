# Airline Demand Analysis Web App ✈️

A Flask web app that fetches and visualizes airline booking market demand across cities.

## Features
- ✅ Fetch live flight data (AviationStack Free API)
- 📊 Visualize:
  - Most popular routes
  - Flight demand trends over time
  - Top airlines
- 🧼 Data saved in SQLite for offline analysis
- 📦 Built with Flask, Plotly, Pandas

## Run Locally

```bash
git clone ...
cd airline-demand-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

