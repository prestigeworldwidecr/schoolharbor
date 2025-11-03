# === CHECK: Task 5 (SQL) ===
def _ref_5a():
    rc = pd.read_csv("data/roster.csv", parse_dates=["dob"])
    rc["school"] = rc["school"].str.strip().str.title()
    rc["first_name"] = rc["first_name"].str.strip().str.title()
    rc["last_name"]  = rc["last_name"].str.strip().str.title()
    rc = rc.drop_duplicates(subset=["student_id"])

    asmt = pd.read_csv("data/assessments.csv", parse_dates=["test_date"])
    latest = (asmt.sort_values(["student_id","subject","season","test_date"])
                   .drop_duplicates(["student_id","subject","season"], keep="last"))
    spring = latest.query('season == "Spring"')
    tested = spring.merge(rc[["student_id","school"]], on="student_id", how="left")
    tested_ids = tested.dropna(subset=["school"]).drop_duplicates(["student_id"])
    spring_tested = tested_ids.groupby("school")["student_id"].nunique().rename("spring_tested")
    prof = tested.assign(prof=(tested["perf_level"].isin(["Proficient","Advanced"]).astype(int)))
    prof_ids = prof.groupby(["school","student_id"])["prof"].max().reset_index()
    spring_prof_rate = prof_ids.groupby("school")["prof"].mean().rename("spring_prof_rate")
    return pd.concat([spring_tested, spring_prof_rate], axis=1).fillna(0).reset_index()

def _ref_5b():
    programs = pd.read_csv("data/programs.csv")
    pe = pd.read_csv("data/program_enrollments.csv")
    enrollees = pe.groupby(["school","program"])["student_id"].nunique().rename("enrollees").reset_index()
    ref = enrollees.merge(programs, on=["school","program"], how="right")
    ref["enrollees"] = ref["enrollees"].fillna(0).astype(int)
    ref["fill_rate"] = (ref["enrollees"]/ref["seats"]).clip(upper=1.0)
    return ref[["school","program","enrollees","seats","fill_rate"]].sort_values(["school","program"]).reset_index(drop=True)

def check_task5(df_5a: pd.DataFrame, df_5b: pd.DataFrame):
    passed, tips = True, []

    # 5a
    if df_5a is None or df_5a.empty:
        passed = False; tips.append("5a returned no rows (set sql_5a and run).")
    else:
        ref_a = _ref_5a().sort_values("school").reset_index(drop=True)
        cand_a = df_5a.copy().sort_values("school").reset_index(drop=True)
        need_a = {"school","spring_tested","spring_prof_rate"}
        if not need_a.issubset(cand_a.columns):
            passed = False; tips.append("5a missing required columns.")
        else:
            m = cand_a.merge(ref_a, on="school", suffixes=("_cand","_ref"), how="outer")
            if m.isna().any().any():
                passed = False; tips.append("5a coverage mismatch (NaNs after join).")
            else:
                if (m["spring_tested_cand"] != m["spring_tested_ref"]).any():
                    passed = False; tips.append("5a spring_tested differs from expected.")
                if (m["spring_prof_rate_cand"] - m["spring_prof_rate_ref"]).abs().gt(1e-3).any():
                    passed = False; tips.append("5a spring_prof_rate differs beyond tolerance (1e-3).")

    # 5b
    if df_5b is None or df_5b.empty:
        passed = False; tips.append("5b returned no rows (set sql_5b and run).")
    else:
        ref_b = _ref_5b()
        cand_b = df_5b.copy()
        need_b = {"school","program","enrollees","seats","fill_rate"}
        if not need_b.issubset(cand_b.columns):
            passed = False; tips.append("5b missing required columns.")
        else:
            m = cand_b.merge(ref_b, on=["school","program"], suffixes=("_cand","_ref"), how="outer")
            if m.isna().any().any():
                passed = False; tips.append("5b coverage mismatch (NaNs after join).")
            else:
                if (m["enrollees_cand"] != m["enrollees_ref"]).any() or (m["seats_cand"] != m["seats_ref"]).any():
                    passed = False; tips.append("5b enrollees or seats differ from expected.")
                if (m["fill_rate_cand"] - m["fill_rate_ref"]).abs().gt(1e-3).any():
                    passed = False; tips.append("5b fill_rate differs beyond tolerance (1e-3).")

    print_result(passed, "Task 5 — SQL Companion", tips)

try:
    check_task5(df_5a, df_5b)
except NameError:
    print_result(False, "Task 5 — SQL Companion", ["Run the SQL helper cell first."])