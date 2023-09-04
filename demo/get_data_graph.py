import datetime
import requests
from enum import Enum
import matplotlib.pyplot as plt
from dateutil.tz import tzutc, gettz

API_URL = "https://api.density.io/v2/spaces"
SPACE_ID = "spc_863128347956216317"
API_TOKEN = "shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e"


def friendly_time(input: int) -> str:
    input += 1
    t = input
    post = "AM"
    if input > 12:
        t = input - 12
        post = "PM"
    elif input == 0:
        t = 12
    return f"{t}{post}"


class Interval(Enum):
    MINUTE = "1m"
    HOUR = "1h"
    DAY = "1d"
    WEEK = "1w"


def get_historical_data(start, end, interval):
    """Get historical data from density.io"""

    start = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    url = "{}/{}/counts?start_time={}&end_time={}&interval={}&page=1&page_size=5000".format(
        API_URL, SPACE_ID, start, end, interval.value
    )

    response = requests.get(
        url, headers={"Authorization": "Bearer {}".format(API_TOKEN)}
    )

    return response.json()


data = [[] for i in range(0, 7)]

end = datetime.datetime.now()
deltas = [
    ("1 Week", end - datetime.timedelta(weeks=1), "1wk"),
    ("2 Weeks", end - datetime.timedelta(weeks=2), "2wk"),
    ("1 Month", end - datetime.timedelta(weeks=4), "1mo"),
    ("1 Year", end - datetime.timedelta(days=365), "1yr"),
]

for name, start, file_id in deltas:
    resp = get_historical_data(start, end, Interval.HOUR)

    for row in resp["results"]:
        timestamp = datetime.datetime.strptime(row["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        timestamp = timestamp.astimezone(gettz("America/Los_Angeles"))

        day = timestamp.weekday()
        hour = timestamp.hour
        percentage_full = row["interval"]["analytics"]["utilization"]

        if len(data[day]) < hour + 1:
            data[day].append(percentage_full)
        else:
            data[day][hour] = (data[day][hour] + percentage_full) / 2

    fig = plt.figure(figsize=(10, 8))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.set_xticklabels(
        [friendly_time(i) for i in range(0, 24)], fontsize=10, rotation=45
    )
    ax1.set_yticklabels( [ "", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", ], fontsize=10)
    cbm = ax1.matshow(data, interpolation=None, cmap="plasma", aspect="auto")
    cb = plt.colorbar(cbm, ax=ax1)
    cb.set_label("Density (%)")

    plt.xticks(range(0, 24))
    plt.imshow(data, interpolation=None, cmap="plasma", aspect="auto")
    plt.tight_layout()
    plt.savefig(f"static/{deltas}.png", dpi=120)
