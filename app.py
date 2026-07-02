import streamlit as st

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="HRVision",
    page_icon="👨‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# CSS
# -------------------------------
with open("assets/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR
# -------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center">
        <h1 style="color:white;margin-bottom:0;">👨‍💼 HRVision</h1>
        <p style="color:#dbeafe;font-size:15px;">
        HR Workforce Intelligence
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 📑 Navigation")

    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/1_Executive_Dashboard.py", label="📊 Executive Dashboard")
    st.page_link("pages/2_Workforce_Analytics.py", label="👥 Workforce Analytics")
    st.page_link("pages/3_Department_Analytics.py", label="🏢 Department Analytics")
    st.page_link("pages/4_Compensation_Analysis.py", label="💰 Compensation Analysis")
    st.page_link("pages/5_Attrition_Analysis.py", label="🚪 Attrition Analysis")
    st.page_link("pages/6_Business_Insights.py", label="💡 Business Insights")

    st.divider()

    st.info(
        """
 🏷️**Version 1.0**

    """
    )

# -------------------------------
# HERO
# -------------------------------

left, right = st.columns([1.2,1])

with left:

    st.markdown(
        """
        <p style='color:#2563eb;
        font-size:28px;
        font-weight:600;
        margin-bottom:0'>
        Welcome to
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 style='font-size:70px;
        margin-top:-10px;
        color:#1e3a8a'>
        HRVision
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h3 style='margin-top:-20px'>
        HR Workforce Intelligence Dashboard
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.write(
        """
Empower your organization with data-driven workforce insights.

Analyze employee demographics,
department performance,
salary trends,
attrition patterns,
and employee satisfaction
through interactive dashboards.
"""
    )

    st.button("🚀 Explore Dashboard")

with right:

    st.image(
        "assets/hero.png",
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# KPI SECTION
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <h2 style="text-align:center;">
        Workforce Overview
    </h2>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="kpi-card">
        <div class="icon">👥</div>
        <h1>1470+</h1>
        <h4>Employees</h4>
        
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kpi-card">
        <div class="icon">🏢</div>
        <h1>3</h1>
        <h4>Departments</h4>
        
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="kpi-card">
        <div class="icon">💼</div>
        <h1>9</h1>
        <h4>Job Roles</h4>
        
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="kpi-card">
        <div class="icon">📈</div>
        <h1>100%</h1>
        <h4>Insights</h4>
        
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

from streamlit_extras.stylable_container import stylable_container
import streamlit as st

# ==========================================================
# WHAT YOU CAN DO
# ==========================================================

st.markdown(
    """
    <h2 style="text-align:center;color:#1E3A8A;margin-bottom:0;">
        🚀 What You Can Do with HRVision
    </h2>

    <p style="text-align:center;
              color:#6B7280;
              font-size:18px;
              margin-bottom:35px;">
        Explore powerful HR analytics modules designed for data-driven workforce decisions.
    </p>
    """,
    unsafe_allow_html=True
)

features = [
    (
        "👥",
        "Workforce Analytics",
        "Analyze employee demographics, age groups, gender distribution and workforce composition."
    ),


    (
        "🏢",
        "Department Analytics",
        "Compare departments using employee count, experience, salary and performance metrics."
    ),

    (
        "💰",
        "Compensation Analysis",
        "Explore salary distribution, compensation trends and department-wise income."
    ),

    (
        "🚪",
        "Attrition Analysis",
        "Identify turnover patterns, overtime impact and retention insights."
    ),

    (
        "😊",
        "Employee Satisfaction",
        "Evaluate work-life balance, satisfaction, environment and engagement."
    ),

    (
        "💡",
        "Business Insights",
        "Generate actionable HR recommendations from workforce analytics."
    ),

    (
        "🎯",
        "Data-Driven Decisions",
        "Support smarter HR decisions through interactive visualizations."
    ),

    (
        "🛡️",
        "Strategic Planning",
        "Align workforce planning with organizational objectives."
    ),
]

for row in range(0, len(features), 4):

    cols = st.columns(4, gap="large")

    for col, (icon, title, desc) in zip(cols, features[row:row+4]):

        with col:
            with stylable_container(
                key=f"card_{title.replace(' ', '_')}",
                css_styles="""
                {
                    background: #ffffff;
                    border: 1px solid #E5E7EB;
                    border-radius: 18px;
                    padding: 20px;
                    min-height: 260px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
                }
                """
            ):
                st.markdown(
                    f"""
                    <div style="
                        font-size:52px;
                        text-align:center;
                        margin-bottom:12px;
                    ">
                        {icon}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <h3 style="
                        text-align:center;
                        color:#1E3A8A;
                        font-weight:700;
                        margin-bottom:12px;
                    ">
                        {title}
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        font-size:15px;
                        line-height:1.8;
                        color:#64748B;
                    ">
                        {desc}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='margin-bottom:35px;'></div>", unsafe_allow_html=True)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#6B7280;
        font-size:15px;
        padding:10px 0;
    ">
        <strong>HRVision v1.0</strong> &nbsp;|&nbsp;
        Made with ❤️ using Streamlit &nbsp;|&nbsp;
        © 2026
    </div>
    """,
    unsafe_allow_html=True,
)