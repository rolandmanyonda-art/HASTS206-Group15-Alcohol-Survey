sim_strata = pd.DataFrame({
    "Stratum": list(("Urban (Harare/Bulawayo)", "Rural (Mashonaland/Matabeleland)")),
    "Pop_Adults_N": list((2500000, 5500000)),
    "Sample_n": list((400, 400)),
    "Observed_Drinkers": list((240, 150))
})

sim_strata["Selection_Prob"] = sim_strata["Sample_n"] / sim_strata["Pop_Adults_N"]
sim_strata["Base_Weight"] = 1 / sim_strata["Selection_Prob"]

unweighted = sim_strata["Observed_Drinkers"].sum() / sim_strata["Sample_n"].sum()
weighted = np.sum(sim_strata["Base_Weight"] * sim_strata["Observed_Drinkers"]) / np.sum(sim_strata["Base_Weight"] * sim_strata["Sample_n"])
print(sim_strata.to_string(index=False))
print(f"\nWeighting Demo -> Unweighted: {unweighted:.2%} | Design-Weighted: {weighted:.2%}")
