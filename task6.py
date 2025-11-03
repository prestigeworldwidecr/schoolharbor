def select_latest(df, key_cols, date_col) :
# {
    """Return the latest row per key based on a datetime column.

    Parameters
    ----------
    df : pd.DataFrame
    key_cols : list[str]
    date_col : str

    Returns
    -------
    pd.DataFrame
        Latest row per key in `key_cols` by `date_col`.
    """
    # TODO: implement

    return out.copy()

# }

# Demo:
_assess = pd.read_csv("data/assessments.csv", parse_dates=["test_date"])
_latest = select_latest(_assess, ["student_id","subject","season"], "test_date")
# display(_latest.head())
print(_latest.head())