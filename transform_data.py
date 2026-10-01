from pathlib import Path

import pandas as pd


data_directory = Path("data/raw")

csv_files = data_directory.glob("*.csv")

dataframes = []

for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    dataframes.append(df)

data = pd.concat(dataframes, ignore_index=True)

# Remove rows with missing values
data = data.dropna()

# Remove rows with unexpected units
data = data[data["unit"] == "visitors"]

# Convert date to datetime
data["date"] = pd.to_datetime(data["date"])

# Group hourly traffic by day, store and sensor
daily_traffic = (
    data.groupby(
        ["date", "store_id", "sensor_id"],
        as_index=False,
    )["visitors"]
    .sum()
)

# Add day of week
daily_traffic["day_of_week"] = (
    daily_traffic["date"].dt.day_name()
)

# Sort before applying the window
daily_traffic = daily_traffic.sort_values(
    by=[
        "day_of_week",
        "store_id",
        "sensor_id",
        "date",
    ]
)

# Average of the 4 previous same days of the week
daily_traffic["average_last_4"] = (
    daily_traffic.groupby(
        ["day_of_week", "store_id", "sensor_id"]
    )["visitors"]
    .transform(
        lambda values: values.shift(1).rolling(
            window=4,
            min_periods=1,
        ).mean()
    )
)

# Percentage difference from the average
daily_traffic["pct_change"] = (
    (
        daily_traffic["visitors"]
        - daily_traffic["average_last_4"]
    )
    / daily_traffic["average_last_4"]
    * 100
)

# Save processed data as Parquet
output_directory = Path("data/processed")
output_directory.mkdir(parents=True, exist_ok=True)

output_file = output_directory / "filtered.parquet"

daily_traffic.to_parquet(
    output_file,
    index=False,
)

print(daily_traffic)