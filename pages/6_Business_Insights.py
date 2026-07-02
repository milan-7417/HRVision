import streamlit as st
import pandas as pd

from streamlit_extras.stylable_container import stylable_container

from utils.data_loader import load_data
from utils.charts import *

st.set_page_config(
    page_title="Business Insights | HRVision",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("assets/style.css") as css:
    st.markdown(
        f"<style>{css.read()}</style>",
        unsafe_allow_html=True
    )

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

df = load_data()

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

    st.divider()

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        st.switch_page("app.py")

    st.divider()


filtered_df = df[
    (df["Department"].isin(department))
    &
    (df["Gender"].isin(gender))
    &
    (df["JobRole"].isin(job_role))
]

st.title("💡 Business Insights")

st.write(
    """
    Executive summary of workforce performance,
    employee retention,
    compensation,
    and organizational trends.
    """
)

st.divider()

total_emp = len(filtered_df)

attrition_rate = (
    filtered_df["Attrition"]
    .eq("Yes")
    .mean() * 100
)

avg_salary = filtered_df["MonthlyIncome"].mean()

largest_department = (
    filtered_df["Department"]
    .value_counts()
    .idxmax()
)

avg_performance = (
    filtered_df["PerformanceRating"]
    .mean()
)

st.subheader("📈 Executive Summary")

st.markdown("<br>", unsafe_allow_html=True)

cols = st.columns(5)

kpis = [

    ("👥", total_emp, "Employees"),

    ("🚪", f"{attrition_rate:.1f}%", "Attrition Rate"),

    ("💰", f"₹ {avg_salary:,.0f}", "Avg Salary"),

    ("🏢", largest_department.replace("Research & Development","R&D").replace("Human Resources","HR"), "Largest Department"),

    ("⭐", f"{avg_performance:.2f}", "Performance")

]

for col, (icon, value, title) in zip(cols, kpis):

    with col:

        with stylable_container(
            key=f"kpi_{title}",
            css_styles=KPI_STYLE
        ):

            st.markdown(f"""
            <div style="text-align:center;font-size:40px;">{icon}</div>

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
                ">
                    {value}
                </h3>
            </div>

            <h4 style="text-align:center;">
                {title}
            </h4>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🏆 Department Performance Overview")

st.caption(
    "Compare departments based on workforce size and average performance."
)

left, right = st.columns(2, gap="large")

with left:

    workforce_df = (

        filtered_df["Department"]

        .value_counts()

        .reset_index()

    )

    workforce_df.columns = [

        "Department",

        "Employees"

    ]

    fig = bar_chart(

        df=workforce_df,

        x="Department",

        y="Employees",

        title="Employees by Department"

    )

    with stylable_container(

        key="workforce_department",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

with right:

    performance_df = (

        filtered_df

        .groupby("Department")["PerformanceRating"]

        .mean()

        .reset_index()

    )

    performance_df.columns = [

        "Department",

        "Performance"

    ]

    fig = bar_chart(

        df=performance_df,

        x="Department",

        y="Performance",

        title="Average Performance Rating"

    )

    with stylable_container(

        key="department_performance",

        css_styles=CARD_STYLE

    ):

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={"displayModeBar":False}

        )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🚪 Attrition & Compensation")

st.caption(
    "Compare employee attrition and compensation across departments."
)

left, right = st.columns(2, gap="large")

with left:

    attrition_df = (

        filtered_df

        .groupby(["Department","Attrition"])

        .size()

        .reset_index(name="Employees")

    )

    fig = grouped_bar_chart(

        df=attrition_df,

        x="Department",

        y="Employees",

        color="Attrition",

        title="Department-wise Attrition"

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

    salary_df = (

        filtered_df

        .groupby("Department")["MonthlyIncome"]

        .mean()

        .reset_index()

    )

    salary_df.columns = [

        "Department",

        "Average Salary"

    ]

    fig = bar_chart(

        df=salary_df,

        x="Department",

        y="Average Salary",

        title="Average Salary by Department"

    )

    fig.update_yaxes(

        tickprefix="₹ "

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

st.subheader("👥 Workforce Composition")

st.caption(
    "Understand employee distribution across the organization."
)

gender_df = (

    filtered_df["Gender"]

    .value_counts()

    .reset_index()

)

gender_df.columns = [

    "Gender",

    "Employees"

]

fig = donut_chart(

    df=gender_df,

    names="Gender",

    values="Employees",

    title="Workforce Composition"

)

with stylable_container(

    key="gender_composition",

    css_styles=CARD_STYLE

):

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar":False}

    )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📊 Executive Scorecard")

st.caption(
    "Overall organizational performance based on workforce, compensation, and attrition metrics."
)

left, right = st.columns(2, gap="large")

with left:

    attrition_score = max(0, 100 - attrition_rate)

    performance_score = avg_performance * 25

    salary_score = min(100, (avg_salary / 10000) * 100)

    overall_score = (
        attrition_score * 0.40
        + performance_score * 0.35
        + salary_score * 0.25
    )

    with stylable_container(
        key="health_score",
        css_styles=CARD_STYLE
    ):

        st.metric(
            "🏆 Organization Health Score",
            f"{overall_score:.1f}/100"
        )

        st.progress(overall_score / 100)

with right:

    if attrition_rate < 10:
        risk = "🟢 Low"

    elif attrition_rate < 20:
        risk = "🟡 Moderate"

    else:
        risk = "🔴 High"

    with stylable_container(
        key="risk_level",
        css_styles=CARD_STYLE
    ):

        st.metric(
            "🚨 Attrition Risk",
            risk
        )

        st.write(
            f"Current Attrition Rate: **{attrition_rate:.1f}%**"
        )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🎯 Key Business Findings")

highest_salary_department = (
    filtered_df.groupby("Department")["MonthlyIncome"]
    .mean()
    .idxmax()
)

highest_attrition_department = (
    filtered_df[filtered_df["Attrition"] == "Yes"]["Department"]
    .value_counts()
    .idxmax()
)

largest_department = (
    filtered_df["Department"]
    .value_counts()
    .idxmax()
)

top_role = (
    filtered_df["JobRole"]
    .value_counts()
    .idxmax()
)

avg_age = filtered_df["Age"].mean()

st.success(f"""

### 📌 Executive Highlights

✅ Total Workforce: **{len(filtered_df):,} Employees**

✅ Largest Department: **{largest_department}**

✅ Highest Paying Department: **{highest_salary_department}**

✅ Highest Attrition Department: **{highest_attrition_department}**

✅ Most Common Job Role: **{top_role}**

✅ Average Employee Age: **{avg_age:.1f} Years**

✅ Organization Health Score: **{overall_score:.1f}/100**

""")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("💡 Strategic HR Recommendations")

st.info("""

### Short-Term Actions

• Monitor departments with above-average attrition.

• Reduce excessive overtime to improve work-life balance.

• Review compensation for lower-paid job roles.

• Improve onboarding and mentorship programs.

---

### Mid-Term Actions

• Invest in employee learning and career development.

• Introduce recognition and reward programs.

• Benchmark high-performing departments.

• Strengthen employee engagement initiatives.

---

### Long-Term Strategy

• Build predictive attrition models.

• Implement AI-powered workforce planning.

• Develop succession planning for key positions.

• Continuously monitor workforce KPIs through HRVision.

""")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📋 Management Action Plan")

action_plan = pd.DataFrame({

    "Priority": [
        "High",
        "High",
        "Medium",
        "Medium",
        "Low"
    ],

    "Action": [

        "Reduce Attrition",

        "Improve Employee Engagement",

        "Optimize Compensation",

        "Leadership Development",

        "Increase Workforce Diversity"

    ],

    "Expected Impact": [

        "Higher Employee Retention",

        "Better Productivity",

        "Improved Satisfaction",

        "Higher Performance",

        "Inclusive Workplace"

    ]

})

st.dataframe(
    action_plan,
    use_container_width=True,
    hide_index=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.success("""

## 🎉 HRVision Executive Summary

HRVision transforms employee data into actionable business intelligence.

By combining workforce analytics, department performance,
compensation insights, and attrition analysis,
organizations can make smarter, data-driven HR decisions.

""")