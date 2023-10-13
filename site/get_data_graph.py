import datetime
from typing import List, Tuple
import requests
from enum import Enum
import matplotlib.pyplot as plt
from dateutil.tz import tzutc, gettz
import config

API_URL = config.get("API_URL")
SPACE_ID = config.get("SPACE_ID")
API_TOKEN = config.get("API_TOKEN")


def friendly_time(input: int) -> str:
    input += 1
    t = input
    post = "AM"
    if input > 12:
        t = input - 12
        post = "PM"
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

deltas: List[Tuple[datetime.datetime, str]]
end: datetime.datetime


def update_global_times():
    global end, deltas
    end = datetime.datetime.now()
    deltas = [
        # (end - datetime.timedelta(weeks=1), "1wk"),
        (end - datetime.timedelta(weeks=2), "2wk"),
        (end - datetime.timedelta(days=30), "1mo"),
        (end - datetime.timedelta(days=365), "1yr"),
    ]


def get_data_graphs():
    for start, file_id in deltas:
        resp = get_historical_data(start, end, Interval.HOUR)

        for row in resp["results"]:
            timestamp = datetime.datetime.strptime(
                row["timestamp"], "%Y-%m-%dT%H:%M:%S%z"
            )
            timestamp = timestamp.astimezone(gettz("America/Los_Angeles"))

            day = timestamp.weekday()
            hour = timestamp.hour
            percentage_full = row["interval"]["analytics"]["utilization"]

            if len(data[day]) < hour + 1:
                data[day].append(percentage_full)
            else:
                data[day][hour] = (data[day][hour] + percentage_full) / 2

        fig = plt.figure(figsize=(10, 4))
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_xticklabels(
            [friendly_time(i) for i in range(0, 24)], fontsize=10, rotation=45
        )
        ax1.set_yticklabels(
            [
                "",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
            fontsize=10,
        )
        cbm = ax1.matshow(data, interpolation=None, cmap="plasma", aspect="auto")
        cb = plt.colorbar(cbm, ax=ax1)
        cb.set_label("Density (%)")

        plt.title(
            f"RSF Weight Room Density {start.strftime('%m/%d/%Y')} - {end.strftime('%m/%d/%Y')}"
        )
        plt.xticks(range(0, 24))
        plt.imshow(data, interpolation=None, cmap="plasma", aspect="auto")
        plt.tight_layout()
        plt.savefig(f"static/{file_id}.png", dpi=120)
