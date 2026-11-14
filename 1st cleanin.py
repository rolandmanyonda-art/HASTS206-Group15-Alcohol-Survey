import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("analysis_outputs", exist_ok=True)
df_raw = pd.read_csv("raw-export.csv.csv")
df_raw.columns = [c.strip().replace("\n", " ") for c in df_raw.columns]
print(f"Member 1 loaded raw dataset: {len(df_raw)} rows, {len(df_raw.columns)} columns.")

