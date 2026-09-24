# calculate_aqi.py
# Converts raw pollutant readings into official India AQI scores,
# using CPCB's published breakpoint tables.

import pandas as pd

breakpoints = {
    "pm25": [(0,30,0,50), (30,60,51,100), (60,90,101,200), (90,120,201,300), (120,250,301,400), (250,1000,401,500)],
    "pm10": [(0,50,0,50), (50,100,51,100), (100,250,101,200), (250,350,201,300), (350,430,301,400), (430,1000,401,500)],
    "no2":  [(0,40,0,50), (40,80,51,100), (80,180,101,200), (180,280,201,300), (280,400,301,400), (400,600,401,500)],
    "so2":  [(0,40,0,50), (40,80,51,100), (80,380,101,200), (380,800,201,300), (800,1600,301,400), (1600,2000,401,500)],
    "o3":   [(0,50,0,50), (50,100,51,100), (100,168,101,200), (168,208,201,300), (208,748,301,400), (748,1000,401,500)],
    "co":   [(0,1.0,0,50), (1.0,2.0,51,100), (2.0,10,101,200), (10,17,201,300), (17,34,301,400), (34,50,401,500)],
}


def get_sub_index(value, pollutant_breakpoints):
    """Converts one raw pollutant value into its 0-500 AQI sub-index."""
    for conc_low, conc_high, aqi_low, aqi_high in pollutant_breakpoints:
        if conc_low <= value <= conc_high:
            sub_index = ((aqi_high - aqi_low) / (conc_high - conc_low)) * (value - conc_low) + aqi_low
            return round(sub_index)
    return None


def main():
    df = pd.read_csv("data/air_quality_clean.csv")
    wide = df.pivot_table(index=["date", "city"], columns="pollutant", values="value").reset_index()

    results = []
    for index, row in wide.iterrows():
        sub_indexes = {}
        for pollutant in breakpoints:
            value = row[pollutant]
            if pd.notna(value):
                sub_index = get_sub_index(value, breakpoints[pollutant])
                if sub_index is not None:
                    sub_indexes[pollutant] = sub_index

        if len(sub_indexes) == 0:
            continue

        # The overall AQI is the WORST sub-index that day (CPCB's official rule)
        dominant_pollutant = max(sub_indexes, key=sub_indexes.get)
        aqi = sub_indexes[dominant_pollutant]

        results.append({
            "date": row["date"],
            "city": row["city"],
            "aqi": aqi,
            "dominant_pollutant": dominant_pollutant
        })

    aqi_df = pd.DataFrame(results)
    aqi_df.to_csv("data/aqi_data.csv", index=False)
    print("Saved", len(aqi_df), "rows to data/aqi_data.csv")


if __name__ == "__main__":
    main()