import streamlit as st
from scraper import get_all
import pandas as pd

@st.cache_data(ttl=3600)
def load_data():
    return get_all()

def main():
    st.title("🎓 Top UG Universities — UK, Canada & Australia (Wikipedia Data)")
    df = load_data()
    if df.empty:
        st.error("⚠️ No data found — scraper failed or Wikipedia structure changed.")
        return

    country = st.selectbox("Filter by country", ["All"] + df["Country"].unique().tolist())
    df = df if country == "All" else df[df["Country"] == country]

    st.write(f"Showing {len(df)} universities")
    st.dataframe(df)

    st.download_button("Download CSV", df.to_csv(index=False), "university_rankings.csv", "text/csv")

if __name__ == "__main__":
    main()
