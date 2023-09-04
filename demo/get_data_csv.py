import csv
import datetime
import requests
from enum import Enum

API_URL = "https://api.density.io/v2/spaces"
SPACE_ID = "spc_863128347956216317"
API_TOKEN = "shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e"

class Interval(Enum):
    MINUTE = "1m"
    HOUR = "1h"
    DAY = "1d"
    WEEK = "1w"

def get_historical_data(start, end, interval):
    """ Get historical data from density.io """

    start = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    url = "{}/{}/counts?start_time={}&end_time={}&interval={}&page=1&page_size=5000".format(API_URL, SPACE_ID, start, end, interval.value)

    response = requests.get(url, headers={"Authorization": "Bearer {}".format(API_TOKEN)})

    return response.json()

columns = [
    "timestamp", 
    "min_number", 
    "max_number",
    "percentage_full",
    "entry_rate",
    "exit_rate"
]

end = datetime.datetime.now()
start = datetime.datetime.now() - datetime.timedelta(days=31)

res = get_historical_data(
    start=start,
    end=end,
    interval=Interval.HOUR
)

print("Start:\t\t", start)
print("End:\t\t", end)
print("Entries:\t", len(res["results"]))

with open('rsf.csv', 'a+') as csvfile:
    writer = csv.DictWriter(csvfile, columns)

    num_lines = sum(1 for line in csvfile)
    if num_lines == 0:
        writer.writeheader()

    for entry in res["results"]:
        writer.writerow({
            "timestamp": entry["timestamp"], 
            "min_number": entry["interval"]["analytics"]["min"], 
            "max_number": entry["interval"]["analytics"]["max"],
            "percentage_full": entry["interval"]["analytics"]["utilization"],
            "entry_rate": entry["interval"]["analytics"]["entry_rate"],
            "exit_rate": entry["interval"]["analytics"]["exit_rate"]
        })
