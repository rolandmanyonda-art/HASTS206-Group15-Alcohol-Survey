# Check 2: Validate Case ID pattern & remove duplicate Case IDs (removes duplicate C-M-006)
n1 = len(df1)
pattern = r"^(S-M-00[1-7]|S-F-00[1-8]|C-M-00[1-8]|C-F-00[1-7])$"
df2 = df1[df1["case_id"].str.match(pattern, na=False)].drop_duplicates(subset=["case_id"], keep="first").copy()
add_log("2. Case ID & Duplicates", "Match valid S-/C- pattern and drop duplicate C-M-006 (keep first)", n1, len(df2))

# Check 3: Consent & Age >= 18 Gate (removes non-consenting C-F-007)
n2 = len(df2)
df2["age"] = pd.to_numeric(df2["age"], errors="coerce")
df3 = df2[
    (df2["consent"].str.upper() == "YES") &
    (df2["age"].between(18, 110)) &
    (df2["above_18"].isna() | (df2["above_18"].str.upper() == "YES"))
].copy()
add_log("3. Consent & Age Gate", "Keep Consent=YES and Age 18-110 (removes C-F-007)", n2, len(df3))
print(f"Verified by Martin Simbarasi: duplicates and consent gate checked. {len(df3)} valid adults remaining.")
