import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create output folder for all 10 analysis files
out_dir = "analysis_outputs"
os.makedirs(out_dir, exist_ok=True)

# Load your cleaned dataset
df = pd.read_csv("clean_case_level.csv")

# ==============================================================================
# 1. GENERATE THE 4 CSV SUMMARY TABLES
# ==============================================================================
# 1a) category_counts.csv
cat_rows = list()
for col in list(("sex", "record_source", "drank_30d", "binge_days")):
    vc = df[col].fillna("Missing").value_counts()
    for val, cnt in vc.items():
        cat_rows.append({"Variable": col, "Category": val, "Count": int(cnt), "Pct": round(cnt / len(df) * 100, 2)})
category_counts_df = pd.DataFrame(cat_rows)
category_counts_df.to_csv(os.path.join(out_dir, "category_counts.csv"), index=False)

# 1b) drinking_by_sex.csv
drinking_by_sex = df.groupby("sex").agg(
    Total_Adults=("case_id", "count"),
    Drinkers=("ind1_drinker", "sum"),
    Prevalence_Pct=("ind1_drinker", lambda s: round(s.mean() * 100, 2))
).reset_index()
drinking_by_sex.to_csv(os.path.join(out_dir, "drinking_by_sex.csv"), index=False)

# 1c) drinking_by_source.csv
drinking_by_source = df.groupby("record_source").agg(
    Total_Adults=("case_id", "count"),
    Drinkers=("ind1_drinker", "sum"),
    Prevalence_Pct=("ind1_drinker", lambda s: round(s.mean() * 100, 2))
).reset_index()
drinking_by_source.to_csv(os.path.join(out_dir, "drinking_by_source.csv"), index=False)

# 1d) heavy_drinking_by_source.csv (among eligible current drinkers)
drinkers_only = df[df["elig_ind2"] == True]
heavy_by_source = drinkers_only.groupby("record_source").agg(
    Eligible_Drinkers=("case_id", "count"),
    Frequent_Binge_Count=("ind2_frequent_binge", "sum"),
    Frequent_Binge_Pct=("ind2_frequent_binge", lambda s: round(s.mean() * 100, 2))
).reset_index()
heavy_by_source.to_csv(os.path.join(out_dir, "heavy_drinking_by_source.csv"), index=False)

# ==============================================================================
# 2. GENERATE THE 5 PNG CHARTS
# ==============================================================================
# 2a) age_distribution.png
plt.figure(figsize=(7, 4.5))
for sex_label, color in list((("Male", "#2b5c8f"), ("Female", "#d95f02"))):
    subset = df[df["sex"] == sex_label]["age"].dropna()
    plt.hist(subset, bins=6, alpha=0.65, label=sex_label, color=color, edgecolor="black")
plt.title("Age Distribution of Valid Respondents by Sex")
plt.xlabel("Age (Years)")
plt.ylabel("Number of Respondents")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "age_distribution.png"), dpi=150)
plt.close()

# 2b) alcohol_last_30_days.png
plt.figure(figsize=(7, 4.5))
ct_drink = pd.crosstab(df["sex"], df["drank_30d"])
ct_drink.plot(kind="bar", color=list(("#d95f02", "#2b5c8f")), edgecolor="black", ax=plt.gca())
plt.title("Past 30-Day Alcohol Consumption by Sex")
plt.xlabel("Sex (Reporting Domain)")
plt.ylabel("Number of Respondents")
plt.xticks(rotation=0)
plt.legend(title="Drank in Last 30 Days")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "alcohol_last_30_days.png"), dpi=150)
plt.close()

# 2c) alcohol_types.png (split multi-select answers among drinkers)
valid_types = df[df["elig_ind3"] == True]["alcohol_types"].dropna()
type_series = valid_types.str.split(",").explode().str.strip()
type_counts = type_series.value_counts()

plt.figure(figsize=(8, 4.5))
type_counts.plot(kind="bar", color="#1b9e77", edgecolor="black")
plt.title("Alcoholic Beverage Types Consumed (Past 30 Days)")
plt.xlabel("Beverage Category")
plt.ylabel("Mentions Among Eligible Drinkers")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "alcohol_types.png"), dpi=150)
plt.close()

# 2d) heavy_drinking_days.png
valid_binge_df = df[df["drank_30d"] == "Yes"]
binge_counts = valid_binge_df["binge_days"].value_counts()

plt.figure(figsize=(7.5, 4.5))
binge_counts.plot(kind="bar", color="#7570b3", edgecolor="black")
plt.title("Frequency of Heavy Drinking (6+ Drinks) Among Current Drinkers")
plt.xlabel("Days in Past 30 Days")
plt.ylabel("Number of Current Drinkers")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "heavy_drinking_days.png"), dpi=150)
plt.close()

# 2e) records_by_source.png
source_sex = pd.crosstab(df["record_source"], df["sex"])
plt.figure(figsize=(7, 4.5))
source_sex.plot(kind="bar", stacked=True, color=list(("#e7298a", "#2b5c8f")), edgecolor="black", ax=plt.gca())
plt.title("Valid Pilot Records by Source Type and Sex")
plt.xlabel("Record Source")
plt.ylabel("Number of Valid Records")
plt.xticks(rotation=15, ha="right")
plt.legend(title="Sex")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "records_by_source.png"), dpi=150)
plt.close()

# ==============================================================================
# 3. GENERATE THE TEXT SUMMARY REPORT (eda_report.txt)
# ==============================================================================
report_lines = list((
    "============================================================",
    "HASTS206 EXPLORATORY DATA ANALYSIS (EDA) SUMMARY REPORT",
    "Topic: Alcohol Consumption Patterns by Sex in Zimbabwe",
    "============================================================\n",
    f"Total Valid Consenting Adults Analyzed: {len(df)}",
    f"Mean Age: {df['age'].mean():.1f} years (Min: {df['age'].min():.0f}, Max: {df['age'].max():.0f})\n",
    "--- 1. DRINKING PREVALENCE BY SEX ---",
    drinking_by_sex.to_string(index=False),
    "\n--- 2. DRINKING PREVALENCE BY SOURCE ---",
    drinking_by_source.to_string(index=False),
    "\n--- 3. FREQUENT BINGE DRINKING BY SOURCE ---",
    heavy_by_source.to_string(index=False),
    "\n--- 4. BEVERAGE MENTIONS AMONG DRINKERS ---",
    type_counts.to_string()
))

with open(os.path.join(out_dir, "eda_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"SUCCESS: All 10 analysis files created inside '{out_dir}/'!")
