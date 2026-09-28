import sys
from datetime import datetime

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

data = request_api(input_date)
print(data)