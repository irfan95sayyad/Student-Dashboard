import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Page Setup
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Custom CSS Styling
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
        color: #111827;
    }
    .stApp {
        background-color: #f5f7fa;
    }
    .main-header {
        color: #ffffff;
        background: linear-gradient(to right, #141E30, #243B55);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    .section-header {
        color: #1e3a8a;
        font-size: 22px;
        font-weight: 700;
        margin-top: 20px;
        border-left: 6px solid #2563eb;
        padding-left: 10px;
    }
    .css-18e3th9 {
        padding: 2rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown('<div class="main-header">📊 Department of Computer Applications - Student Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header">👨‍🏫 Developed by Irfan Sayyad, Vignan’s University</div>', unsafe_allow_html=True)


# Seaborn style for colorful charts
sns.set_style("whitegrid")
sns.set_palette("viridis")

# ==============================
# 📘 Attendance Analysis Section
# ==============================
st.markdown('<div class="section-header">📘 Attendance Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📂 Upload Attendance Excel File</div>', unsafe_allow_html=True)
att_file = st.file_uploader("Upload Attendance Excel File", type=["xlsx", "xls"], key="attendance")

if att_file is not None:
    df_att = pd.read_excel(att_file)
    st.write("### 🧾 Attendance Data Preview")
    st.dataframe(df_att.head(), use_container_width=True)

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

    st.success("✅ Attendance Summary Generated Successfully!")
    st.write("### 📋 Attendance Summary Table")
    st.dataframe(df_summary.style.background_gradient(cmap="YlOrBr"), use_container_width=True)

    st.write("### 📊 Attendance Range Distribution")
    plt.figure(figsize=(8, 5))
    df_summary.set_index("Subject")[["<60%", "60-65%", "65-75%"]].plot(
        kind="bar", stacked=True, figsize=(8, 5), colormap="plasma", edgecolor='black'
    )
    plt.title("Attendance Range per Subject", fontsize=14, fontweight="bold", color="#1e293b")
    plt.xlabel("Subjects")
    plt.ylabel("No. of Students")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# ==============================
# 📗 Marks Analysis Section
# ==============================
st.markdown('<div class="section-header">📗 Marks Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📗 Upload Marks Excel File</div>', unsafe_allow_html=True)
marks_file = st.file_uploader("Upload Marks Excel File", type=["xlsx", "xls"], key="marks")

if marks_file is not None:
    df_marks = pd.read_excel(marks_file)
    st.write("### 🧾 Marks Data Preview")
    st.dataframe(df_marks.head(), use_container_width=True)

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

    st.success("✅ Marks Summary Generated Successfully!")
    st.write("### 📋 Subject-wise Learner Summary")
    st.dataframe(df_marks_summary.style.background_gradient(cmap="YlGnBu"), use_container_width=True)

    st.write("### 📈 Learner Distribution Chart")
    plt.figure(figsize=(8, 5))
    df_marks_summary.set_index("Subject")[[
        "Slow Learners (<40)", "Regular Learners (40-60)", "Advanced Learners (>60)"
    ]].plot(kind="bar", stacked=True, colormap="cubehelix", edgecolor='black')
    plt.title("Learner Distribution per Subject", fontsize=14, fontweight="bold", color="#1e293b")
    plt.xlabel("Subjects")
    plt.ylabel("Number of Students")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# ==============================
# Footer
# ==============================
st.markdown("---")
st.caption("🌐 © 2025 Department of Computer Applications, Vignan’s University | Developed by Irfan Sayyad")
