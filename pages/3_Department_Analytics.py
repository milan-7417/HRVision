import streamlit as st
import pandas as pd

from streamlit_extras.stylable_container import stylable_container

from utils.data_loader import load_data
from utils.charts import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Department Analytics | HRVision",

    page_icon="🏢",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ==========================================================
# LOAD CSS
# ==========================================================

with open("assets/style.css") as css:

    st.markdown(

        f"<style>{css.read()}</style>",

        unsafe_allow_html=True

    )

# ==========================================================
# CARD STYLES
# ==========================================================

CARD_STYLE = """
{
    background:white;
    border-radius:18px;
    padding:18px;
    border:1px solid #E5E7EB;
    box-shadow:0 6px 18px rgba(0,0,0,.08);
}
"""

KPI_STYLE = """
{
    background:white;
    border-radius:18px;
    padding:20px;
    border:1px solid #E5E7EB;
    box-shadow:0 8px 18px rgba(0,0,0,.08);

    min-height:240px;

    display:flex;
    flex-direction:column;
    justify-content:center;
}
"""

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center">
            <h1 style="color:white;margin-bottom:0;">👨‍💼 HRVision</h1>
            <p style="color:#DBEAFE;">
                HR Workforce Intelligence
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()

    st.markdown("### 🔍 Filters")

    department = st.multiselect(
        "Department",
        sorted(df["Department"].unique()),
        default=sorted(df["Department"].unique())
    )

    job_role = st.multiselect(
        "Job Role",
        sorted(df["JobRole"].unique()),
        default=sorted(df["JobRole"].unique())
    )

    travel = st.multiselect(
        "Business Travel",
        sorted(df["BusinessTravel"].unique()),
        default=sorted(df["BusinessTravel"].unique())
    )

    overtime = st.multiselect(
        "OverTime",
        sorted(df["OverTime"].unique()),
        default=sorted(df["OverTime"].unique())
    )

    st.divider()

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        st.switch_page("app.py")

    st.divider()

# ==========================================================
# FILTER DATA
# ==========================================================

filtered_df = df[

    (df["Department"].isin(department))

    &

    (df["JobRole"].isin(job_role))

    &

    (df["BusinessTravel"].isin(travel))

    &

    (df["OverTime"].isin(overtime))

]

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🏢 Department Analytics")

st.write(
    """
    Compare departments based on workforce,
    compensation,
    performance,
    experience,
    and operational trends.
    """
)

st.divider()

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_departments = filtered_df["Department"].nunique()

largest_department = (
    filtered_df["Department"]
    .value_counts()
    .idxmax()
)

avg_performance = (
    filtered_df["PerformanceRating"]
    .mean()
)

avg_experience = (
    filtered_df["TotalWorkingYears"]
    .mean()
)

avg_salary = (
    filtered_df["MonthlyIncome"]
    .mean()
)

# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("📊 Department Overview")

st.markdown("<br>", unsafe_allow_html=True)

cols = st.columns(5)

kpis = [

    ("🏢", total_departments, "Departments"),

    ("👨‍💼", largest_department, "Largest Department"),

    ("📈", f"{avg_performance:.2f}", "Performance"),

    ("⏳", f"{avg_experience:.1f}", "Experience"),

    ("💰", f"${avg_salary:,.0f}", "Avg Salary")

]

for col, (icon, value, title) in zip(cols, kpis):

    with col:

        with stylable_container(

            key=f"kpi_{title}",

            css_styles=KPI_STYLE

        ):

            st.markdown(
                f"""
                <div style="text-align:center;font-size:40px;">
                    {icon}
                </div>
                <div style='height:70px; display:flex; align-items:center; justify-content:center;'>
                    <h3 style='text-align:center; color:#2563EB; font-size:26px; margin:0; line-height:1.3; word-break:break-word;'>{value}</h3>
                </div>
                <h4 style='text-align:center; margin-top:12px; margin-bottom:0;'>{title}</h4>
                """,
                unsafe_allow_html=True,
            )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("👥 Department Workforce Analysis")

st.caption(
    "Compare employee count and average salary across departments."
)

