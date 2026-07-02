import streamlit as st
from utils.data_loader import load_data
import plotly.express as px

CARD_STYLE = """
{
    background:white;
    border-radius:18px;
    padding:15px;
    border:1px solid #E5E7EB;
    box-shadow:0 6px 18px rgba(0,0,0,.08);
}
"""


st.title("📊 Executive Dashboard")

st.write(
    "Gain a high-level overview of your workforce through key HR metrics and interactive visualizations."
)

st.divider()
# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Executive Dashboard | HRVision",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD CSS
# ==========================================

with open("assets/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data()

# ==========================================
# SIDEBAR
# ==========================================

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
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 🔍 Filters")

    # -----------------------
    # Filters
    # -----------------------

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

    overtime = st.multiselect(
        "OverTime",
        sorted(df["OverTime"].unique()),
        default=sorted(df["OverTime"].unique())
    )

    st.divider()

    # -----------------------
    # Home Button
    # -----------------------

    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

    st.divider()

# ==========================================
# FILTER DATA
# ==========================================

filtered_df = df[
    (df["Department"].isin(department))
    & (df["Gender"].isin(gender))
    & (df["JobRole"].isin(job_role))
    & (df["OverTime"].isin(overtime))
]


   # ==========================================================
# KPI SECTION
# ==========================================================

# ---------- Calculate KPIs ----------

total_employees = len(filtered_df)

attrition_rate = (
    filtered_df["Attrition"]
    .value_counts(normalize=True)
    .get("Yes", 0) * 100
)

avg_income = filtered_df["MonthlyIncome"].mean()

avg_age = filtered_df["Age"].mean()

avg_years = filtered_df["YearsAtCompany"].mean()

# ---------- KPI Title ----------

st.subheader("📈 Workforce Overview")

st.write("Quick overview of the organization's workforce.")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# KPI CARDS
# ==========================================================

from streamlit_extras.stylable_container import stylable_container

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

# -----------------------------
# Total Employees
# -----------------------------

with col1:

    with stylable_container(
        key="emp_card",
        css_styles="""
        {
            background:#FFFFFF;
            border:1px solid #E5E7EB;
            border-radius:18px;
            padding:20px;
            box-shadow:0 8px 18px rgba(0,0,0,.08);
        }
        """
    ):

        st.markdown(
            f"""
            <div style="text-align:center;font-size:34px;">👥</div>

            <h1 style="text-align:center;color:#2563EB;margin:10px 0;">
            {total_employees:,}
            </h1>

            <h4 style="text-align:center;margin:0;">
            Total Employees
            </h4>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------
# Attrition Rate
# -----------------------------

with col2:

    with stylable_container(
        key="attrition_card",
        css_styles="""
        {
            background:#FFFFFF;
            border:1px solid #E5E7EB;
            border-radius:18px;
            padding:20px;
            box-shadow:0 8px 18px rgba(0,0,0,.08);
        }
        """
    ):

        st.markdown(
            f"""
            <div style="text-align:center;font-size:34px;">🚪</div>

            <h1 style="text-align:center;color:#EF4444;margin:10px 0;">
            {attrition_rate:.1f}%
            </h1>

            <h4 style="text-align:center;margin:0;">
            Attrition Rate
            </h4>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------
# Avg Income
# -----------------------------

with col3:

    with stylable_container(
        key="income_card",
        css_styles="""
        {
            background:#FFFFFF;
            border:1px solid #E5E7EB;
            border-radius:18px;
            padding:20px;
            box-shadow:0 8px 18px rgba(0,0,0,.08);
        }
        """
    ):

        st.markdown(
            f"""
            <div style="text-align:center;font-size:34px;">💰</div>

            <h1 style="text-align:center;color:#10B981;margin:10px 0;">
            ${avg_income:,.0f}
            </h1>

            <h4 style="text-align:center;margin:0;">
            Avg Income
            </h4>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------
# Average Age
# -----------------------------

with col4:

    with stylable_container(
        key="age_card",
        css_styles="""
        {
            background:#FFFFFF;
            border:1px solid #E5E7EB;
            border-radius:18px;
            padding:20px;
            box-shadow:0 8px 18px rgba(0,0,0,.08);
        }
        """
    ):

        st.markdown(
            f"""
            <div style="text-align:center;font-size:34px;">🎂</div>

            <h1 style="text-align:center;color:#F59E0B;margin:10px 0;">
            {avg_age:.1f}
            </h1>

            <h4 style="text-align:center;margin:0;">
            Average Age
            </h4>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------
# Average Years
# -----------------------------

with col5:

    with stylable_container(
        key="years_card",
        css_styles="""
        {
            background:#FFFFFF;
            border:1px solid #E5E7EB;
            border-radius:18px;
            padding:20px;
            box-shadow:0 8px 18px rgba(0,0,0,.08);
        }
        """
    ):

        st.markdown(
            f"""
            <div style="text-align:center;font-size:34px;">📅</div>

            <h1 style="text-align:center;color:#8B5CF6;margin:10px 0;">
            {avg_years:.1f}
            </h1>

            <h4 style="text-align:center;margin:0;">
            Avg Years
            </h4>
            """,
            unsafe_allow_html=True,
        )

# ==========================================================
# DEPARTMENT ANALYTICS
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🏢 Department Analytics")

st.caption("Employee distribution and attrition across departments.")

left, right = st.columns(2, gap="large")

with left:
    with stylable_container(
        key="department_distribution",
        css_styles=CARD_STYLE
    ):
        dept_count = (
            filtered_df["Department"]
            .value_counts()
            .reset_index()
        )

        dept_count.columns = ["Department", "Employees"]

        fig = px.pie(
            dept_count,
            names="Department",
            values="Employees",
            hole=0.60,
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig.update_layout(
            title="Employee Distribution",
            height=420,
            showlegend=True,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

with right:
    with stylable_container(
        key="attrition_department",
        css_styles=CARD_STYLE
    ):
        attrition = (
            filtered_df[filtered_df["Attrition"] == "Yes"]
            .groupby("Department")
            .size()
            .reset_index(name="Employees")
        )

        fig = px.bar(
            attrition,
            x="Department",
            y="Employees",
            color="Department",
            text="Employees",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            title="Attrition by Department",
            height=420,
            showlegend=False,
            xaxis_title="",
            yaxis_title="Employees",
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("💰 Compensation & Work Pattern Analysis")

st.caption("Analyze employee income distribution and the relationship between overtime and attrition.")

left, right = st.columns(2, gap="large")

with left:
    with stylable_container(
        key="income_distribution",
        css_styles=CARD_STYLE
    ):
        fig = px.histogram(
            filtered_df,
            x="MonthlyIncome",
            nbins=30,
            color_discrete_sequence=["#2563EB"]
        )

        fig.update_layout(
            title="Monthly Income Distribution",
            height=420,
            xaxis_title="Monthly Income",
            yaxis_title="Employees",
            bargap=0.05,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

with right:
    with stylable_container(
        key="overtime_attrition",
        css_styles=CARD_STYLE
    ):
        overtime = (
            filtered_df
            .groupby(["OverTime", "Attrition"])
            .size()
            .reset_index(name="Employees")
        )

        fig = px.bar(
            overtime,
            x="OverTime",
            y="Employees",
            color="Attrition",
            barmode="group",
            text="Employees",
            color_discrete_map={
                "Yes": "#EF4444",
                "No": "#2563EB"
            }
        )

        fig.update_traces(textposition="outside")

        fig.update_layout(
            title="Overtime vs Attrition",
            height=420,
            xaxis_title="OverTime",
            yaxis_title="Employees",
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("👨‍💼 Workforce Insights")

st.caption(
    "Explore employee job roles and workforce experience across the organization."
)

left, right = st.columns(2, gap="large")

with left:
    with stylable_container(
        key="jobrole_distribution",
        css_styles=CARD_STYLE
    ):
        role_df = (
            filtered_df["JobRole"]
            .value_counts()
            .reset_index()
        )

        role_df.columns = ["Job Role", "Employees"]

        fig = px.bar(
            role_df,
            x="Employees",
            y="Job Role",
            orientation="h",
            text="Employees",
            color="Employees",
            color_continuous_scale="Blues"
        )

        fig.update_traces(textposition="outside")

        fig.update_layout(
            title="Employees by Job Role",
            height=430,
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

with right:
    with stylable_container(
        key="years_company",

        css_styles=CARD_STYLE
    ):

        fig = px.histogram(
            filtered_df,
            x="YearsAtCompany",
            nbins=20,
            color_discrete_sequence=["#2563EB"]
        )

        fig.update_layout(

            title="Years at Company Distribution",

            height=430,

            xaxis_title="Years",

            yaxis_title="Employees",

            margin=dict(l=20, r=20, t=60, b=20)

        )

        st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("💡 Executive Summary")

total = len(filtered_df)

attrition = (
    filtered_df["Attrition"]
    .value_counts(normalize=True)
    .get("Yes", 0) * 100
)

top_department = (
    filtered_df["Department"]
    .value_counts()
    .idxmax()
)

top_role = (
    filtered_df["JobRole"]
    .value_counts()
    .idxmax()
)

avg_income = filtered_df["MonthlyIncome"].mean()

avg_years = filtered_df["YearsAtCompany"].mean()

st.info(
f"""
### HR Insights

• **Total Employees:** {total:,}

• **Attrition Rate:** {attrition:.1f}%

• **Largest Department:** {top_department}

• **Most Common Job Role:** {top_role}

• **Average Monthly Income:** ${avg_income:,.0f}

• **Average Years at Company:** {avg_years:.1f} years

---

### Recommendation

Focus retention strategies on departments with higher attrition.
Monitor overtime trends and employee satisfaction regularly.
Invest in career growth and employee engagement to improve retention.
"""
)

