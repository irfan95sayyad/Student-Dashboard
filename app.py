import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Title and Header
st.title("📊 Department of Computer Applications - Student Performance Dashboard")
st.markdown("#### Developed by *Irfan Sayyad*, Vignan's University")

# ==============================
# Attendance Section
# ==============================
st.header("📘 Attendance Analysis")

att_file = st.file_uploader("Upload Attendance Excel File", type=["xlsx", "xls"], key="attendance")

if att_file is not None:
    df_att = pd.read_excel(att_file)
    st.write("### Preview of Attendance Data")
    st.dataframe(df_att.head())

    st.markdown("#### Attendance Range Categorization")

    # Get subject columns automatically (excluding first 3 columns)
    sub_cols = df_att.columns[3:]

    attendance_summary = []

    for sub in sub_cols:
        below_60 = df_att[df_att[sub] < 60].shape[0]
        between_60_65 = df_att[(df_att[sub] >= 60) & (df_att[sub] < 65)].shape[0]
        between_65_75 = df_att[(df_att[sub] >= 65) & (df_att[sub] < 75)].shape[0]

        attendance_summary.append({
            "Subject": sub,
            "<60%": below_60,
            "60-65%": between_60_65,
            "65-75%": between_65_75
        })

    df_summary = pd.DataFrame(attendance_summary)
    st.write("### Attendance Summary Table")
    st.dataframe(df_summary)

    # Plot stacked bar chart
    st.write("### Attendance Range Distribution")
    df_summary.plot(x="Subject", kind="bar", stacked=True, figsize=(8, 5))
    plt.title("Attendance Range per Subject")
    plt.xlabel("Subject")
    plt.ylabel("Number of Students")
    st.pyplot(plt)

# ==============================
# Marks Section
# ==============================
st.header("📗 Marks Analysis")

marks_file = st.file_uploader("Upload Marks Excel File", type=["xlsx", "xls"], key="marks")

if marks_file is not None:
    df_marks = pd.read_excel(marks_file)
    st.write("### Preview of Marks Data")
    st.dataframe(df_marks.head())

    st.markdown("#### Learner Categorization per Subject")

    sub_cols = [col for col in df_marks.columns if "total" in col.lower()]

    marks_summary = []

    for sub in sub_cols:
        slow = df_marks[df_marks[sub] < 40].shape[0]
        regular = df_marks[(df_marks[sub] >= 40) & (df_marks[sub] <= 60)].shape[0]
        advanced = df_marks[df_marks[sub] > 60].shape[0]

        marks_summary.append({
            "Subject": sub,
            "Slow Learners (<40)": slow,
            "Regular Learners (40-60)": regular,
            "Advanced Learners (>60)": advanced
        })

    df_marks_summary = pd.DataFrame(marks_summary)
    st.write("### Subject-wise Learner Summary")
    st.dataframe(df_marks_summary)

    # Bar chart for each subject
    st.write("### Learner Distribution Chart")
    df_marks_summary.plot(x="Subject", kind="bar", stacked=True, figsize=(8, 5))
    plt.title("Learner Distribution per Subject")
    plt.xlabel("Subject")
    plt.ylabel("Number of Students")
    st.pyplot(plt)

st.markdown("---")
st.caption("© 2025 Department of Computer Applications, Vignan's University | Developed by Irfan Sayyad")
