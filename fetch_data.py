# fetch_data.py
# Pulls daily air pollution data for Delhi and Mumbai from the OpenAQ API
# and saves it as one combined CSV file.

import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAQ_API_KEY")
headers = {"X-API-Key": api_key}

# We split the date range into smaller chunks because asking for
# too much data in one request causes the API to time out.
date_chunks = [
    ("2025-02-18", "2025-03-31"),
    ("2025-04-01", "2025-05-31"),
    ("2025-06-01", "2025-07-31"),
    ("2025-08-01", "2025-09-30"),
    ("2025-10-01", "2025-11-30"),
    ("2025-12-01", "2026-01-31"),
    ("2026-02-01", "2026-03-31"),
    ("2026-04-01", "2026-05-31"),
    ("2026-06-01", "2026-07-31"),
    ("2026-08-01", "2026-09-08"),
]

# Which sensor ID to use for each city and pollutant.
# We found these earlier by scanning OpenAQ's station list.
sensors = {
    "Delhi": {
        "pm25": 12234787, "pm10": 12234786, "no2": 12234784,
        "so2": 12234789, "co": 12234782, "o3": 12234785,
    },
    "Mumbai": {
        "pm25": 12235834, "pm10": 12235833, "no2": 12235831,
        "so2": 12289836, "co": 12235829, "o3": 12235832,
    },
}


def fetch_sensor_data(sensor_id, city, pollutant):
    """Downloads all daily readings for one sensor, in date chunks."""
    rows = []
    for start, end in date_chunks:
        url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements/daily"
        params = {"datetime_from": start, "datetime_to": end, "limit": 1000}
        response = requests.get(url, headers=headers, params=params)
        print(city, pollutant, start, "to", end, "-> status:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            for day in data["results"]:
                rows.append({
                    "date": day["period"]["datetimeFrom"]["local"],
                    "city": city,
                    "pollutant": pollutant,
                    "value": day["value"]
                })
    return rows


def main():
    all_rows = []
    for city, pollutants in sensors.items():
        for pollutant, sensor_id in pollutants.items():
            all_rows.extend(fetch_sensor_data(sensor_id, city, pollutant))

    df = pd.DataFrame(all_rows)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/air_quality_all.csv", index=False)
    print("Saved", len(df), "rows to data/air_quality_all.csv")


if __name__ == "__main__":
    main()