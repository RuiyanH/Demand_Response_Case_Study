# src/config.py

import pandas as pd

# Timezone used in the raw data 
TIMEZONE = "EST"

# Event window (start inclusive, end exclusive)
EVENT_START = pd.Timestamp("2022-06-14 14:00", tz="America/New_York")
EVENT_END = pd.Timestamp("2022-06-14 18:00", tz="America/New_York")

# FSL baseline
FSL_KW = {
    "site_1": 10700,
    "site_2": 5400,
    "site_3": 850,
    "site_5": 9000,
    "site_6": 350,
}

LMP = {
    "2022-06-14 14:00:00-04:00": 1500,
    "2022-06-14 15:00:00-04:00": 1800,
    "2022-06-14 16:00:00-04:00": 3000,
    "2022-06-14 17:00:00-04:00": 780,
}

REVENUE_SHARE = {
    "site_1": 0.64,
    "site_2": 0.62,
    "site_3": 0.56,
    "site_5": 0.65,
    "site_6": 0.51,
}