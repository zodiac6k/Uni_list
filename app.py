import streamlit as st
import pandas as pd
from scraper import get_qs_top100

@st.cache_data(ttl=3600)
def load_data():
    return get_qs_top100()

def main():
    st.title("🎓 Top UG Universities – UK, Australia & Canada (QS 2025)")
    df = load_data()

    if df.empty or "Country" not in df.columns:
        st.error("⚠️ No data found. QS site may have changed or failed to load.")
        return

    country = st.selectbox("Filter by Country", ["All"] + sorted(df["Country"].unique()))
    if country != "All":
        df = df[df["Country"] == country]

    search = st.text_input("Search University")
    if search:
        df = df[df["University"].str.contains(search, case=False)]

    st.write(f"Showing {len(df)} universities")
    st.dataframe(df.reset_index(drop=True), use_container_width=True)

    st.download_button("Download CSV", df.to_csv(index=False), "top_ug_universities.csv", "text/csv")

if __name__ == "__main__":
    main()
