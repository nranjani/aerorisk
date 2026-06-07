import streamlit as st

st.set_page_config(
    page_title="AeroRisk | Flight Intelligence Platform",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 { color: white; font-size: 2.5rem; margin: 0; }
    .main-header p  { color: #a0b4c8; font-size: 1.1rem; margin-top: 0.5rem; }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #4361ee;
    }
    .metric-card h2 { color: #4361ee; font-size: 2rem; margin: 0; }
    .metric-card p  { color: #555; font-size: 0.9rem; margin: 0.3rem 0 0 0; }
    .crisis-card {
        background: #fff5f5;
        border: 1px solid #f8d7da;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .tool-card {
        border-radius: 12px;
        padding: 1.5rem;
        height: 220px;
        margin-bottom: 1rem;
    }
    .source-text {
        color: #888;
        font-size: 11px;
        text-align: center;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='main-header'>
    <h1>✈️ AeroRisk Intelligence Platform</h1>
    <p>Flight Cancellation Prediction & Carrier Benchmarking System</p>
    <p style='color:#7ecef4; font-size:0.9rem;'>
        Built on 220,000+ BTS Flight Records (2015–2025) · XGBoost AUC 0.89 · 82% Recall
    </p>
</div>
""", unsafe_allow_html=True)

# ── 2025 Crisis Banner ────────────────────────────────────────────────────────
st.markdown("## 🚨 2025 U.S. Aviation Crisis")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='crisis-card'>
        <h2 style='color:#dc3545; font-size:2rem;'>248M</h2>
        <p style='color:#333;'><b>Passengers disrupted in 2025</b></p>
        <p style='color:#888; font-size:11px;'>AirHelp 2025 USA Flight Disruption Report</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='crisis-card'>
        <h2 style='color:#fd7e14; font-size:2rem;'>76.84%</h2>
        <p style='color:#333;'><b>On-time performance — worst in recent years</b></p>
        <p style='color:#888; font-size:11px;'>BTS via Kiplinger 2026</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Key Findings ──────────────────────────────────────────────────────────────
st.markdown("## 📊 Key Findings from 10 Years of BTS Data")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class='metric-card'>
        <h2>220K+</h2>
        <p>Flight Records Analyzed</p>
        <p style='color:#888; font-size:11px;'>2015–2025 · 21 Airlines · 300+ Airports</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='metric-card'>
        <h2>73%</h2>
        <p>Delays Are Airline-Caused</p>
        <p style='color:#888; font-size:11px;'>Not weather — controllable by airlines</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='metric-card'>
        <h2>26x</h2>
        <p>Cancellation Rate Gap</p>
        <p style='color:#888; font-size:11px;'>Delta 0.6% vs Peninsula Airways 15.6%</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class='metric-card'>
        <h2>AUC 0.89</h2>
        <p>XGBoost Model Accuracy</p>
        <p style='color:#888; font-size:11px;'>82% Recall · 8,016 High-Risk Flights Flagged</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Two Tools ───────────────────────────────────────────────────────────────
st.markdown("## 🛠️ Two Decision Tools")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='tool-card' style='background:#f0f4ff; border-left:5px solid #4361ee;'>
        <h3 style='color:#4361ee;'>🔍 Cancellation Risk Checker</h3>
        <p style='color:#333;'><b>For: Passengers</b></p>
        <p style='color:#555;'>Enter your airline, airport, and travel month
        to get a real-time cancellation risk score with safer flight alternatives.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ Check My Flight Risk", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Cancellation_Risk_Checker.py")

with col2:
    st.markdown("""
    <div class='tool-card' style='background:#fff4f0; border-left:5px solid #f77f00;'>
        <h3 style='color:#f77f00;'>📉 Delay Cause Breakdown</h3>
        <p style='color:#333;'><b>For: Airline OCC Teams</b></p>
        <p style='color:#555;'>Select any carrier to see a full breakdown
        of delay causes with the biggest driver flagged for immediate action.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ Analyze Delay Causes", use_container_width=True):
        st.switch_page("pages/2_Delay_Cause_Breakdown.py")
st.markdown("<hr>", unsafe_allow_html=True)

# ── Model Performance ─────────────────────────────────────────────────────────
st.markdown("## 🤖 Model Performance")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Model Comparison:**")
    st.markdown("""
    | Model | AUC | Recall |
    |---|---|---|
    | Logistic Regression | 0.71 | 74% |
    | Random Forest | 0.74 | 76% |
    | **XGBoost ✅** | **0.89** | **82%** |
    """)

with col2:
    st.markdown("**Top Predictors (SHAP Analysis):**")
    st.markdown("""
    | Rank | Feature | Importance |
    |---|---|---|
    | 1 | 📅 Travel Month | 26% |
    | 2 | ⏱️ Delay Severity Per Flight | 16% |
    | 3 | ✈️ Total Flight Volume | 15% |
    | 4 | 📊 Delay Rate | 12% |
    | 5 | 🏢 Carrier Delay % | 11% |
    """)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Roadmap ───────────────────────────────────────────────────────────────────
st.markdown("## 🚀 Future Roadmap")
col1, col2 = st.columns(2)

with col1:
    st.info("""
    **Phase 2 — Amadeus API Integration**
    Surface ML cancellation risk scores
    at point of booking on third-party
    platforms like Expedia and Google Flights
    """)

with col2:
    st.info("""
    **Phase 3 — Real-Time Flight Data**
    AviationStack API integration for
    live risk scoring beyond historical
    BTS patterns
    """)
with col3:
    st.info("""
    **Phase 3 — Regional Carrier Toolkit**
    Free open-source ML toolkit targeting
    regional operators like Peninsula Airways
    (15.6% cancellation rate) with zero
    ML infrastructure
    """)

st.markdown("""
<p class='source-text'>
    Built on BTS On-Time Performance Data (2015–2025) ·
    XGBoost · FastAPI · Streamlit · 
</p>
""", unsafe_allow_html=True)
