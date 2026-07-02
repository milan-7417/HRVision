import streamlit as st
import pandas as pd

from streamlit_extras.stylable_container import stylable_container

from utils.data_loader import load_data
from utils.charts import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Attrition Analysis | HRVision",

    page_icon="🚪",

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

    gender = st.multiselect(
        "Gender",
        sorted(df["Gender"].unique()),
        default=sorted(df["Gender"].unique())
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

    (df["Gender"].isin(gender))

    &

    (df["JobRole"].isin(job_role))

    &

    (df["BusinessTravel"].isin(travel))

]

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🚪 Attrition Analysis")

st.write(
    """
    Analyze employee turnover patterns,
    identify attrition drivers,
    and understand workforce retention across departments.
    """
)

st.divider()

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_employees = len(filtered_df)

employees_left = len(
    filtered_df[
        filtered_df["Attrition"] == "Yes"
    ]
)

active_employees = len(
    filtered_df[
        filtered_df["Attrition"] == "No"
    ]
)

attrition_rate = (
    employees_left / total_employees * 100
    if total_employees > 0 else 0
)

overtime_attrition = len(

    filtered_df[
        (filtered_df["Attrition"] == "Yes")
        &
        (filtered_df["OverTime"] == "Yes")
    ]

)

avg_years_before_exit = (

    filtered_df[
        filtered_df["Attrition"] == "Yes"
    ]["YearsAtCompany"].mean()

)

# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("📊 Attrition Overview")

st.markdown("<br>", unsafe_allow_html=True)

cols = st.columns(5)

kpis = [

    ("🚪", f"{attrition_rate:.1f}%", "Attrition Rate"),

    ("👥", employees_left, "Employees Left"),

    ("🟢", active_employees, "Active Employees"),

    ("⏰", overtime_attrition, "Overtime Attrition"),

    ("📉", f"{avg_years_before_exit:.1f}", "Avg Years Before Exit")

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

st.subheader("🏢 Department & Gender Attrition")

st.caption(
    "Analyze employee attrition across departments and gender."
)

left, right = st.columns(2, gap="large")

with left:

    department_attrition = (

        filtered_df[
            filtered_df["Attrition"] == "Yes"
        ]

        .groupby("Department")

        .size()

        .reset_index(name="Employees")

    )

    fig = bar_chart(

        df=department_attrition,

        x="Department",

        y="Employees",

        title="Attrition by Department"

    )

    with stylable_container(

        key="department_attrition",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

with right:

    gender_attrition = (

        filtered_df[
            filtered_df["Attrition"] == "Yes"
        ]["Gender"]

        .value_counts()

        .reset_index()

    )

    gender_attrition.columns = [

        "Gender",

        "Employees"

    ]

    fig = donut_chart(

        df=gender_attrition,

        names="Gender",

        values="Employees",

        title="Gender-wise Attrition"

    )

    with stylable_container(

        key="gender_attrition",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🎂 Age Group & Job Role Attrition")

st.caption(
    "Understand which age groups and job roles experience the highest employee turnover."
)

left, right = st.columns(2, gap="large")

with left:

    age_df = filtered_df.copy()

    age_df["Age Group"] = pd.cut(

        age_df["Age"],

        bins=[18,25,35,45,55,65],

        labels=[
            "18-25",
            "26-35",
            "36-45",
            "46-55",
            "56-65"
        ]

    )

    age_attrition = (

        age_df[
            age_df["Attrition"]=="Yes"
        ]

        .groupby("Age Group")

        .size()

        .reset_index(name="Employees")

    )

    fig = bar_chart(

        df=age_attrition,

        x="Age Group",

        y="Employees",

        title="Age Group Attrition"

    )

    with stylable_container(

        key="age_group_attrition",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

with right:

    role_attrition = (

        filtered_df[
            filtered_df["Attrition"]=="Yes"
        ]

        .groupby("JobRole")

        .size()

        .reset_index(name="Employees")

    )

    fig = bar_chart(

        df=role_attrition,

        x="JobRole",

        y="Employees",

        title="Attrition by Job Role",

        horizontal=True

    )

    with stylable_container(

        key="jobrole_attrition",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

st.subheader("✈️ Business Travel & Overtime Analysis")

st.caption(
    "Analyze the impact of business travel and overtime on employee attrition."
)

left, right = st.columns(2, gap="large")

with left:

    travel_attrition = (

        filtered_df

        .groupby(["BusinessTravel", "Attrition"])

        .size()

        .reset_index(name="Employees")

    )

    fig = grouped_bar_chart(

        df=travel_attrition,

        x="BusinessTravel",

        y="Employees",

        color="Attrition",

        title="Business Travel vs Attrition"

    )

    with stylable_container(

        key="business_travel_attrition",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

with right:

    overtime_attrition = (

        filtered_df

        .groupby(["OverTime", "Attrition"])

        .size()

        .reset_index(name="Employees")

    )

    fig = grouped_bar_chart(

        df=overtime_attrition,

        x="OverTime",

        y="Employees",

        color="Attrition",

        title="Overtime vs Attrition"

    )

    with stylable_container(

        key="overtime_attrition",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

st.subheader("😊 Job Satisfaction & Attrition")

st.caption(
    "Understand the relationship between job satisfaction and employee turnover."
)

satisfaction_df = (

    filtered_df

    .groupby(["JobSatisfaction", "Attrition"])

    .size()

    .reset_index(name="Employees")

)

fig = grouped_bar_chart(

    df=satisfaction_df,

    x="JobSatisfaction",

    y="Employees",

    color="Attrition",

    title="Job Satisfaction vs Attrition"

)

with stylable_container(

    key="job_satisfaction_attrition",

    css_styles=CARD_STYLE

):

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar":False}

    )

st.markdown("<br>", unsafe_allow_html=True)

st.divider()

st.subheader("💡 Attrition Insights")

highest_attrition_department = (

    filtered_df[filtered_df["Attrition"] == "Yes"]

    ["Department"]

    .value_counts()

    .idxmax()

)

highest_attrition_role = (

    filtered_df[filtered_df["Attrition"] == "Yes"]

    ["JobRole"]

    .value_counts()

    .idxmax()

)

highest_travel = (

    filtered_df[filtered_df["Attrition"] == "Yes"]

    ["BusinessTravel"]

    .value_counts()

    .idxmax()

)

avg_exit_years = (

    filtered_df[
        filtered_df["Attrition"] == "Yes"
    ]["YearsAtCompany"].mean()

)

attrition_rate = (

    len(filtered_df[
        filtered_df["Attrition"] == "Yes"
    ])

    /

    len(filtered_df)

) * 100

st.info(f"""
### 📊 Attrition Summary

- 🚪 **Overall Attrition Rate:** {attrition_rate:.1f}%

- 🏢 **Highest Attrition Department:** {highest_attrition_department}

- 💼 **Highest Attrition Job Role:** {highest_attrition_role}

- ✈️ **Most Common Business Travel:** {highest_travel}

- 📉 **Average Years Before Exit:** {avg_exit_years:.1f}

---

### 🎯 HR Recommendations

- Improve employee engagement in high-attrition departments.
- Review overtime policies to reduce employee burnout.
- Strengthen career growth opportunities for high-turnover job roles.
- Enhance onboarding and retention strategies for early-career employees.
- Monitor business travel frequency and work-life balance.
""")