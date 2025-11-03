import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3, os

# === CHECK: Task 6 — Helper Function ===

def _make_dupe_df(base_df, key=["student_id","subject","season"], date="test_date", n_dupes=300) :
# {
    # Create a test df with guaranteed duplicates where the duplicate has a LATER date.
    base_df = base_df.copy()

    # ensure datetime dtype
    if (np.issubdtype(base_df[date].dtype, np.datetime64)) :
    # {
        None
    # }

    else : 
    # {
        base_df[date] = pd.to_datetime(base_df[date])
    # }

    n_dupes = min(n_dupes, len(base_df)//3 if len(base_df) >= 3 else 0)

    if (n_dupes == 0) :
    # {
        return base_df
    # }

    else :
    # {
        None    
    # }

    idx = np.random.choice(base_df.index, size=n_dupes, replace=False)
    dupes = base_df.loc[idx].copy()
    dupes[date] = dupes[date] + pd.to_timedelta(np.random.randint(1, 10, size=len(dupes)), unit='D')

    for c in base_df.columns :
    # {
        if (c in key+[date] and base_df[c].dtype.kind in "if") :
        # {
            None
        # }

        else :
        # {
            dupes[c] = dupes[c] + np.random.normal(0, 1, size=len(dupes))
        # }

    # }

    return pd.concat([base_df, dupes], ignore_index=True)

# }

def check_task6_strict(select_latest, assessments: pd.DataFrame) :
# {
    passed = True
    tips = []
    key = ["student_id","subject","season"]
    date = "test_date"

    # Build a df that DEFINITELY needs deduping
    test_df = _make_dupe_df(assessments, key=key, date=date, n_dupes=400)

    # Ground-truth via reference method
    ref = (test_df.sort_values(key + [date]).drop_duplicates(subset=key, keep="last"))

    # 1) function must run
    try :
    # {
        out = select_latest(test_df.copy(), key, date)
    # }

    except Exception as e :
    # {
        # return print_result(False, "Task 6 — Helper Function", [f"Function raised exception: {e}"])
        return print(False, "Task 6 — Helper Function", ["Function raised exception:", e])
    # }

    # 2) must reduce duplicates → rows == number of unique keys
    expected_n = ref.shape[0]

    if (len(out) == expected_n) :
    # {
        None
    # }

    else :
    # {
        passed = False
        tips.append("Output has wrong number of rows. Expected", expected_n, "got", len(out))
    # }

    # 3) must be unique by key
    if (out.duplicated(key).any()) :
    # {
        passed = False
        tips.append("Output still has duplicate keys after select_latest.")
    # }

    else :
    # {
        None    
    # }

    # 4) must pick the *latest* date for each key
    merged = out.merge(ref[key+[date]], on=key, how="outer", suffixes=("", "_ref"))

    if (merged.isna().any().any()) :
    # {
        passed = False
        tips.append("Key coverage mismatch vs expected latest rows (NaNs after join).")
    # }

    else :
    # {
        None
    # }

    bad = (merged[date] != merged[f"{date}_ref"]).sum()

    if (bad > 0) :
    # {
        passed = False
        tips.append(bad, "keys are not selecting the latest", date)
    # }

    else :
    # {
        None    
    # }

    # print_result(passed, "Task 6 — Helper Function", tips)
    print(passed, "Task 6 — Helper Function", tips)

# }

assessments_for_check = pd.read_csv("data/assessments.csv", parse_dates=["test_date"])
check_task6_strict(select_latest, assessments_for_check)