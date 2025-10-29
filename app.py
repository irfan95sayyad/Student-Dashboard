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
st.header("1️⃣ Attendance Analysis")
attendance_file = st.file_uploader("Upload Attendance Excel", type=["xlsx"], key="att")

if attendance_file:
    df_att = pd.read_excel(attendance_file)
    subjects = df_att.columns[3:]
    
    # Preprocess attendance
    def preprocess_att(x):
        if x <= 1:          # decimal like 0.75
            x = x * 100
        x = int(x)          # remove decimals
        return min(x, 75)   # cap at 75
    
    df_att[subjects] = df_att[subjects].applymap(preprocess_att)
    
    # Subjects <75 per student
    def low_attendance(row):
        low_sub = [sub for sub in subjects if row[sub] < 75]
        return ', '.join(low_sub)
    
    df_att['Subjects <75%'] = df_att.apply(low_attendance, axis=1)
    df_att['Count of Subjects <75%'] = df_att['Subjects <75%'].apply(lambda x: len(x.split(',')) if x else 0)
    
    # Count per student per range
    def count_range(row, low, high):
        return sum((row[sub] >= low) & (row[sub] < high) for sub in subjects)

    df_att['<60% Count'] = df_att.apply(lambda row: count_range(row, 0, 60), axis=1)
    df_att['60-70% Count'] = df_att.apply(lambda row: count_range(row, 60, 70), axis=1)
    df_att['70-75% Count'] = df_att.apply(lambda row: count_range(row, 70, 75), axis=1)
    
    # Subjects per range
    def subjects_in_range(row, low, high):
        return ', '.join([sub for sub in subjects if low <= row[sub] < high])

    df_att['Subjects <60%'] = df_att.apply(lambda row: subjects_in_range(row, 0, 60), axis=1)
    df_att['Subjects 60-70%'] = df_att.apply(lambda row: subjects_in_range(row, 60, 70), axis=1)
    df_att['Subjects 70-75%'] = df_att.apply(lambda row: subjects_in_range(row, 70, 75), axis=1)
    
    # Filter students with any subject <75
    low_att_df = df_att[df_att['Count of Subjects <75%'] > 0]

    st.subheader("Students Attendance Summary")
    st.dataframe(
        low_att_df[['REGD.NO','NAME','Subjects <75%','Count of Subjects <75%',
                    '<60% Count','Subjects <60%',
                    '60-70% Count','Subjects 60-65%',
                    '70-75% Count','Subjects 65-75%']].style.set_properties(**{'background-color': '#e6f2ff', 'color': '#000'})
    )
    
    # ----------------- Enhanced Attendance Ranges Chart -----------------
    attendance_ranges = {}
    for sub in subjects:
        low = df_att[df_att[sub] < 60].shape[0]
        moderate = df_att[(df_att[sub] >= 60) & (df_att[sub] < 65)].shape[0]
        near_threshold = df_att[(df_att[sub] >= 65) & (df_att[sub] < 75)].shape[0]
        attendance_ranges[sub] = {'<60%': low, '60-65%': moderate, '65-75%': near_threshold}

    labels = subjects
    low_counts = [attendance_ranges[sub]['<60%'] for sub in labels]
    mid_counts = [attendance_ranges[sub]['60-65%'] for sub in labels]
    high_counts = [attendance_ranges[sub]['65-75%'] for sub in labels]

    fig, ax = plt.subplots(figsize=(12,6))

    # Stacked bars
    ax.bar(labels, low_counts, color='#ff4d4d', label='<60%')
    ax.bar(labels, mid_counts, bottom=low_counts, color='#ffcc66', label='60-65%')
    bottom_high = [low_counts[i] + mid_counts[i] for i in range(len(labels))]
    ax.bar(labels, high_counts, bottom=bottom_high, color='#66b3ff', label='65-75%')

    # Count labels inside each segment
    for i in range(len(labels)):
        if low_counts[i] > 0:
            ax.text(i, low_counts[i]/2, str(low_counts[i]), ha='center', va='center', color='white', fontweight='bold')
        if mid_counts[i] > 0:
            ax.text(i, low_counts[i] + mid_counts[i]/2, str(mid_counts[i]), ha='center', va='center', color='black', fontweight='bold')
        if high_counts[i] > 0:
            ax.text(i, bottom_high[i] + high_counts[i]/2, str(high_counts[i]), ha='center', va='center', color='white', fontweight='bold')

    # Total labels on top
    total_counts = [low_counts[i]+mid_counts[i]+high_counts[i] for i in range(len(labels))]
    for i, total in enumerate(total_counts):
        ax.text(i, total + 0.2, str(total), ha='center', va='bottom', fontsize=11, fontweight='bold', color='blue')

    # Styling
    ax.set_ylabel("Number of Students", fontsize=12)
    ax.set_title("Attendance Distribution per Subject", fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend()
    st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)  # End Attendance section

# ----------------- MARKS -----------------
st.markdown('<div class="section" style="background-color: #fff0f5;">', unsafe_allow_html=True)
st.header("2️⃣ Marks Analysis")
marks_file = st.file_uploader("Upload Marks Excel", type=["xlsx"], key="marks")

if marks_file:
    df_marks = pd.read_excel(marks_file)
    subjects = df_marks.columns[3:]
    
    df_marks['Total Marks'] = df_marks[subjects].sum(axis=1)
    df_marks['Average %'] = df_marks['Total Marks'] / len(subjects)
    df_marks['Average %'] = df_marks['Average %'].round(2)
    
    def categorize(avg):
        if avg > 60:
            return 'Advance Learner'
        elif avg < 40:
            return 'Slow Learner'
        else:
            return 'Regular Learner'
    
    df_marks['Category'] = df_marks['Average %'].apply(categorize)
    
    st.subheader("Student Categories based on Average Marks")
    st.dataframe(df_marks[['REGD.NO','NAME','Total Marks','Average %','Category']].style.set_properties(**{'background-color': '#fff0f5', 'color': '#000'}))
    
    # Pie chart
    category_counts = df_marks['Category'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(6,6))
    colors_marks = ['#66b3ff','#ff9999','#99ff99']
    ax2.pie(category_counts, labels=category_counts.index, autopct=lambda p: f'{p:.1f}% ({int(p*sum(category_counts)/100)})', startangle=90, colors=colors_marks, wedgeprops={'edgecolor':'black'})
    ax2.set_title("Student Category Distribution", fontsize=14, fontweight='bold')
    st.pyplot(fig2)

st.markdown('</div>', unsafe_allow_html=True)  # End Marks section
