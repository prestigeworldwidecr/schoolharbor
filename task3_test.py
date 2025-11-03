# === CHECK: Task 3 — School Test & Proficiency Rates ===

def _norm_school(s):
    return (s.astype("string")
             .str.strip()
             .str.replace(r"\s+", " ", regex=True)
             .str.title())

def check_task3_v2(school_rates: pd.DataFrame, roster_clean: pd.DataFrame, spring_latest: pd.DataFrame, tol=1e-3):
    tips = []
    # 0) Basic column presence
    need = {"school", "spring_test_rate", "spring_prof_rate"}
    if not need.issubset(school_rates.columns):
        missing = sorted(need - set(school_rates.columns))
        return print_result(False, "Task 3 — School Test & Proficiency Rates", [f"Missing columns: {missing}"])

    # 1) Build the reference exactly (then normalize school labels)
    tested = spring_latest.merge(roster_clean[["student_id","school"]], on="student_id", how="left")
    tested_ids = tested.dropna(subset=["school"]).drop_duplicates(["student_id"])

    roster_n = (roster_clean.groupby("school", dropna=False)["student_id"]
                          .nunique().rename("roster_n"))
    tested_n = (tested_ids.groupby("school", dropna=False)["student_id"]
                          .nunique().rename("tested_n"))

    prof = tested.assign(prof=(tested["perf_level"].isin(["Proficient","Advanced"]).astype(int)))
    prof_ids = prof.groupby(["school","student_id"], dropna=False)["prof"].max().reset_index()
    prof_rate = prof_ids.groupby("school", dropna=False)["prof"].mean().rename("spring_prof_rate")

    ref = (pd.concat([roster_n, tested_n], axis=1)
             .fillna({"tested_n": 0})
             .assign(spring_test_rate=lambda d: d["tested_n"]/d["roster_n"])
             .drop(columns=["roster_n","tested_n"])
             .join(prof_rate, how="left")
             .fillna({"spring_prof_rate": 0})
             .reset_index())

    # Normalize school names on BOTH sides
    ref["school"] = _norm_school(ref["school"])
    cand = school_rates.copy()
    cand["school"] = _norm_school(cand["school"])

    # 2) Coverage diagnostics (don’t rely on outer-join NaN; show exact diffs)
    ref_set  = set(ref["school"])
    cand_set = set(cand["school"])
    missing = sorted(ref_set - cand_set)
    extra   = sorted(cand_set - ref_set)
    if missing:
        tips.append(f"Missing schools in candidate: {missing}")
    if extra:
        tips.append(f"Unexpected schools in candidate: {extra}")

    # If there are coverage issues, still continue to provide numeric diffs for the overlap
    overlap = sorted(ref_set & cand_set)
    ref_o = ref[ref["school"].isin(overlap)].sort_values("school").reset_index(drop=True)
    cand_o = cand[cand["school"].isin(overlap)].sort_values("school").reset_index(drop=True)

    # Ensure dtype is numeric for comparison
    for col in ["spring_test_rate","spring_prof_rate"]:
        ref_o[col]  = pd.to_numeric(ref_o[col], errors="coerce")
        cand_o[col] = pd.to_numeric(cand_o[col], errors="coerce")

    # 3) Numeric comparisons
    merged = cand_o.merge(ref_o, on="school", suffixes=("_cand","_ref"), how="inner")
    bad_rows = []
    for col in ["spring_test_rate","spring_prof_rate"]:
        diff = (merged[f"{col}_cand"] - merged[f"{col}_ref"]).abs()
        bad_mask = diff > tol
        if bad_mask.any():
            # Keep a few examples to help the candidate see what's off
            sample = merged.loc[bad_mask, ["school", f"{col}_cand", f"{col}_ref"]].head(5)
            bad_rows.append((col, sample))

    passed = (not missing) and (not extra) and (len(bad_rows) == 0)
    if bad_rows:
        for col, sample in bad_rows:
            tips.append(f"{col} differs beyond tol={tol}. Examples:\n{sample.to_string(index=False)}")

    print_result(passed, "Task 3 — School Test & Proficiency Rates", tips)

# Run checker
check_task3_v2(school_rates, roster_clean, spring_latest, tol=1e-3)