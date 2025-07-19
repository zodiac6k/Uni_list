import pandas as pd

# Step 1: Load the CSV
file_path = "C:/Py Test/Univ_List/timesData.csv"
df = pd.read_csv(file_path)

# Step 2: Filter for 2022 and target countries
target_countries = ["United Kingdom", "Canada", "Australia"]
df_2022 = df[(df["year"] == 2022) & (df["country"].isin(target_countries))]

# Step 3: Clean rank and sort
df_2022["Rank"] = pd.to_numeric(df_2022["world_rank"].str.replace("=", ""), errors="coerce")
df_2022 = df_2022.dropna(subset=["Rank"]).sort_values("Rank")

# Step 4: Select top 100
df_top100 = df_2022.head(100)

# Step 5: Keep essential columns
df_final = df_top100[[
    "Rank", "university_name", "country", "total_score", "teaching", "research", "citations", "income", "num_students", "international_students"
]]
df_final.columns = [
    "Rank", "University", "Country", "Score", "Teaching", "Research", "Citations", "Income", "No. of Students", "International Students"
]

# Step 6: Save the final CSV
output_path = "C:/Py Test/Univ_List/top100_universities_2022.csv"
df_final.to_csv(output_path, index=False)

print(f"✅ Saved Top 100 universities to: {output_path}")
