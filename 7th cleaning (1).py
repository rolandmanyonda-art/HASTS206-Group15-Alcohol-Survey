import pandas as pd
def calc_metrics(sub_df, label):
    i1 = sub_df["ind1_drinker"].dropna()
    i2 = sub_df["ind2_frequent_binge"].dropna()
    i3 = sub_df["ind3_comm_beer"].dropna()
    return pd.Series({
        "Domain": label,
        "Valid_Adults": len(sub_df),
        "Ind1_Drinkers_Count": int(i1.sum()),
        "Ind1_Denom": int(len(i1)),
        "Ind1_Prevalence_Pct": round(i1.mean() * 100, 2) if len(i1) > 0 else np.nan,
        "Ind2_Binge_Count": int(i2.sum()),
        "Ind2_Binge_Denom": int(len(i2)),
        "Ind2_Binge_Pct": round(i2.mean() * 100, 2) if len(i2) > 0 else np.nan,
        "Ind3_Beer_Count": int(i3.sum()),
        "Ind3_Beer_Denom": int(len(i3)),
        "Ind3_Beer_Pct": round(i3.mean() * 100, 2) if len(i3) > 0 else np.nan
    })

benchmark_df = pd.DataFrame([
    calc_metrics(df_clean, "Overall"),
    calc_metrics(df_clean[df_clean["sex"] == "Male"], "Male"),
    calc_metrics(df_clean[df_clean["sex"] == "Female"], "Female")
])
print("\n=== BENCHMARK TABLE (FOR POWER BI RECONCILIATION) ===")
print(benchmark_df.to_string(index=False))
