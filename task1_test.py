# === CHECK: Task 1 — Roster Cleaning ===
def check_task1(roster_clean: pd.DataFrame, roster_raw: pd.DataFrame):
    passed, tips = True, []
    req_cols = {"student_id","first_name","last_name","school","grade"}
    if not req_cols.issubset(roster_clean.columns):
        return print_result(False, "Task 1 — Roster Cleaning",
                            [f"Missing: {sorted(req_cols - set(roster_clean.columns))}"])

    # 1. Check stripping + Title Case for string columns
    for col in ["first_name","last_name","school"]:
        norm = roster_clean[col].fillna("").astype(str).str.strip().str.title()
        if not roster_clean[col].fillna("").equals(norm):
            passed = False
            tips.append(f"Column '{col}' not fully stripped+title-cased.")

    # 2. Ensure no duplicate student_id
    if roster_clean["student_id"].duplicated().any():
        passed = False
        tips.append("Duplicate student_id values remain—dedup by student_id.")

    # 3. Grade must be string dtype and valid
    if not pd.api.types.is_string_dtype(roster_clean["grade"]):
        passed = False
        tips.append("Column 'grade' is not string dtype. Cast it with astype(str).")

    valid = set(["K"] + [str(i) for i in range(1,13)])
    bad_vals = set(roster_clean["grade"].unique()) - valid
    if bad_vals:
        passed = False
        tips.append(f"Invalid grade values found: {sorted(bad_vals)}")

    print_result(passed, "Task 1 — Roster Cleaning", tips)

# Run it
check_task1(roster_clean, roster)