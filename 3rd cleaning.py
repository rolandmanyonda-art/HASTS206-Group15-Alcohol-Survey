quality_log = []
def add_log(step, rule, before, after):
    quality_log.append({
        "Check Step": step,
        "Cleaning Rule": rule,
        "Before": before,
        "After": after,
        "Removed": before - after
    })

# Check 1: Remove technical test cases (T-001 to T-005)
n0 = len(df)
df1 = df[~df["case_id"].str.startswith("T-", na=False)].copy()
add_log("1. Technical Test Cases", "Exclude Case IDs starting with 'T-' (T-001 to T-005)", n0, len(df1))
print(f"Member 3 excluded technical test cases: {len(df1)} rows remaining.")
