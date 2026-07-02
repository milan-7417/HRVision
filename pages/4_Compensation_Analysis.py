import streamlit as st
import pandas as pd

from streamlit_extras.stylable_container import stylable_container

from utils.data_loader import load_data
from utils.charts import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Compensation Analysis | HRVision",

    page_icon="💰",

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
    min-height:230px;
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

    education = st.multiselect(

        "Education Field",

        sorted(df["EducationField"].unique()),

        default=sorted(df["EducationField"].unique())
    
    )

    gender = st.multiselect(

        "Gender",

        sorted(df["Gender"].unique()),

        default=sorted(df["Gender"].unique())

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

    (df["EducationField"].isin(education))

    &

    (df["Gender"].isin(gender))

]

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("💰 Compensation Analysis")

st.write(
    """
    Analyze employee compensation,
    salary distribution,
    salary hike,
    and income patterns across departments.
    """
)

st.divider()

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

avg_salary = filtered_df["MonthlyIncome"].mean()

highest_salary = filtered_df["MonthlyIncome"].max()

lowest_salary = filtered_df["MonthlyIncome"].min()

avg_hike = filtered_df["PercentSalaryHike"].mean()

avg_daily_rate = filtered_df["DailyRate"].mean()

# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("📈 Compensation Overview")

st.markdown("<br>", unsafe_allow_html=True)

cols = st.columns(5)

kpis = [

    ("💰", f"${avg_salary:,.0f}", "Avg Salary"),

    ("📈", f"{avg_hike:.1f}%", "Salary Hike"),

    ("💵", f"${highest_salary:,.0f}", "Highest Salary"),

    ("💸", f"${lowest_salary:,.0f}", "Lowest Salary"),

    ("🪙", f"${avg_daily_rate:,.0f}", "Daily Rate")

]

for col, (icon, value, title) in zip(cols, kpis):

    with col:

        with stylable_container(

            key=f"kpi_{title}",

            css_styles=KPI_STYLE

        ):

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-size:40px;
                    margin-bottom:10px;
                ">
                    {icon}
                </div>

                <div style="
                    height:65px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                ">
                    <h3 style="
                        text-align:center;
                        color:#2563EB;
                        margin:0;
                        font-size:28px;
                    ">
                        {value}
                    </h3>
                </div>

                <h4 style="
                    text-align:center;
                    margin-top:10px;
                ">
                    {title}
                </h4>
                """,
                unsafe_allow_html=True
            )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("💰 Salary Analysis")

st.caption(
    "Analyze salary distribution across the organization."
)

left, right = st.columns(2, gap="large")

with left:

    fig = histogram_chart(

        df=filtered_df,

        x="MonthlyIncome",

        title="Monthly Salary Distribution",

        bins=25

    )

    fig.update_layout(

        xaxis_title="Monthly Salary",

        yaxis_title="Employees"

    )

    with stylable_container(

        key="salary_distribution",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

with right:

    salary_department = (

        filtered_df

        .groupby("Department")["MonthlyIncome"]

        .mean()

        .reset_index()

    )

    salary_department.columns=[

        "Department",

        "Average Salary"

    ]

    fig = bar_chart(

        df=salary_department,

        x="Department",

        y="Average Salary",

        title="Average Salary by Department"

    )

    fig.update_layout(

        yaxis_title="Average Salary"

    )

    with stylable_container(

        key="salary_department",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("💼 Job Role Compensation")

st.caption(
    "Compare salaries and salary hikes across job roles."
)

left, right = st.columns(2, gap="large")

with left:

    role_salary = (

        filtered_df

        .groupby("JobRole")["MonthlyIncome"]

        .mean()

        .sort_values(ascending=False)

        .reset_index()

    )

    role_salary.columns=[

        "Job Role",

        "Average Salary"

    ]

    fig = bar_chart(

        df=role_salary,

        x="Job Role",

        y="Average Salary",

        title="Average Salary by Job Role",

        horizontal=True

    )

    fig.update_layout(

        xaxis_title="Average Salary"

    )

    with stylable_container(

        key="salary_jobrole",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

with right:

    salary_hike = (

        filtered_df

        .groupby("Department")["PercentSalaryHike"]

        .mean()

        .reset_index()

    )

    salary_hike.columns=[

        "Department",

        "Salary Hike"

    ]

    fig = bar_chart(

        df=salary_hike,

        x="Department",

        y="Salary Hike",

        title="Average Salary Hike by Department"

    )

    fig.update_layout(

        yaxis_title="Salary Hike (%)"

    )

    with stylable_container(

        key="salary_hike_department",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📈 Experience & Compensation")

st.caption(
    "Analyze the relationship between employee experience and compensation."
)

left, right = st.columns(2, gap="large")

with left:

    fig = scatter_chart(

        df=filtered_df,

        x="TotalWorkingYears",

        y="MonthlyIncome",

        title="Monthly Income vs Total Working Years"

    )

    fig.update_layout(

        xaxis_title="Total Working Years",

        yaxis_title="Monthly Salary"

    )

    with stylable_container(

        key="income_experience",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

with right:

    fig = histogram_chart(

        df=filtered_df,

        x="DailyRate",

        title="Daily Rate Distribution",

        bins=20

    )

    fig.update_layout(

        xaxis_title="Daily Rate",

        yaxis_title="Employees"

    )

    with stylable_container(

        key="daily_rate",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("⏰ Employee Pay Rates")

st.caption(
    "Analyze hourly and monthly compensation patterns."
)

left, right = st.columns(2, gap="large")

with left:

    fig = histogram_chart(

        df=filtered_df,

        x="HourlyRate",

        title="Hourly Rate Distribution",

        bins=18

    )

    fig.update_layout(

        xaxis_title="Hourly Rate",

        yaxis_title="Employees"

    )

    with stylable_container(

        key="hourly_rate",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

with right:

    fig = histogram_chart(

        df=filtered_df,

        x="MonthlyRate",

        title="Monthly Rate Distribution",

        bins=25

    )

    fig.update_layout(

        xaxis_title="Monthly Rate",

        yaxis_title="Employees"

    )

    with stylable_container(

        key="monthly_rate",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

st.divider()

st.subheader("💡 Compensation Insights")

highest_salary_role = (

    filtered_df.groupby("JobRole")["MonthlyIncome"]

    .mean()

    .idxmax()

)

highest_salary_department = (

    filtered_df.groupby("Department")["MonthlyIncome"]

    .mean()

    .idxmax()

)

highest_hike_department = (

    filtered_df.groupby("Department")["PercentSalaryHike"]

    .mean()

    .idxmax()

)

avg_income = filtered_df["MonthlyIncome"].mean()

avg_hike = filtered_df["PercentSalaryHike"].mean()

st.info(f"""
### 💰 Compensation Summary

- 💰 **Average Monthly Salary:** ₹ {avg_income:,.0f}

- 💼 **Highest Paying Job Role:** {highest_salary_role}

- 🏢 **Highest Paying Department:** {highest_salary_department}

- 📈 **Highest Salary Hike:** {highest_hike_department}

- 🎯 **Average Salary Hike:** {avg_hike:.1f}%

---

### 📊 Recommendations

- Maintain equitable salary structures across departments.
- Review compensation for lower-paying job roles.
- Align salary hikes with employee performance and tenure.
- Monitor compensation trends to improve employee retention.
""")

