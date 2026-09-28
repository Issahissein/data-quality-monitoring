import sys
from datetime import datetime, date, timedelta
from pathlib import Path

import pandas as pd
import requests


def request_api(business_date):
    url = "http://127.0.0.1:8000/visits"
    response = requests.get(
        url,
        params={"business_date": business_date},
    )
    return response.json()


try:
    input_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
except ValueError:
    print("Invalid date")
    sys.exit()


all_data = []
current_date = input_date

while current_date <= date.today():
    data = request_api(current_date)
    all_data.extend(data)

    current_date += timedelta(days=1)


df = pd.DataFrame(all_data)

# Add unreliable data
if not df.empty:
    bad_sensor_data = df.sample(n=1).copy()
    bad_sensor_data["sensor_id"] = None

    bad_unit_data = df.sample(n=1).copy()
    bad_unit_data["unit"] = "bananas"

    df = pd.concat(
        [df, bad_sensor_data, bad_unit_data],
        ignore_index=True,
    )


# Create data/raw directory
output_directory = Path("data/raw")
output_directory.mkdir(parents=True, exist_ok=True)


# Create one CSV per month
df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")

for month, monthly_data in df.groupby("month"):
    monthly_data = monthly_data.drop(columns=["month"])

    output_file = output_directory / f"visits_{month}.csv"

    monthly_data.to_csv(
        output_file,
        index=False,
    )

    print(f"Created {output_file}")