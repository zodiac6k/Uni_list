import streamlit as st
import pandas as pd
from scraper import get_qs_top100

@st.cache_data(ttl=3600)
def load_data():
    return get_qs_top100()

def main():
    st.title("🌎 Top Undergraduate Universities (QS 2025)")
    st.write("Based on QS World University Rankings for UK, Australia, and Canada")

    df = load_data()

    if df.empty or "Country" not in df.columns:
        st.error("⚠️ No data found. Please check scraper or site structure.")
        return

    countries = ["All"] + sorted(df["Country"].unique())
    country = st.selectbox("Filter by Country", countries)
    if country != "All":
        df = df[df["Country"] == country]

    uni_search = st.text_input("Search University")
    if uni_search:
        df = df[df["University"].str.contains(uni_search, case=False)]

    st.write(f"Showing {len(df)} universities")
    st.dataframe(df.reset_index(drop=True))

    st.download_button("Download CSV", df.to_csv(index=False), "top_ug_unis.csv", "text/csv")

if __name__ == "__main__":
    main()
