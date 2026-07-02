import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from utils.data_loader import load_data
from utils.charts import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Workforce Analytics | HRVision",
    page_icon="👥",
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
# CARD STYLE
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

    gender = st.multiselect(
        "Gender",
        sorted(df["Gender"].unique()),
        default=sorted(df["Gender"].unique())
    )

    department = st.multiselect(
        "Department",
        sorted(df["Department"].unique()),
        default=sorted(df["Department"].unique())
    )

    education = st.multiselect(
        "Education Field",
        sorted(df["EducationField"].unique()),
        default=sorted(df["EducationField"].unique())
    )

    marital = st.multiselect(
        "Marital Status",
        sorted(df["MaritalStatus"].unique()),
        default=sorted(df["MaritalStatus"].unique())
    )

    st.divider()

    if st.button(
    "🏠 Home",
    use_container_width=True
):
      st.switch_page("app.py")

   

# ==========================================================
# FILTER DATA
# ==========================================================

filtered_df = df[

    (df["Gender"].isin(gender))

    &

    (df["Department"].isin(department))

    &

    (df["EducationField"].isin(education))

    &

    (df["MaritalStatus"].isin(marital))

]

# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("👥 Workforce Analytics")

st.write(
    """
    Analyze workforce demographics including
    gender,
    age,
    education,
    marital status,
    and employee distribution.
    """
)

st.divider()

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_emp = len(filtered_df)

male = len(
    filtered_df[
        filtered_df["Gender"] == "Male"
    ]
)

female = len(
    filtered_df[
        filtered_df["Gender"] == "Female"
    ]
)

avg_age = filtered_df["Age"].mean()

education_fields = filtered_df[
    "EducationField"
].nunique()

# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("📈 Workforce Overview")

st.markdown("<br>", unsafe_allow_html=True)

cols = st.columns(5)

kpis = [

    ("👥", total_emp, "Employees"),

    ("👨", male, "Male"),

    ("👩", female, "Female"),

    ("🎂", f"{avg_age:.1f}", "Average Age"),

    ("🎓", education_fields, "Education Fields")

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

                <h1 style="
                text-align:center;
                color:#2563EB;
                margin:8px 0;
                ">
                {value}
                </h1>

                <h4 style="
                text-align:center;
                margin:0;
                ">
                {title}
                </h4>
                """,

                unsafe_allow_html=True

            )

st.markdown("<br>", unsafe_allow_html=True)


st.subheader("👥 Gender & Age Analysis")

st.caption(
    "Analyze workforce gender composition and employee age distribution."
)

left, right = st.columns(2, gap="large")

with left:

    gender_df = (
        filtered_df["Gender"]
        .value_counts()
        .reset_index()
    )

    gender_df.columns = ["Gender", "Employees"]

    fig = donut_chart(
        df=gender_df,
        names="Gender",
        values="Employees",
        title="Gender Distribution"
    )

    with stylable_container(
        key="gender_distribution",
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
        x="Age",
        title="Employee Age Distribution",
        bins=18
    )

    with stylable_container(
        key="age_distribution",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🎓 Education & Personal Profile")

st.caption(
    "Understand employees' educational background and marital status."
)

left, right = st.columns(2, gap="large")

with left:

    education_df = (
        filtered_df["EducationField"]
        .value_counts()
        .reset_index()
    )

    education_df.columns = ["Education", "Employees"]

    fig = bar_chart(
        df=education_df,
        x="Education",
        y="Employees",
        title="Education Field Distribution"
    )

    with stylable_container(
        key="education_distribution",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with right:

    marital_df = (
        filtered_df["MaritalStatus"]
        .value_counts()
        .reset_index()
    )

    marital_df.columns = ["Status", "Employees"]

    fig = donut_chart(
        df=marital_df,
        names="Status",
        values="Employees",
        title="Marital Status"
    )

    with stylable_container(
        key="marital_distribution",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🌍 Business Travel & Job Roles")

st.caption(
    "Analyze employee business travel frequency and workforce distribution across job roles."
)

left, right = st.columns(2, gap="large")

with left:

    travel_df = (
        filtered_df["BusinessTravel"]
        .value_counts()
        .reset_index()
    )

    travel_df.columns = ["Travel", "Employees"]

    fig = bar_chart(
        df=travel_df,
        x="Travel",
        y="Employees",
        title="Business Travel Distribution"
    )

    with stylable_container(
        key="business_travel",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with right:

    role_df = (
        filtered_df["JobRole"]
        .value_counts()
        .reset_index()
    )

    role_df.columns = ["Job Role", "Employees"]

    fig = bar_chart(
        df=role_df,
        x="Job Role",
        y="Employees",
        title="Job Role Distribution",
        horizontal=True
    )

    with stylable_container(
        key="job_role_distribution",
        css_styles=CARD_STYLE
    ):

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

st.divider()

st.subheader("💡 Workforce Insights")

male_pct = (
    filtered_df["Gender"]
    .value_counts(normalize=True)
    .get("Male", 0) * 100
)

female_pct = (
    filtered_df["Gender"]
    .value_counts(normalize=True)
    .get("Female", 0) * 100
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

top_education = (
    filtered_df["EducationField"]
    .value_counts()
    .idxmax()
)

avg_age = filtered_df["Age"].mean()

travel = (
    filtered_df["BusinessTravel"]
    .value_counts()
    .idxmax()
)

st.info(f"""
### 📊 Workforce Summary

- 👥 **Total Employees:** {len(filtered_df):,}

- 👨 **Male Employees:** {male_pct:.1f}%

- 👩 **Female Employees:** {female_pct:.1f}%

- 🎂 **Average Age:** {avg_age:.1f} years

- 🏢 **Largest Department:** {top_department}

- 💼 **Most Common Job Role:** {top_role}

- 🎓 **Top Education Field:** {top_education}

- 🌍 **Most Common Business Travel:** {travel}

---

### 🎯 Key Recommendations

- Promote workforce diversity through balanced hiring initiatives.
- Invest in career development for high-volume job roles.
- Encourage continuous learning across education groups.
- Review travel policies to maintain employee well-being.
""")


