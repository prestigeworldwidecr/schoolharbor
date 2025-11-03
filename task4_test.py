# === CHECK: Task 4 ===
def check_task4(ada_by_school_month: pd.DataFrame, roster_clean: pd.DataFrame, attendance: pd.DataFrame):
    passed, tips = True, []
    req = {"school","year_month","present_days","marked_days","ADA"}
    if not req.issubset(ada_by_school_month.columns):
        return print_result(False, "Task 4 — ADA by School-Month", [f"Missing: {sorted(req - set(ada_by_school_month.columns))}"])

    att = attendance.merge(roster_clean[["student_id","school"]], on="student_id", how="left").dropna(subset=["present"])
    att["year_month"] = att["date"].dt.to_period("M").astype(str)
    ref = (att.groupby(["school","year_month"], dropna=False)["present"]
             .agg(present_days="sum", marked_days="count").reset_index())
    ref["ADA"] = ref["present_days"]/ref["marked_days"]

    m = ada_by_school_month.merge(ref, on=["school","year_month"], suffixes=("_cand","_ref"), how="outer")
    if m.isna().any().any():
        return print_result(False, "Task 4 — ADA by School-Month", ["Coverage mismatch (NaNs after join)."])

    if (m["present_days_cand"] != m["present_days_ref"]).any() or (m["marked_days_cand"] != m["marked_days_ref"]).any():
        passed = False; tips.append("present_days/marked_days counts differ from expected.")

    if (m["ADA_cand"] - m["ADA_ref"]).abs().gt(1e-3).any():
        passed = False; tips.append("ADA differs from expected beyond tolerance (1e-3).")

    print_result(passed, "Task 4 — ADA by School-Month", tips)

attendance_for_check = pd.read_csv("data/attendance.csv", parse_dates=["date"])
check_task4(ada_by_school_month, roster_clean, attendance_for_check)