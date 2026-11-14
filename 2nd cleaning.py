rename_dict = {}
for col in df_raw.columns:
    if col.startswith("Timestamp"):
        rename_dict[col] = "timestamp"
    elif col.startswith("Do you agree to take part"):
        rename_dict[col] = "consent"
    elif col.startswith("Case ID"):
        rename_dict[col] = "case_id"
    elif col.startswith("Source of this record"):
        rename_dict[col] = "record_source"
    elif col.startswith("What is your sex"):
        rename_dict[col] = "sex"
    elif col.startswith("Age in years"):
        rename_dict[col] = "age"
    elif col.startswith("In the last 30 days, did you drink"):
        rename_dict[col] = "drank_30d"
    elif col.startswith("Which kinds of alcohol"):
        rename_dict[col] = "alcohol_types"
    elif col.startswith("In the last 30 days, on how many days"):
        rename_dict[col] = "binge_days"
    elif col.startswith("Do you drink alcohol"):
        rename_dict[col] = "ever_drink_dup"
    elif col.startswith("Are you above 18"):
        rename_dict[col] = "above_18"

df = df_raw.rename(columns=rename_dict).copy()

for c in ["consent", "case_id", "record_source", "sex", "drank_30d", "alcohol_types", "binge_days", "above_18"]:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip().replace({"nan": np.nan, "": np.nan})
print("Member 2 standardized column names and whitespace.")
