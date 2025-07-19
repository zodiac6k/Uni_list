import pandas as pd

data = {
    "university_name": [
        "University of Oxford", "Harvard University", "University of Toronto"
    ],
    "country": ["UK", "USA", "Canada"],
    "score": [95.6, 94.8, 91.2],
    "teaching": [90.3, 91.7, 87.1],
    "research": [92.5, 93.0, 90.2],
    "citations": [98.1, 96.8, 94.6],
    "income": [85.2, 82.1, 78.5],
    "IELTS_required": [6.5, 7.0, 6.5],
    "program_major": ["Business Analytics", "Finance", "Data Science"],
    "years_of_study": [3, 4, 4],
    "coop_available": ["Yes", "No", "Yes"],
    "post_study_visa": ["Yes", "Yes", "Yes"]
}

df = pd.DataFrame(data)
df.to_csv("university_data.csv", index=False)
