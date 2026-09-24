# clean_data.py
# Reads the raw data and removes physically impossible sensor readings.

import pandas as pd

# These are the highest values that are physically realistic for each
# pollutant, based on India's official CPCB "Severe" pollution category.
# Anything above this is treated as a broken sensor reading, not real air.
realistic_max = {
    "pm25": 1000, "pm10": 1000, "no2": 600,
    "so2": 2000, "o3": 1000, "co": 50,
}


def main():
    df = pd.read_csv("data/air_quality_all.csv")
    print("Loaded", len(df), "rows")

    clean_pieces = []
    for pollutant, max_value in realistic_max.items():
        pollutant_rows = df[df["pollutant"] == pollutant]
        good_rows = pollutant_rows[pollutant_rows["value"] <= max_value]
        removed = len(pollutant_rows) - len(good_rows)
        print(pollutant, "- removed as broken readings:", removed)
        clean_pieces.append(good_rows)

    df_clean = pd.concat(clean_pieces, ignore_index=True)
    df_clean.to_csv("data/air_quality_clean.csv", index=False)
    print("Saved", len(df_clean), "rows to data/air_quality_clean.csv")


if __name__ == "__main__":
    main()