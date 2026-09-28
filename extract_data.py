import sys
from datetime import datetime

try:
    input_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    print(input_date)
except ValueError:
    print("Invalid date")