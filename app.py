import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/REPO_NAME/main/data/universities_enriched_streamlit.csv"
    return pd.read_csv(url)

def main():
    st.set_page_config(page_title="Top UG Business Universities", layout="wide")
    st.title("🎓 Top UG Business Universities – UK, Canada, Australia")

    df = load_data()

    # Filters
    country = st.selectbox("🌍 Filter by Country", ["All"] + sorted(df["Country"].unique()))
    if country != "All":
        df = df[df["Country"] == country]

    coop = st.selectbox("🛠️ Co-op Availability", ["All", "Yes", "No"])
    if coop != "All":
        df = df[df["Co-op"] == coop]

    max_fee = st.slider("💰 Max Fees (INR)", min_value=1000000, max_value=3000000, step=100000, value=2500000)
    df = df[df["Fees (INR)"] <= max_fee]

    search = st.text_input("🔎 Search University")
    if search:
        df = df[df["University"].str.contains(search, case=False)]

    st.write(f"Showing {len(df)} universities")
    st.dataframe(df.reset_index(drop=True), use_container_width=True)

    st.download_button("📥 Download CSV", df.to_csv(index=False), "top_ug_universities.csv", "text/csv")

if __name__ == "__main__":
    main()
