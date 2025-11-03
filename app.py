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
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True
)

# ----------------- Header -----------------
st.markdown(
    """
    <div style="text-align: center; background-color: #f0f8ff; padding: 25px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
        <h1 style="color: #4b0082;">📊 Student Dashboard</h1>
        <h3 style="color: #ff4500;">Developed by Mr. Irfan Sayyad</h3>
        <h4 style="color: #228b22;">Department of Computer Applications</h4>
    </div>
    """, unsafe_allow_html=True
)

# =========================================================
# 1️⃣ ATTENDANCE ANALYSIS SECTION
# =========================================================
st.markdown('<div class="section" style="background-color: #e6f7ff;">', unsafe_allow_html=True)
st.header("1️⃣ Attendance Analysis (Below 65%)")

attendance_file = st.file_uploader("Upload Attendance Excel", type=["xlsx"], key="att")

if attendance_file:
    df_att = pd.read_excel(attendance_file)
    subjects = df_att.columns[3:]  # assuming first 3 columns are S.No, REGD.NO, NAME

    def preprocess_att(x):
        if pd.isna(x):
            return 0
        if x <= 1:
            x = x * 100
        return int(x)

    df_att[subjects] = df_att[subjects].applymap(preprocess_att)

    def subjects_below_65_with_percent(row):
        low_subs = [f"{sub} ({row[sub]}%)" for sub in subjects if row[sub] < 65]
        return ', '.join(low_subs)

    df_att['Subjects <65% (with %)'] = df_att.apply(subjects_below_65_with_percent, axis=1)
    df_att['Count <65%'] = df_att['Subjects <65% (with %)'].apply(lambda x: len(x.split(',')) if x else 0)
    below_65_df = df_att[df_att['Count <65%'] > 0]

    st.subheader("Students with Attendance Below 65%")
    st.dataframe(
        below_65_df[['REGD.NO', 'NAME', 'Subjects <65% (with %)', 'Count <65%']].style.set_properties(
            **{'background-color': '#e6f2ff', 'color': '#000'}
        ),
        use_container_width=True
    )

    st.subheader("Subject-wise Count of Students Below 65% Attendance")
    subject_counts = {sub: (df_att[sub] < 65).sum() for sub in subjects}
    subject_df = pd.DataFrame(list(subject_counts.items()), columns=['Subject', 'Students Below 65%'])

    colors = plt.cm.Paired(range(len(subject_df)))
    fig, ax = plt.subplots(figsize=(7.5, 4))
    bars = ax.bar(subject_df['Subject'], subject_df['Students Below 65%'], color=colors, edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.2, f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#333333')

    ax.set_xlabel('Subjects', fontsize=11)
    ax.set_ylabel('No. of Students (<65%)', fontsize=11)
    ax.set_title('Attendance Below 65% per Subject', fontsize=13, fontweight='bold')
    plt.xticks(rotation=30, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 2️⃣ MARKS ANALYSIS (MULTIPLE SUBJECTS)
# =========================================================
st.markdown('<div class="section" style="background-color: #fff0f5;">', unsafe_allow_html=True)
st.header("2️⃣ Marks Analysis (Multiple Subjects)")

marks_file = st.file_uploader("Upload Marks Excel (Multiple Subjects)", type=["xlsx"], key="marks")

if marks_file:
    df_marks = pd.read_excel(marks_file)
    subjects = df_marks.columns[3:]  # assuming first 3 columns are S.No, REGD.NO, NAME

    df_marks['Total Marks'] = df_marks[subjects].sum(axis=1)
    df_marks['Average %'] = (df_marks['Total Marks'] / len(subjects)).round(2)

    def categorize(avg):
        if avg > 60:
            return 'Advance Learner'
        elif avg < 40:
            return 'Slow Learner'
        else:
            return 'Regular Learner'

    df_marks['Category'] = df_marks['Average %'].apply(categorize)

    st.subheader("Student Categories based on Average Marks")
    st.dataframe(
        df_marks[['REGD.NO', 'NAME', 'Total Marks', 'Average %', 'Category']].style.set_properties(
            **{'background-color': '#fff0f5', 'color': '#000'}
        ),
        use_container_width=True
    )

    category_counts = df_marks['Category'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    colors_marks = ['#66b3ff', '#ff9999', '#99ff99']
    ax2.pie(category_counts, labels=category_counts.index,
            autopct=lambda p: f'{p:.1f}% ({int(p*sum(category_counts)/100)})',
            startangle=90, colors=colors_marks, wedgeprops={'edgecolor': 'black'})
    ax2.set_title("Student Category Distribution", fontsize=14, fontweight='bold')
    st.pyplot(fig2)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 3️⃣ SIMPLE MARKS CLASSIFICATION (REGD NO + MARKS)
# =========================================================
st.markdown('<div class="section" style="background-color: #f9fbe7;">', unsafe_allow_html=True)
st.header("3️⃣ Simple Marks Classification (Regd No & Marks Only)")

simple_marks_file = st.file_uploader("Upload Excel/CSV (Regd No and Marks Only)", type=["xlsx", "csv"], key="simple")

if simple_marks_file:
    df_simple = pd.read_csv(simple_marks_file) if simple_marks_file.name.endswith('.csv') else pd.read_excel(simple_marks_file)
    df_simple.columns = df_simple.columns.str.strip().str.upper()

    if 'MARKS' not in df_simple.columns:
        st.error("❌ The file must contain a 'MARKS' column.")
    else:
        total_marks = 60
        df_simple['PERCENTAGE'] = (df_simple['MARKS'] / total_marks) * 100

        # Initial classification
        df_simple['CATEGORY'] = 'Average'
        df_simple.loc[df_simple['PERCENTAGE'] < 40, 'CATEGORY'] = 'Slow Learner'
        df_simple.loc[df_simple['PERCENTAGE'] > 60, 'CATEGORY'] = 'Advance Learner'

        # Auto-scale if needed
        if (df_simple['CATEGORY'] == 'Slow Learner').sum() == 0 or (df_simple['CATEGORY'] == 'Advance Learner').sum() == 0:
            st.warning("⚠️ Scaling marks based on highest mark since classification not balanced.")
            highest = df_simple['MARKS'].max()
            df_simple['PERCENTAGE'] = (df_simple['MARKS'] / highest) * 100
            df_simple['CATEGORY'] = 'Average'
            df_simple.loc[df_simple['PERCENTAGE'] < 40, 'CATEGORY'] = 'Slow Learner'
            df_simple.loc[df_simple['PERCENTAGE'] > 60, 'CATEGORY'] = 'Advance Learner'

        st.subheader("Student Classification (Based on Marks)")
        st.dataframe(
            df_simple[['REGD.NO', 'MARKS', 'PERCENTAGE', 'CATEGORY']].style.set_properties(
                **{'text-align': 'center', 'font-weight': 'bold'}
            ),
            use_container_width=True
        )

        # Bar chart
        category_counts = df_simple['CATEGORY'].value_counts().reindex(['Advance Learner', 'Average', 'Slow Learner'], fill_value=0)
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        bars = ax3.bar(category_counts.index, category_counts.values,
                       color=['#00BFFF', '#FFD700', '#FF6347'], width=0.5)

        for bar in bars:
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                     int(bar.get_height()), ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax3.set_title('Marks-Based Student Classification', fontsize=13, fontweight='bold')
        ax3.set_ylabel('Number of Students', fontsize=11)
        ax3.grid(axis='y', linestyle='--', alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig3)

st.markdown('</div>', unsafe_allow_html=True)
