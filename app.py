import streamlit as st
import pandas as pd
from pathlib import Path

# Page config
st.set_page_config(page_title="UniChamp - University Finder", layout="wide")
st.title("🎓 UniChamp - Top Universities & Courses")
st.markdown("Find top universities, explore finance/analytics programs, and get weekly preparation tips.")

# Load university data
DATA_PATH = Path("data/university_data_sample.csv")
if not DATA_PATH.exists():
    st.error("University data file not found. Please upload the CSV to the 'data' folder.")
    st.stop()

# Load CSV and sanitize
df = pd.read_csv(DATA_PATH)
if 'university_name' not in df.columns:
    st.error("The CSV must contain a 'university_name' column.")
    st.stop()

# Add default rank if missing
df.insert(1, 'rank', range(1, len(df) + 1)) if 'rank' not in df.columns else None

df = df.dropna(subset=["university_name"])  # ensure data consistency

# Filters
st.sidebar.header("🔍 Filter Options")
top_n = st.sidebar.slider("Show Top N Universities", min_value=10, max_value=100, value=50, step=10)
country_filter = st.sidebar.multiselect("Filter by Country", options=sorted(df["country"].dropna().unique()), default=sorted(df["country"].dropna().unique()))

# Apply filters
df_filtered = df[df["country"].isin(country_filter)].nsmallest(top_n, "rank")

# Load contacts if available
CONTACTS_PATH = Path("data/university_contacts.csv")
contacts_df = pd.read_csv(CONTACTS_PATH) if CONTACTS_PATH.exists() else pd.DataFrame()

# Display universities
for _, row in df_filtered.iterrows():
    st.markdown(f"### 🎓 {row['university_name']} (Rank #{row['rank']})")
    st.write(f"📍 Country: {row['country']}")
    if 'website' in row and pd.notna(row['website']):
        st.write(f"🌐 Website: [{row['website']}]({row['website']})")

    if 'sample_courses' in row and pd.notna(row['sample_courses']):
        st.markdown("**📘 Courses in Finance/Analytics:**")
        st.markdown(row["sample_courses"], unsafe_allow_html=True)

    # Show contact details if available
    if not contacts_df.empty:
        contact = contacts_df[contacts_df["university_name"] == row["university_name"]]
        if not contact.empty:
            st.markdown("**📞 Counselor Contact:**")
            for _, info in contact.iterrows():
                st.markdown(f"- **{info['counselor_name']}**: {info['email']} | {info['phone']}")

    st.markdown("---")

# Weekly tips section
st.subheader("📝 Weekly Preparation Tips")
st.markdown("""
- Review university admission deadlines.
- Prepare SOPs and recommendation letters early.
- Focus on IELTS/TOEFL/GRE/GMAT practice weekly.
- Explore finance and data analytics MOOCs (Coursera, edX).
- Reach out to university counselors in August for Fall 2026 intake.
- Track your shortlisting progress in Excel or Notion.
""")
