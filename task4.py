import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3, os

attendance = pd.read_csv("data/attendance.csv", parse_dates=["date"])

# TODO: compute ADA grouped by school and YYYY-MM

ada_by_school_month = # replace

# display(ada_by_school_month.head(10))
print(ada_by_school_month.head(10))