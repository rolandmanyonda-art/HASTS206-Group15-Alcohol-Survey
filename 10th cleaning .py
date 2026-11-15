df_clean.to_csv("cleaned_data_level.csv", index=False)
benchmark_df.to_csv("benchmark_table.csv", index=False)
print("SUCCESS: cleaned_data_level.csv and benchmark_table.csv exported!")
