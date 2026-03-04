"""
This module builds the 10of10 and FSL baselines and calculates the performance for each 
hour of the event.
"""

import pandas as pd


def calc_10of10_baseline(historical: pd.DataFrame, hour: int) -> float:
    """
    Compute the 10-of-10 baseline for the given hour.

    Inputs:
    - historical: pre-filtered historical site data, with weekday/weekend split
      matching the event day type
    - hour: hour-of-day (0-23) to compute the baseline for

    Returns:
    - mean load_kw of the 10 most recent hours of the same type (i.e. same value
      of hour and weekday/weekend)
    """
    hour_df = historical[historical["timestamp"].dt.hour == hour]
    top_10 = hour_df.sort_values("timestamp", ascending=False).iloc[:10]
    return top_10["load_kw"].mean()


def build_10of10(
    df_hourly: pd.DataFrame, 
    event_df: pd.DataFrame, 
) -> pd.DataFrame:
    """
    Add 10of10 baseline and performance columns to event_df.

    Inputs:
    - df_hourly: hisotrical hourly load data
    - event_df: event-window rows (from build_event_hourly)

    Outputs:
    - event_df with added columns: hour, 10of10_baseline, 10of10_performance
    """

    if "hour" not in event_df.columns:
        event_df["hour"] = event_df["timestamp"].dt.hour

    event_start = event_df["timestamp"].min()
    is_weekend = event_start.weekday() >= 5
    
    if is_weekend:
        historical = df_hourly[
            (df_hourly["timestamp"] < event_start) &
            (df_hourly["timestamp"].dt.weekday >= 5)
        ]
    else:
        historical = df_hourly[
            (df_hourly["timestamp"] < event_start) &
            (df_hourly["timestamp"].dt.weekday < 5)
        ]

    baselines = {
        h: calc_10of10_baseline(historical, h)
        for h in event_df["hour"].unique()
    }

    event_df["10of10_baseline"] = event_df["hour"].map(baselines)
    event_df["10of10_performance"] = event_df["10of10_baseline"] - event_df["load_kw"]

    return event_df

def build_fsl(event_df: pd.DataFrame, fsl_baseline: int) -> pd.DataFrame:
    """
    Builds the FSL baselines and calculates the performance and adds the columns to 
    the event_df.
    """
    event_df["fsl_baseline"] = fsl_baseline
    event_df["fsl_performance"] = event_df["fsl_baseline"] - event_df["load_kw"]
    
    return event_df