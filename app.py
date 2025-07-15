import streamlit as st
import pandas as pd
from scraper import get_universities_from_wikipedia

@st.cache_data(ttl=3600)
def load_data():
    return get_universities_from_wikipedia()

def main():
    st.set_page_config(page_title="Top UG Universities", layout="wide")
    st.title("🎓 Top UG Universities – UK, Canada & Australia (Wikipedia)")
    df = load_data()

    if df.empty:
        st.error("⚠️ No university data available.")
        return

    countries = ["All"] + sorted(df["Country"].unique())
    country = st.selectbox("Filter by Country", countries)
    if country != "All":
        df = df[df["Country"] == country]

    search = st.text_input("Search University")
    if search:
        df = df[df["University"].str.contains(search, case=False)]

    st.dataframe(df.reset_index(drop=True), use_container_width=True)
    st.download_button("Download CSV", df.to_csv(index=False), "ug_universities_wikipedia.csv", "text/csv")

if __name__ == "__main__":
    main()
