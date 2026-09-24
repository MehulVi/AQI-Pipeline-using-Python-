# India Air Quality Analytics Pipeline

An end-to-end data pipeline that pulls real air quality sensor data from the OpenAQ API for Delhi and Mumbai, cleans it, calculates official India AQI scores using CPCB's published formula, and visualizes pollution trends.

## What this project does
- Pulls 500+ days of real daily pollutant readings (PM2.5, PM10, NO2, SO2, CO, O3) via API
- Handles real-world API issues: timeouts, pagination, missing sensor data
- Cleans data using domain-informed rules (India's CPCB severity thresholds), not blind statistics
- Calculates real AQI values using India's official sub-index formula
- Visualizes daily trends, pollutant breakdowns, and dominant-pollutant analysis

## Tech stack
Python, Pandas, Matplotlib, OpenAQ API, python-dotenv

## How to run
1. Clone this repo
2. Create a virtual environment and install: `pip install requests pandas matplotlib python-dotenv`
3. Get a free API key at explore.openaq.org and add it to a `.env` file as `OPENAQ_API_KEY=your_key`
4. Run in order: `fetch_data.py` → `clean_data.py` → `calculate_aqi.py` → `visualize.py`

## Sample output
![AQI Comparison](data/chart_daily_trend.png)