left, right = st.columns(2, gap="large")

with left:

    employee_df = (
        filtered_df["Department"]
        .value_counts()
        .reset_index()
    )

    employee_df.columns = ["Department", "Employees"]

    fig = bar_chart(
        df=employee_df,
        x="Department",
        y="Employees",
        title="Employees by Department"
    )

    with stylable_container(
        key="employees_department",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with right:

    salary_df = (
        filtered_df
        .groupby("Department")["MonthlyIncome"]
        .mean()
        .reset_index()
    )

    salary_df.columns = ["Department", "Average Salary"]

    fig = bar_chart(
        df=salary_df,
        x="Department",
        y="Average Salary",
        title="Average Monthly Salary"
    )

    with stylable_container(
        key="salary_department",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📈 Department Performance")

st.caption(
    "Compare employee performance ratings across departments."
)

performance_df = filtered_df.copy()

fig = box_plot(

    df=performance_df,

    x="Department",

    y="PerformanceRating",

    title="Performance Rating by Department"

)

with stylable_container(

    key="performance_department",

    css_styles=CARD_STYLE

):

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar": False}

    )

st.subheader("⏳ Experience Analysis")

st.caption(
    "Compare employee experience across departments."
)

left, right = st.columns(2, gap="large")

with left:

    experience_df = (
        filtered_df
        .groupby("Department")["TotalWorkingYears"]
        .mean()
        .reset_index()
    )

    experience_df.columns = [
        "Department",
        "Average Experience"
    ]

    fig = bar_chart(
        df=experience_df,
        x="Department",
        y="Average Experience",
        title="Average Experience by Department"
    )

    with stylable_container(
        key="experience_department",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with right:

    fig = histogram_chart(
        df=filtered_df,
        x="YearsAtCompany",
        title="Years at Company Distribution",
        bins=15
    )

    with stylable_container(
        key="years_company_department",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("💼 Job Roles & Overtime")

st.caption(
    "Analyze workforce composition and overtime across departments."
)

left, right = st.columns(2, gap="large")

with left:

    role_df = (
        filtered_df
        .groupby(["Department", "JobRole"])
        .size()
        .reset_index(name="Employees")
    )

    fig = grouped_bar_chart(
        df=role_df,
        x="Department",
        y="Employees",
        color="JobRole",
        title="Job Roles by Department"
    )

    with stylable_container(
        key="jobrole_department",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with right:

    overtime_df = (
        filtered_df
        .groupby(["Department", "OverTime"])
        .size()
        .reset_index(name="Employees")
    )

    fig = grouped_bar_chart(
        df=overtime_df,
        x="Department",
        y="Employees",
        color="OverTime",
        title="Overtime by Department"
    )

    with stylable_container(
        key="overtime_department",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

st.markdown("<br>", unsafe_allow_html=True)

st.divider()

st.subheader("💡 Department Insights")

largest_department = (
    filtered_df["Department"]
    .value_counts()
    .idxmax()
)

highest_salary_department = (
    filtered_df.groupby("Department")["MonthlyIncome"]
    .mean()
    .idxmax()
)

highest_experience_department = (
    filtered_df.groupby("Department")["TotalWorkingYears"]
    .mean()
    .idxmax()
)

highest_performance_department = (
    filtered_df.groupby("Department")["PerformanceRating"]
    .mean()
    .idxmax()
)

highest_overtime_department = (
    filtered_df[filtered_df["OverTime"] == "Yes"]["Department"]
    .value_counts()
    .idxmax()
)

st.info(f"""
### 📊 Department Summary

- 🏢 Largest Department: **{largest_department}**

- 💰 Highest Average Salary: **{highest_salary_department}**

- ⏳ Most Experienced Workforce: **{highest_experience_department}**

- 📈 Highest Performance Rating: **{highest_performance_department}**

- ⏱️ Highest Overtime: **{highest_overtime_department}**

---

### 🎯 Recommendations

- Review staffing distribution across departments.
- Benchmark high-performing departments and share best practices.
- Monitor overtime to reduce employee burnout.
- Ensure salary structures remain competitive and equitable.
""")


