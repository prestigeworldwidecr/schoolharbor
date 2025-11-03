import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3, os

def run_sql(query: str) -> pd.DataFrame :
# {
    conn = sqlite3.connect("schoolharbor.db")

    try :
    # {
        df = pd.read_sql_query(query, conn)
    # }

    finally :
    # {
        conn.close()
    # }

    return df

# }

# Bring in your `roster_clean` and `spring_latest` tables from Python (no edits required)
conn = sqlite3.connect("schoolharbor.db")
roster_clean.to_sql("roster_clean_sql", conn, if_exists="replace", index=False)
spring_latest.to_sql("spring_latest_sql", conn, if_exists="replace", index=False)
conn.close()


# Write and run your SQL:
sql_5a = 
# Return: school, spring_tested, spring_prof_rate

df_5a = run_sql(sql_5a) if sql_5a.strip() else pd.DataFrame()
# display(df_5a.head())
print(df_5a.head())

sql_5b = 
# Return: school, program, enrollees, seats, fill_rate

df_5b = run_sql(sql_5b) if sql_5b.strip() else pd.DataFrame()
# display(df_5b.head())
print(df_5b.head())