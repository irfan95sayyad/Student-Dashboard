import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------- Page Config -----------------
st.set_page_config(page_title="Admin Dashboard", layout="wide")

# ----------------- Custom CSS -----------------
st.markdown(
    """
    <style>
    body {
        background-color: #f2f2f2;
    }
    .section {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True
)

# ----------------- Header -----------------
st.markdown(
    """
    <div style="text-align: center; background-color: #f0f8ff; padding: 25px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
        <h1 style="color: #4b0082; font-family: 'Arial', sans-serif;">📊 Student Dashboard</h1>
        <h3 style="color: #ff4500; font-family: 'Arial', sans-serif;">Developed by Mr. Irfan Sayyad</h3>
        <h4 style="color: #228b22; font-family: 'Arial', sans-serif;">Department of Computer Applications</h4>
    </div>
    """, unsafe_allow_html=True
)

# ----------------- ATTENDANCE -----------------
st.markdown('<div class="section" style="background-color: #e6f7ff;">', unsafe_allow_html=True)
st.header("1️⃣ Attendance Analysis (Below 65%)")
attendance_file = st.file_uploader("Upload Attendance Excel", type=["xlsx"], key="att")

if attendance_file:
    df_att = pd.read_excel(attendance_file)
    subjects = df_att.columns[3:]  # assuming first 3 columns are S.No, REGD.NO, NAME

    # -------- Preprocess attendance --------
    def preprocess_att(x):
        if pd.isna(x):
            return 0
        if x <= 1:  # handle decimals like 0.75
            x = x * 100
        return int(x)

    df_att[subjects] = df_att[subjects].applymap(preprocess_att)

    # -------- Subjects below 65% with their percentage --------
    def subjects_below_65_with_percent(row):
        low_subs = [f"{sub} ({row[sub]}%)" for sub in subjects if row[sub] < 65]
        return ', '.join(low_subs)

    df_att['Subjects <65% (with %)'] = df_att.apply(subjects_below_65_with_percent, axis=1)
    df_att['Count <65%'] = df_att['Subjects <65% (with %)'].apply(lambda x: len(x.split(',')) if x else 0)

    # -------- Filter students who have any subject <65% --------
    below_65_df = df_att[df_att['Count <65%'] > 0]

    st.subheader("Students with Attendance Below 65%")
    st.dataframe(
        below_65_df[['REGD.NO', 'NAME', 'Subjects <65% (with %)', 'Count <65%']].style.set_properties(
            **{'background-color': '#e6f2ff', 'color': '#000'}
        )
    )

    # -------- 📊 Bar Chart: Count of students <65% per subject --------
    st.subheader("Subject-wise Count of Students Below 65% Attendance")

    subject_counts = {sub: (df_att[sub] < 65).sum() for sub in subjects}
    subject_df = pd.DataFrame(list(subject_counts.items()), columns=['Subject', 'Students Below 65%'])

    colors = plt.cm.Paired(range(len(subject_df)))

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(subject_df['Subject'], subject_df['Students Below 65%'], color=colors, edgecolor='black')

    # Add count labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.1,
            f'{int(height)}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold',
            color='black'
        )

    ax.set_xlabel('Subjects', fontsize=12)
    ax.set_ylabel('Number of Students (<65%)', fontsize=12)
    ax.set_title('Attendance Below 65% per Subject', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)  # End Attendance section

# ----------------- MARKS -----------------
st.markdown('<div class="section" style="background-color: #fff0f5;">', unsafe_allow_html=True)
st.header("2️⃣ Marks Analysis")
marks_file = st.file_uploader("Upload Marks Excel", type=["xlsx"], key="marks")

if marks_file:
    df_marks = pd.read_excel(marks_file)
    subjects = df_marks.columns[3:]  # assuming first 3 columns are S.No, REGD.NO, NAME

    # -------- Compute totals and averages --------
    df_marks['Total Marks'] = df_marks[subjects].sum(axis=1)
    df_marks['Average %'] = df_marks['Total Marks'] / len(subjects)
    df_marks['Average %'] = df_marks['Average %'].round(2)

    # -------- Categorize students --------
    def categorize(avg):
        if avg > 60:
            return 'Advance Learner'
        elif avg < 40:
            return 'Slow Learner'
        else:
            return 'Regular Learner'

    df_marks['Category'] = df_marks['Average %'].apply(categorize)

    st.subheader("Student Categories based on Average Marks")
    st.dataframe(df_marks[['REGD.NO', 'NAME', 'Total Marks', 'Average %', 'Category']].style.set_properties(
        **{'background-color': '#fff0f5', 'color': '#000'}
    ))

    # -------- Pie chart --------
    category_counts = df_marks['Category'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    colors_marks = ['#66b3ff', '#ff9999', '#99ff99']
    ax2.pie(
        category_counts,
        labels=category_counts.index,
        autopct=lambda p: f'{p:.1f}% ({int(p*sum(category_counts)/100)})',
        startangle=90,
        colors=colors_marks,
        wedgeprops={'edgecolor': 'black'}
    )
    ax2.set_title("Student Category Distribution", fontsize=14, fontweight='bold')
    st.pyplot(fig2)

st.markdown('</div>', unsafe_allow_html=True)
