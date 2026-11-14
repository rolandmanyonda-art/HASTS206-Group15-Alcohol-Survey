df_clean["ind1_drinker"] = np.where(df_clean["drank_30d"] == "Yes", 1,
                           np.where(df_clean["drank_30d"] == "No", 0, np.nan))

valid_binge = (df_clean["drank_30d"] == "Yes") & (~df_clean["binge_days"].isin(["Inapplicable", "Refused", "Unknown", "Missing"]))
df_clean["elig_ind2"] = valid_binge
df_clean["ind2_frequent_binge"] = np.where(~valid_binge, np.nan,
                                  np.where(df_clean["binge_days"].isin(["5-10", "10-20", "20-30"]), 1, 0))

valid_type = (df_clean["drank_30d"] == "Yes") & (~df_clean["alcohol_types"].isin(["Inapplicable", "Refused", "Unknown", "Missing"]))
df_clean["elig_ind3"] = valid_type
df_clean["ind3_comm_beer"] = np.where(~valid_type, np.nan,
                             np.where(df_clean["alcohol_types"].str.contains("Commercial Beer", case=False, na=False), 1, 0))
print("Member 6 created indicator columns and eligibility masks.")
