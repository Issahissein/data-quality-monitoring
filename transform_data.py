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

daily_traffic = (
    data.groupby("date")["visitors"]
    .sum()
    .reset_index()
)

print(daily_traffic)