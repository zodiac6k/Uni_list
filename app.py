import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

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

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
top_n = st.sidebar.slider("Show Top N Universities", min_value=10, max_value=100, value=50, step=10)
country_filter = st.sidebar.multiselect("Filter by Country", options=sorted(df["country"].dropna().unique()), default=sorted(df["country"].dropna().unique()))

# Course filter
if 'program_major' in df.columns:
    course_filter = st.sidebar.multiselect("Filter by Course", options=sorted(df['program_major'].dropna().unique()), default=sorted(df['program_major'].dropna().unique()))
    df = df[df['program_major'].isin(course_filter)]

# Additional filters if available
if 'scholarship' in df.columns:
    scholarship_filter = st.sidebar.multiselect("Scholarship Available", options=df['scholarship'].dropna().unique(), default=df['scholarship'].dropna().unique())
    df = df[df['scholarship'].isin(scholarship_filter)]
if 'visa_type' in df.columns:
    visa_filter = st.sidebar.multiselect("Post-Study Visa Type", options=df['visa_type'].dropna().unique(), default=df['visa_type'].dropna().unique())
    df = df[df['visa_type'].isin(visa_filter)]

# University name search
search_term = st.sidebar.text_input("Search University")
if search_term:
    df = df[df["university_name"].str.contains(search_term, case=False, na=False)]

# Apply filters
df_filtered = df[df["country"].isin(country_filter)].nsmallest(top_n, "rank")

# Load contacts if available
CONTACTS_PATH = Path("data/university_contacts.csv")
contacts_df = pd.read_csv(CONTACTS_PATH) if CONTACTS_PATH.exists() else pd.DataFrame()

# Add clickable website column if available
if 'website' in df_filtered.columns:
    df_filtered['website'] = df_filtered['website'].apply(lambda x: f"[Visit Site]({x})" if pd.notna(x) else "")

# Display as interactive table with clickable links
st.subheader("🏫 Filtered University List")
st.dataframe(df_filtered.style.format({"website": lambda x: x}), use_container_width=True, hide_index=True)

# Chart
if not df_filtered.empty:
    chart = px.bar(df_filtered, x="university_name", y=["score", "teaching", "research", "citations"],
                   barmode="group", title="📊 Academic Performance Comparison")
    st.plotly_chart(chart, use_container_width=True)

# Download button
st.download_button("📥 Download Filtered Results", df_filtered.to_csv(index=False), "filtered_universities.csv", "text/csv")

# Contacts section
if not contacts_df.empty:
    st.subheader("📞 University Contacts and Deadlines")
    st.dataframe(contacts_df, use_container_width=True, hide_index=True)
else:
    st.info("No contact information available yet. Please upload to data/university_contacts.csv")

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
