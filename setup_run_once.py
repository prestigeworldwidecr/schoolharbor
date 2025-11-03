import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3, os

np.random.seed(42)

schools = ["Altura", "Mosley", "Riverview", "Sunset", "Pinecrest"]
grades = ["K","1","2","3","4","5",6.0,"7","8","9","10","11","hs-senior"]

n_students = 800
start_id = 200000

def rand_name() :
# {
    first = np.random.choice(["Ava","Liam","Mia","Noah","Emma","Olivia","Sophia","Elijah","Lucas","Isabella","Mateo","Amelia","James","Benjamin","Charlotte"])
    last = np.random.choice(["Smith","Johnson","Brown","Garcia","Martinez","Davis","Lopez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin"])

    return first, last
# }

rows = []

for i in range(n_students) :
# {
    sid = start_id + i
    first, last = rand_name()
    school = np.random.choice(schools, p=[0.18,0.17,0.22,0.21,0.22])

    # FIX: probabilities must match len(grades)=13 and sum to 1.0
    grade = np.random.choice(grades, p=[0.06,0.06,0.06,0.06,0.06,0.06,0.08,0.08,0.08,0.10,0.10,0.10,0.10])
    frl = np.random.choice(["Free/Reduced","Paid","Unknown"], p=[0.55,0.38,0.07])
    ell = np.random.choice([0,1], p=[0.8,0.2])
    sped = np.random.choice([0,1], p=[0.86,0.14])
    dob = pd.Timestamp("2007-09-01") + pd.to_timedelta(np.random.randint(0, 365*12), unit="D")
    rows.append([sid, first, last, school, grade, frl, ell, sped, dob])
# }

roster = pd.DataFrame(rows, columns=["student_id","first_name","last_name","school","grade","frl_status","ell_flag","sped_flag","dob"])
# Quality issues
roster.loc[::31, "school"] = roster.loc[::31, "school"].str.lower()
roster.loc[::47, "last_name"] = roster.loc[::47, "last_name"] + " "
dupe = roster.sample(1, random_state=1).copy()
roster = pd.concat([roster, dupe], ignore_index=True)

# Attendance
calendar_days = pd.date_range("2024-09-01","2025-05-31", freq='B')
att_rows = []

for sid in roster.student_id.sample(frac=0.8, random_state=4) :
# {    
    p_present = np.random.uniform(0.9, 0.98)
    presents = np.random.choice([1,0], size=len(calendar_days), p=[p_present, 1-p_present])

    for day, prs in zip(calendar_days, presents) :
    # {
        if (np.random.rand() < 0.01) :
        # {
            mark = None
        # }

        else :
        # {
            mark = prs
        # }

        att_rows.append([sid, day, mark])
    # }

# }

attendance = pd.DataFrame(att_rows, columns=["student_id","date","present"])

# Assessments
subjects = ["ELA","Math"]
asm_rows = []

for sid in roster.student_id.sample(frac=0.9, random_state=5) :
# {
    for subj in subjects :
    # {
        for season, date in [("Fall","2024-10-15"), ("Spring","2025-04-20")] :
        # {
            score = np.random.normal(700 if subj=="ELA" else 720, 55)
            level = pd.cut([score], bins=[0,650,700,750,1000], labels=["Below","Approaching","Proficient","Advanced"])[0]
            asm_rows.append([sid, subj, season, pd.Timestamp(date) + pd.Timedelta(days=np.random.randint(-7,7)), float(f"{score:.1f}"), str(level)])
assessments = pd.DataFrame(asm_rows, columns=["student_id","subject","season","test_date","scale_score","perf_level"])
        # }

    # }

# }

dup_idx = np.random.choice(assessments.index, size=max(200, len(assessments)//10), replace=False)
dups = assessments.loc[dup_idx].copy()
# push duplicates forward in time so the "latest" is different from the original
dups["test_date"] = dups["test_date"] + pd.to_timedelta(np.random.randint(1, 10, size=len(dups)), unit="D")
# tiny score jitter to make rows visibly different
dups["scale_score"] = dups["scale_score"] + np.random.normal(0, 5, size=len(dups))
assessments = pd.concat([assessments, dups], ignore_index=True)

# Programs
prog_rows = []

for s in schools:

    for prog in ["After School", "STEM Club", "Reading Lab"]:

        seats = np.random.randint(25, 90)
        prog_rows.append([s, prog, seats])
programs = pd.DataFrame(prog_rows, columns=["school","program","seats"])

prog_enr = []
for sid in roster.student_id.sample(frac=0.55, random_state=6):

    s = np.random.choice(schools)
    prog = np.random.choice(["After School", "STEM Club", "Reading Lab"], p=[0.5,0.3,0.2])
    prog_enr.append([sid, s, prog])
program_enrollments = pd.DataFrame(prog_enr, columns=["student_id","school","program"])

# Save CSVs
os.makedirs("data", exist_ok=True)
roster.to_csv("data/roster.csv", index=False)
attendance.to_csv("data/attendance.csv", index=False)
assessments.to_csv("data/assessments.csv", index=False)
programs.to_csv("data/programs.csv", index=False)
program_enrollments.to_csv("data/program_enrollments.csv", index=False)
print("Saved CSVs to ./data")

# Create a SQLite DB for the SQL companion
conn = sqlite3.connect("schoolharbor.db")
roster.to_sql("roster", conn, if_exists="replace", index=False)
attendance.assign(date=lambda d: d["date"].astype(str)).to_sql("attendance", conn, if_exists="replace", index=False)
assessments.assign(test_date=lambda d: d["test_date"].astype(str)).to_sql("assessments", conn, if_exists="replace", index=False)
programs.to_sql("programs", conn, if_exists="replace", index=False)
program_enrollments.to_sql("program_enrollments", conn, if_exists="replace", index=False)
conn.commit()
conn.close()
print("SQLite database created: schoolharbor.db (tables: roster, attendance, assessments, programs, program_enrollments)")

# === Grading Utilities ===
import pandas as pd

GREEN = "\x1b[92m"; RED = "\x1b[91m"; RESET = "\x1b[0m"
def _ok(msg) :  
# {
    print(GREEN, '✓', msg, RESET)
# }

def _err(msg) : 
# {
    print(RED, '✗', msg, RESET)
# }

def print_result(passed: bool, header: str, tips=None) :
# {
    tips = tips or []
    bar = "=" * 60

    print(bar)
    print(header)
    print(bar)

    if (passed) : 
    # {
        _ok("PASS")
    # }

    else : 
    # {
        _err("TRY AGAIN")
    # }

    for t in tips :
    # {        
        print("-", t)
    # }
    
    print(bar)
# }