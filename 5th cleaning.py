# Check 4: Standardize Labels, Fix Domain Mismatch (S-F-008), & Enforce Skip Logic
df_clean = df3.copy()
df_clean["record_source"] = df_clean["record_source"].replace({"Simulated response": "Simulated Household Response"})

# Align S-F-008 sex to Female to match its assigned Female Case ID prefix
df_clean["sex"] = np.where(df_clean["case_id"].str.contains("-F-"), "Female", "Male")

if "ever_drink_dup" in df_clean.columns:
    df_clean = df_clean.drop(columns=["ever_drink_dup"])

is_drinker = df_clean["drank_30d"].str.lower() == "yes"
for col in ["alcohol_types", "binge_days"]:
    df_clean[col] = np.where(~is_drinker, "Inapplicable", df_clean[col].fillna("Missing"))
    df_clean[col] = df_clean[col].replace({"Prefer not to say": "Refused", "Don't know": "Unknown"})

add_log("4. Skip Logic & Consistency", "Fix S-F-008 sex label; recode non-drinkers to Inapplicable", len(df3), len(df_clean))

quality_log_df = pd.DataFrame(quality_log)
print("=== DATA QUALITY LOG ===")
print(quality_log_df.to_string(index=False))
