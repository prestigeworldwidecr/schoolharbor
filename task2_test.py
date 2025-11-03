# === CHECK: Task 2 — Latest Spring Assessments ===
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3, os

def _latest_by_key(df, key=["student_id","subject","season"], date="test_date") :
# {
    return df.sort_values(key + [date]).drop_duplicates(subset=key, keep="last")
# }

def check_task2(spring_latest: pd.DataFrame, assessments: pd.DataFrame) :
# {
    passed, tips = True, []
    need = {"student_id","subject","season","test_date","scale_score","perf_level"}

    if (need.issubset(spring_latest.columns)) :
    # {
        # return print_result(False, "Task 2 — Latest Spring Assessments", [f"Missing cols: {sorted(need - set(spring_latest.columns))}"])
        None    
    # }

    else :
    # {
        return print(False, "Task 2 — Latest Spring Assessments", ["Missing cols:", sorted(need - set(spring_latest.columns))])
    # }

    # 1) the raw data MUST actually contain duplicates per key (we injected them in setup)
    raw_dupes = assessments.duplicated(["student_id","subject","season"], keep=False).any()

    if (raw_dupes) :
    # {
        None
    # }
        
    else :
    # {
        passed = False
        tips.append("Raw assessments has no duplicate keys; ensure Setup duplicates were created.")
    # }

    # 2) spring_latest must be Spring only AND unique per (student_id, subject)
    if ((spring_latest["season"] == "Spring").all()) :
    # {
        None
    # }
        
    else :
    # {
        passed = False
        tips.append("Output must be filtered to Spring only.")
    # }

    if (spring_latest.duplicated(["student_id","subject"]).any()) :
    # {
        passed = False
        tips.append("Output still has duplicate (student_id, subject) rows.")
    # }

    else :
    # {
        None
    # }

    # 3) spring_latest must be the *latest* by test_date
    ref_spring = _latest_by_key(assessments).query('season == "Spring"')[["student_id","subject","test_date"]]
    merged = spring_latest.merge(ref_spring, on=["student_id","subject"], suffixes=("", "_ref"), how="outer")

    # coverage check
    if (merged.isna().any().any()) :
    # {
        passed = False
        tips.append("Key coverage mismatch vs expected latest Spring (outer join produced NaNs).")
    # }

    else :
    # {
        None
    # }

    # date check
    bad = (merged["test_date"] != merged["test_date_ref"]).sum()

    if (bad > 0) :
    # {
        passed = False
        tips.append(bad, "rows are not the latest by test_date.")
    # }

    else :
    # {
        None
    # }

    # size check (must equal unique (student,subject,Spring) combos in raw)
    expected_n = ref_spring.shape[0]

    if (len(spring_latest) == expected_n) :
    # {
        None
    # }

    else :
    # {
        passed = False
        tips.append("Row count mismatch: expected" + expected_n + "got" + len(spring_latest))
    # }

    # print_result(passed, "Task 2 — Latest Spring Assessments", tips)
    print(passed, "Task 2 — Latest Spring Assessments", tips)
# }

# 
# task2.py
#

assessments = pd.read_csv("data/assessments.csv", parse_dates=["test_date"])

# TODO: deduplicate by latest test_date per (student_id, subject, season)
assessments.drop_duplicates(subset = ["student_id", "subject", "season"], inplace = True)

# TODO: filter to spring only
assessments = assessments[assessments["season"] == "Spring"]

spring_latest = assessments.copy()
dup_keys = spring_latest.duplicated(subset=["student_id","subject"]).sum()

print("Duplicates after latest-per-key (should be 0):", dup_keys)
print(spring_latest.head())

check_task2(spring_latest, assessments)

'''

***** BONEYARD *****

# filtered_df = df[df[filter_column] == filter_value]
# roster_clean["school"] = roster_clean["school"].str.title().str.strip(' ')

# display(spring_latest.head())

'''