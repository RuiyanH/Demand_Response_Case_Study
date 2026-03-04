"""
This module turns raw site CSVs into standardized hourly load data.
"""

import pandas as pd

from src.config import TIMEZONE

def load_site(csv_path, tz=TIMEZONE):
    """
    Inputs: 
    - csv_path: path to the csv file containing the site data
    - tz: timezone of the data
    - KEY ASSUMPTION: 
        - first column is the timestamp in time zone tz
        - second column is the load in kwh

    outputs:
    - df: a dataframe with 2 columns:
        - timestamp: time adjusted to EDT
        - load_kw: the load in kw
    """
    df = pd.read_csv(csv_path)

    if df.shape[1] < 2:
        raise ValueError(f"{csv_path}: expected to have at least 2 columns, got {df.shape[1]}")

    df["timestamp"] = pd.to_datetime(df.iloc[:,0])
    df["timestamp"] = df["timestamp"].dt.tz_localize(tz)
    df["timestamp"] = df["timestamp"].dt.tz_convert("America/New_York")

    interval_min = (df["timestamp"].iloc[1] - df["timestamp"].iloc[0]).total_seconds() / 60
    df["load_kw"] = df.iloc[:,1] * 60.0 / interval_min

    df = df[["timestamp", "load_kw"]]

    return df


def to_hourly(df):
    """
    Resample data to hourly means.
    """
    hourly = df.set_index("timestamp").resample("h").mean().reset_index()
    return hourly


def load_site_hourly(csv_path, tz=TIMEZONE):
    """
    Wrapper: load a site CSV and resample to hourly.
    """
    return to_hourly(load_site(csv_path, tz))


def slice_event_hourly(df_hourly, start, end):
    """
    Filter hourly data to the event window [start, end).
    """
    event_slice = df_hourly[
        (df_hourly["timestamp"] >= start) & 
        (df_hourly["timestamp"] < end)
    ]

    return event_slice
