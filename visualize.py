# visualize.py
# Draws several charts comparing Delhi and Mumbai's air quality.

import pandas as pd
import matplotlib.pyplot as plt


def chart_daily_trend(aqi_df):
    """Chart 1: Daily AQI over time, both cities on one line chart."""
    delhi = aqi_df[aqi_df["city"] == "Delhi"].sort_values("date")
    mumbai = aqi_df[aqi_df["city"] == "Mumbai"].sort_values("date")

    plt.figure(figsize=(14, 6))
    plt.plot(delhi["date"], delhi["aqi"], label="Delhi", color="red")
    plt.plot(mumbai["date"], mumbai["aqi"], label="Mumbai", color="blue")
    plt.title("Daily Air Quality Index: Delhi vs Mumbai")
    plt.xlabel("Date")
    plt.ylabel("AQI (higher = worse air quality)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("data/chart_daily_trend.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved data/chart_daily_trend.png")


def chart_pollutant_comparison(clean_df):
    """Chart 2: Average level of each pollutant, side by side per city."""
    # Average value per city+pollutant combination
    averages = clean_df.groupby(["city", "pollutant"])["value"].mean().reset_index()

    # Reshape so each city becomes its own column, pollutants become rows
    pivoted = averages.pivot(index="pollutant", columns="city", values="value")

    pivoted.plot(kind="bar", figsize=(10, 6), color=["red", "blue"])
    plt.title("Average Pollutant Levels: Delhi vs Mumbai")
    plt.xlabel("Pollutant")
    plt.ylabel("Average concentration")
    plt.xticks(rotation=0)
    plt.grid(True, alpha=0.3, axis="y")
    plt.savefig("data/chart_pollutant_comparison.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved data/chart_pollutant_comparison.png")


def chart_dominant_pollutant(aqi_df):
    """Chart 3: How often each pollutant was the main cause of bad air."""
    counts = aqi_df.groupby(["city", "dominant_pollutant"]).size().reset_index(name="days")
    pivoted = counts.pivot(index="dominant_pollutant", columns="city", values="days").fillna(0)

    pivoted.plot(kind="bar", figsize=(10, 6), color=["red", "blue"])
    plt.title("Which Pollutant Drives Bad Air Quality Most Often")
    plt.xlabel("Pollutant")
    plt.ylabel("Number of days it was the worst pollutant")
    plt.xticks(rotation=0)
    plt.grid(True, alpha=0.3, axis="y")
    plt.savefig("data/chart_dominant_pollutant.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved data/chart_dominant_pollutant.png")


def chart_monthly_average(aqi_df):
    """Chart 4: Monthly average AQI, smoothing out daily noise."""
    aqi_df["month"] = aqi_df["date"].dt.to_period("M").astype(str)
    monthly = aqi_df.groupby(["city", "month"])["aqi"].mean().reset_index()

    delhi = monthly[monthly["city"] == "Delhi"]
    mumbai = monthly[monthly["city"] == "Mumbai"]

    plt.figure(figsize=(14, 6))
    plt.plot(delhi["month"], delhi["aqi"], label="Delhi", color="red", marker="o")
    plt.plot(mumbai["month"], mumbai["aqi"], label="Mumbai", color="blue", marker="o")
    plt.title("Monthly Average AQI: Delhi vs Mumbai")
    plt.xlabel("Month")
    plt.ylabel("Average AQI")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("data/chart_monthly_average.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved data/chart_monthly_average.png")


def main():
    aqi_df = pd.read_csv("data/aqi_data.csv")
    aqi_df["date"] = pd.to_datetime(aqi_df["date"])

    clean_df = pd.read_csv("data/air_quality_clean.csv")

    chart_daily_trend(aqi_df)
    chart_pollutant_comparison(clean_df)
    chart_dominant_pollutant(aqi_df)
    chart_monthly_average(aqi_df)

    print()
    print("All charts saved in the data folder.")


if __name__ == "__main__":
    main()