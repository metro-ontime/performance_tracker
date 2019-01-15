import pandas as pd
import pendulum


class NextBusData:
    def __init__(self, data):
        obj = data
        self.last_report_time = get_last_report_time(obj)
        self.vehicles = get_vehicles(obj, self.last_report_time)


def get_vehicles(data, last_report_time):
    try:
        df = pd.DataFrame(data["vehicle"])
    except:
        if type(data["vehicle"]) is dict:
            df = pd.DataFrame(data["vehicle"], index=[0])

    df = matchColumnNames(df)
    min_secs_since_report = min(list(map(int, list(df["seconds_since_report"]))))
    df["report_time"] = df.apply(
        lambda row: get_report_time(
            last_report_time, min_secs_since_report, int(row.seconds_since_report)
        ),
        axis=1,
    )
    return df[
        [
            "vehicle_id",
            "direction",
            "report_time",
            "latitude",
            "longitude",
            "predictable",
        ]
    ]


def get_last_report_time(data):
    return int(data["lastTime"]["time"]) / 1000


def get_report_time(last_report_time, offset, secs_since_report):
    # This method is up for debate.
    # To account for possible latency in the connection, we are subtracting
    # "seconds_since_report" from the last report time,
    # not the time the request was made or the time returned in the header.
    # Therefore an "offset" is added - equal to the seconds_since_report
    # of the most recent report, in order to make seconds_since_report
    # relative to the last report time --> not "now".
    # The reason for not using "now" is that it is unclear what
    # seconds_since_report is measured relative to. No info from NextBus
    # or Metro on this.
    return pendulum.from_timestamp(
        int(last_report_time + offset - secs_since_report)
    ).to_rfc3339_string()


def matchColumnNames(df):
    return df.rename(
        columns={
            "id": "vehicle_id",
            "heading": "direction",
            "secsSinceReport": "seconds_since_report",
            "lat": "latitude",
            "lon": "longitude",
        }
    )
