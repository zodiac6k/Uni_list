import pandas as pd

df = pd.read_csv("C:/Py Test/Univ_List/timesData.csv")
print(df.columns.tolist())
df["rank_numeric"] = pd.to_numeric(df["world_rank"].str.replace("=", ""), errors="coerce")
df["world_rank"]  # or whatever correct name you see

