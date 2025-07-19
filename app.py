import streamlit as st
import pandas as pd
import datetime

# Page settings
st.set_page_config(page_title="Unichamp - Top Universities", layout="wide")
st.title("🎓 Unichamp - Explore Top Universities for Finance & Analytics")

# Load data
@st.cache_data
def load_data():
    df_universities = pd.read_csv("data/university_data_sample.csv")
    df_courses = pd.read_csv("data/finance_courses.csv")
    return df_universities, df_courses

df_universities, df_courses = load_data()

# Rank calculation
df_universities = df_universities.sort_values("score", ascending=False).reset_index(drop=True)
df_universities["rank"] = df_universities.index + 1

# Sidebar Filters
st.sidebar.header("🔍 Filters")
top_n = st.sidebar.slider("Show Top N Universities", 10, 50, 25)
countries = df_universities["country"].unique()
selected_countries = st.sidebar.multiselect("Filter by Country", options=sorted(countries), default=sorted(countries))
sort_by = st.sidebar.selectbox("Sort By", ["rank", "score", "teaching", "research", "citations", "income"])

# Filter DataFrame
df_filtered = df_universities[df_universities["country"].isin(selected_countries)]
df_filtered = df_filtered[df_filtered["rank"] <= top_n]
df_filtered = df_filtered.sort_values(by=sort_by, ascending=(sort_by == "rank"))

# Weekly Prep Tip
prep_tips = [
    "Start preparing for IELTS early.",
    "Build your resume with internships and online courses.",
    "Research visa options for each country.",
    "Reach out to alumni via LinkedIn.",
    "Mark application deadlines in your calendar."
]
week = datetime.date.today().isocalendar()[1]
st.sidebar.header("📅 Weekly Prep Tip")
st.sidebar.info(prep_tips[week % len(prep_tips)])

# Display Summary Table
st.markdown(f"### 📊 Showing Top {top_n} Universities (Sorted by **{sort_by}**)")
st.dataframe(df_filtered[["rank", "university_name", "country", "score", "teaching", "research", "citations", "income"]], use_container_width=True)

# Per-university display with course table
for _, row in df_filtered.iterrows():
    st.markdown(f"---\n### 🎓 {row['university_name']} (Rank #{row['rank']})")
    st.markdown
