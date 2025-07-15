import streamlit as st
import pandas as pd
from scraper import get_qs_top100

@st.cache_data(ttl=3600)
def load_data():
    df = get_qs_top100()
    return df

def main():
    st.title("🎓 Top Undergraduate Universities (UG) – UK, Australia & Canada")
    st.write("Data based on QS World University Rankings (Top 100, 2026 edition)")

    df = load_data()

    countries = ["All"] + sorted(df["Country"].unique())
    country = st.selectbox("Filter by Country", countries)
    if country != "All":
        df = df[df["Country"] == country]

    uni_search = st.text_input("Search University")
    if uni_search:
        df = df[df["University"].str.contains(uni_search, case=False)]

    st.write(f"Showing {len(df)} universities")
    st.dataframe(df.reset_index(drop=True))

    if st.button("Download CSV"):
        st.download_button("Download CSV", df.to_csv(index=False), "top_ug_unis.csv", "text/csv")

if __name__ == "__main__":
    main()
