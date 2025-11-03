import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------- Page Configuration -------------------
st.set_page_config(page_title="Student Performance Analyzer", layout="wide")
st.title("🎯 Student Performance Analyzer")

# ------------------- File Upload Section -------------------
uploaded_file = st.file_uploader("📂 Upload Excel File (REGD.NO and MARKS)", type=["xlsx"])

if uploaded_file is not None:
    # Read uploaded Excel
    df = pd.read_excel(uploaded_file)

    # Validate required columns
    if 'REGD.NO' not in df.columns or 'MARKS' not in df.columns:
        st.error("❌ Excel must contain 'REGD.NO' and 'MARKS' columns only.")
    else:
        # ------------------- Basic Setup -------------------
        total_marks = 60
        df['Percentage'] = (df['MARKS'] / total_marks) * 100

        # ------------------- Initial Classification -------------------
        df['Category'] = 'Average'
        df.loc[df['Percentage'] < 40, 'Category'] = 'Slow Learner'
        df.loc[df['Percentage'] > 60, 'Category'] = 'Advanced Learner'

        # Check if categories exist
        if (df['Category'] == 'Slow Learner').sum() == 0 or (df['Category'] == 'Advanced Learner').sum() == 0:
            st.warning("⚠️ No Slow or Advanced learners found — Scaling down based on highest mark...")

            # ------------------- Scale Down Logic -------------------
            max_marks = df['MARKS'].max()
            scaled_total = max_marks  # use top score as new total
            df['Percentage'] = (df['MARKS'] / scaled_total) * 100

            # Recalculate categories
            df['Category'] = 'Average'
            df.loc[df['Percentage'] < 40, 'Category'] = 'Slow Learner'
            df.loc[df['Percentage'] > 60, 'Category'] = 'Advanced Learner'

        # ------------------- Display Styled Data -------------------
        st.subheader("📋 Student Performance Table")

        def highlight_category(val):
            if val == 'Slow Learner':
                return 'background-color: #ffb3b3; color: black; font-weight: bold;'
            elif val == 'Advanced Learner':
                return 'background-color: #b3ffb3; color: black; font-weight: bold;'
            else:
                return 'background-color: #ffffb3; color: black;'

        styled_df = df.style.applymap(highlight_category, subset=['Category']) \
                            .format({'Percentage': '{:.2f}%'})
        st.dataframe(styled_df, use_container_width=True)

        # ------------------- Summary -------------------
        slow_count = (df['Category'] == 'Slow Learner').sum()
        adv_count = (df['Category'] == 'Advanced Learner').sum()
        avg_count = (df['Category'] == 'Average').sum()

        st.markdown(f"""
        ### 📊 Summary
        - 🟥 Slow Learners: **{slow_count}**
        - 🟩 Advanced Learners: **{adv_count}**
        - 🟨 Average Students: **{avg_count}**
        """)

        # ------------------- Graph -------------------
        st.subheader("📈 Learner Distribution")

        categories = ['Slow Learner', 'Average', 'Advanced Learner']
        counts = [slow_count, avg_count, adv_count]
        colors = ['#ff6666', '#fff176', '#66ff66']

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(categories, counts, color=colors, edgecolor='black')

        # Add count labels on top
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.2,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_ylabel("Number of Students")
        ax.set_title("Performance Classification", fontsize=13, fontweight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.6)
        st.pyplot(fig)

else:
    st.info("⬆️ Please upload an Excel file with 'REGD.NO' and 'MARKS' columns to begin.")
