assessments = pd.read_csv("data/assessments.csv", parse_dates=["test_date"])

# TODO: deduplicate by latest test_date per (student_id, subject, season)
# TODO: filter to spring only

spring_latest = latest_assessments_spring_only.copy()

dup_keys = spring_latest.duplicated(subset=["student_id","subject"]).sum()
print("Duplicates after latest-per-key (should be 0):", dup_keys)
display(spring_latest.head())