import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3, os

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
    

# display(roster_clean.head())
print(roster_clean.head())
print("\nSchools:")
print(roster_clean["school"].value_counts())
print("\nGrades:")
print(roster_clean["grade"].value_counts())

''' 
***** BONEYARD *****

# valid_grades = [K,1,2,3,4,5,6,7,8,9,10,11,12]


# roster_clean = roster.copy()
# roster_clean = roster
# first_name, last_name, school Title

# data = {'col1': [1, 2, 1, 3, 2],
#           'col2': ['A', 'B', 'A', 'C', 'B']}
#   df = pd.DataFrame(data)

# roster_clean["first_name"] = roster_clean["first_name"].replace("first_name", "first_name".upper()) # use Title
# data = roster_clean["student_id"]

# r_map = {""  : 

#         }


roster_clean["first_name"] = roster_clean["first_name"].replace("first_name", "first_name") # dont need to replace
roster_clean["last_name"] = roster_clean["last_name"].replace("last_name", "last_name".upper()) # possible 
# roster_clean["last_name"] = roster_clean["last_name"].replace("last_name", "last_name".upper()) .title().trim()
roster_clean["school"] = roster_clean["school"].replace("school", "school".upper())
roster_clean["last_name"] = roster_clean["last_name"].replace("last_name", "last_name".upper())


# r_map = {"6.0": "6"
#          }


'''