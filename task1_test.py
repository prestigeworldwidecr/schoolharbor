import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3, os
import task1

# === CHECK: Task 1 — Roster Cleaning ===
def check_task1(roster_clean: pd.DataFrame, roster_raw: pd.DataFrame) :
# {
    passed, tips = True, []
    req_cols = {"student_id","first_name","last_name","school","grade"}

    if (req_cols.issubset(roster_clean.columns)) :
    # {
        # return print_result(False, "Task 1 — Roster Cleaning",
        None
    # } 
    
    else :
    # {
        return print(False, "Task 1 — Roster Cleaning", ["Missing:", sorted(req_cols - set(roster_clean.columns))])
    # }

    # 1. Check stripping + Title Case for string columns
    for col in ["first_name","last_name","school"] :
    # {
        norm = roster_clean[col].fillna("").astype(str).str.strip().str.title()

        if (roster_clean[col].fillna("").equals(norm)) :

            None

        else :
        # {
            passed = False
            tips.append("Column", col, "not fully stripped+title-cased.")
        # }

    # }

    # 2. Ensure no duplicate student_id
    if (roster_clean["student_id"].duplicated().any()) :
    # {
        passed = False
        tips.append("Duplicate student_id values remain—dedup by student_id.")
    # }

    else :
    # {
        None
    # }

    # 3. Grade must be string dtype and valid
    if (pd.api.types.is_string_dtype(roster_clean["grade"])) :
    # {
        None
    # }

    else :
    # {
        passed = False
        tips.append("Column 'grade' is not string dtype. Cast it with astype(str).")
    # }

    valid = set(["K"] + [str(i) for i in range(1,13)])
    bad_vals = set(roster_clean["grade"].unique()) - valid

    if (bad_vals) :
    # {
        passed = False
        tips.append("Invalid grade values found:" + str(sorted(bad_vals)))
    # }

    else :
    # {
        None
    # }

    # print_result(passed, "Task 1 — Roster Cleaning", tips)
    print(passed, "Task 1 — Roster Cleaning", tips)
# }

#
# task1.py
# 

roster = pd.read_csv("data/roster.csv", parse_dates=["dob"])

# TODO: implement cleaning -> roster_clean

roster_clean = roster.copy()

# Step 1
# Standardize first_name, last_name, and school to Title Case and trim whitespace
roster_clean["first_name"] = roster_clean["first_name"].str.title().str.strip(' ')
roster_clean["last_name"] = roster_clean["last_name"].str.title().str.strip(' ')
roster_clean["school"] = roster_clean["school"].str.title().str.strip(' ')

# Step 2
# Deduplicate by student_id, keeping the first occurrence
roster_clean.drop_duplicates(subset = "student_id", inplace = True)

# Step 3
# Ensure grade is a string with values K,1,2,3,4,5,6,7,8,9,10,11,12.
roster_clean["grade"] = roster_clean["grade"].replace({"6.0" : "6"})
roster_clean["grade"] = roster_clean["grade"].replace({"hs-senior" : "12"})
    

# display(roster_clean.head())
print(roster_clean.head())
print("\nSchools:")
print(roster_clean["school"].value_counts())
print("\nGrades:")
print(roster_clean["grade"].value_counts())

# Run it
check_task1(roster_clean, roster)