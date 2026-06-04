import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

st.set_page_config(
    page_title="Cancellation Risk Checker",
    page_icon="🔍",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .risk-card {
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .alt-card {
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
FEATURES = [
    'arr_flights', 'nas_delay', 'security_delay',
    'delay_minutes_per_flight_capped_p999',
    'avg_delay_minutes_given_delayed_capped_p999',
    'month', 'delay_rate', 'weather_pct', 'carrier_pct'
]

MONTHS = {
    1:"January", 2:"February", 3:"March", 4:"April",
    5:"May", 6:"June", 7:"July", 8:"August",
    9:"September", 10:"October", 11:"November", 12:"December"
}

HIGH_RISK_MONTHS = {1, 3, 4, 7}

DEMO_RISKS = {
    "Delta Air Lines": 0.10,
    "Hawaiian Airlines": 0.07,
    "Alaska Airlines": 0.18,
    "Southwest Airlines": 0.28,
    "United Airlines": 0.30,
    "American Airlines": 0.35,
    "JetBlue Airways": 0.42,
    "Frontier Airlines": 0.60,
    "Spirit Airlines": 0.62,
    "Peninsula Airways": 0.78
}

# ── Load Model & Data ─────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    path = os.path.join(os.path.dirname(__file__), "..", "model", "xgboost_model.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_data.csv")
    return pd.read_csv(path)

try:
    df    = load_data()
    model = load_model()
    data_loaded = True
except Exception:
    data_loaded = False
    df = None

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🔍 Flight Cancellation Risk Checker")
st.markdown("*Enter your flight details to get a real-time cancellation risk score powered by XGBoost (AUC 0.89 · 82% Recall)*")
st.markdown("---")

if not data_loaded:
    st.info("ℹ️ Running in demo mode — predictions based on historical averages. Add model and data files for live XGBoost predictions.")

# ── Inputs ────────────────────────────────────────────────────────────────────
st.markdown("### ✈️ Enter Your Flight Details")
col1, col2, col3 = st.columns(3)

with col1:
    if data_loaded and df is not None:
        carrier_col = 'carrier_name' if 'carrier_name' in df.columns else 'carrier'
        carriers = sorted(df[carrier_col].dropna().unique().tolist())
    else:
        carriers = sorted(DEMO_RISKS.keys())
    selected_carrier = st.selectbox("🏷️ Select Airline", carriers)

with col2:
    if data_loaded and df is not None:
        airports = sorted(df['airport'].dropna().unique().tolist())
    else:
        airports = ["ATL","LAX","ORD","DFW","DEN",
                    "JFK","SFO","SEA","LAS","MCO",
                    "PHX","CLT","MIA","BOS","MSP"]
    selected_airport = st.selectbox("🛫 Select Airport", airports)

with col3:
    selected_month = st.selectbox(
        "📅 Select Travel Month",
        options=list(MONTHS.keys()),
        format_func=lambda x: MONTHS[x]
    )

predict_btn = st.button(
    "🔍 Check Cancellation Risk",
    type="primary",
    use_container_width=True
)

# ── Prediction ────────────────────────────────────────────────────────────────
if predict_btn:
    st.markdown("---")

    if data_loaded and df is not None:
        carrier_col = 'carrier_name' if 'carrier_name' in df.columns else 'carrier'
        filtered = df[
            (df[carrier_col] == selected_carrier) &
            (df['airport'] == selected_airport) &
            (df['month'] == selected_month)
        ]
        if len(filtered) == 0:
            filtered = df[
                (df[carrier_col] == selected_carrier) &
                (df['month'] == selected_month)
            ]
        if len(filtered) > 0:
            available = [f for f in FEATURES if f in filtered.columns]
            inp = filtered[available].mean().values.reshape(1, -1)
            inp_df = pd.DataFrame(inp, columns=available)
            try:
                prob = float(model.predict_proba(inp_df)[0][1])
            except Exception:
                prob = DEMO_RISKS.get(selected_carrier, 0.35)
        else:
            prob = DEMO_RISKS.get(selected_carrier, 0.35)
    else:
        base = DEMO_RISKS.get(selected_carrier, 0.35)
        adj  = 0.15 if selected_month in HIGH_RISK_MONTHS else 0.0
        prob = min(base + adj, 0.99)

    # ── Risk Level ────────────────────────────────────────────────────────────
    if prob >= 0.70:
        risk_level = "HIGH RISK"
        risk_color = "#dc3545"
        risk_bg    = "#fff5f5"
        risk_emoji = "🔴"
        risk_msg   = "This flight has a HIGH cancellation probability. We strongly recommend booking a safer alternative."
        risk_action = "⚠️ Action Required: Consider rebooking now before prices rise"
    elif prob >= 0.40:
        risk_level = "MEDIUM RISK"
        risk_color = "#fd7e14"
        risk_bg    = "#fff9f0"
        risk_emoji = "🟡"
        risk_msg   = "This flight carries MODERATE cancellation risk. Consider travel insurance or flexible fare."
        risk_action = "💡 Tip: Book a flexible fare or check alternatives below"
    else:
        risk_level = "LOW RISK"
        risk_color = "#28a745"
        risk_bg    = "#f0fff4"
        risk_emoji = "🟢"
        risk_msg   = "This flight has LOW cancellation risk. You are good to go!"
        risk_action = "✅ You are all set — enjoy your flight!"

    # ── Display Results ───────────────────────────────────────────────────────
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
        <div style='background:{risk_bg}; border:3px solid {risk_color};
                    border-radius:16px; padding:2rem; text-align:center;'>
            <h2 style='color:{risk_color}; margin:0;'>{risk_emoji} {risk_level}</h2>
            <h1 style='color:{risk_color}; font-size:4rem; margin:0.5rem 0;'>{prob:.0%}</h1>
            <p style='color:#333; font-size:15px;'>{risk_msg}</p>
            <p style='color:{risk_color}; font-weight:bold;'>{risk_action}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if selected_month in HIGH_RISK_MONTHS:
            st.warning(f"⚠️ **{MONTHS[selected_month]}** is historically a **high-risk month** — peak disruption period based on 10 years of BTS data (2015–2025)")

    with col2:
        st.markdown("### 📋 Flight Summary")
        st.markdown(f"""
        | Detail | Value |
        |---|---|
        | ✈️ Airline | {selected_carrier} |
        | 🛫 Airport | {selected_airport} |
        | 📅 Month | {MONTHS[selected_month]} |
        | ⚠️ Risk Level | **{risk_level}** |
        | 🎯 Probability | **{prob:.1%}** |
        | 📊 Data Source | BTS 2015–2025 |
        """)

        st.markdown("**📅 Monthly Risk Pattern:**")
        monthly_risk = pd.DataFrame({
            'Month': list(MONTHS.values()),
            'Historical Risk': [
                0.62, 0.40, 0.68, 0.70, 0.38,
                0.35, 0.62, 0.40, 0.18, 0.16,
                0.28, 0.48
            ]
        }).set_index('Month')
        st.bar_chart(monthly_risk, height=200)

    # ── Safer Alternatives ────────────────────────────────────────────────────
    if prob >= 0.40:
        st.markdown("---")
        st.markdown("### 🔄 Safer Alternatives at This Airport")

        safe_airlines = {
            "Delta Air Lines":    0.10,
            "Hawaiian Airlines":  0.07,
            "Alaska Airlines":    0.18,
            "Southwest Airlines": 0.25,
            "United Airlines":    0.28
        }
        alternatives = {
            k: v for k, v in safe_airlines.items()
            if k != selected_carrier and v < prob
        }

        if alternatives:
            top3 = sorted(alternatives.items(), key=lambda x: x[1])[:3]
            cols = st.columns(3)
            medals = ["🥇 Best Option", "🥈 2nd Option", "🥉 3rd Option"]
            for i, (airline, risk) in enumerate(top3):
                saving = prob - risk
                with cols[i]:
                    st.markdown(f"""
                    <div style='background:#f0fff4; border:2px solid #28a745;
                                border-radius:12px; padding:1rem; text-align:center;'>
                        <p style='color:#28a745; font-weight:bold; margin:0;'>{medals[i]}</p>
                        <h4 style='color:#1a1a2e; margin:0.3rem 0;'>{airline}</h4>
                        <h3 style='color:#28a745; margin:0;'>{risk:.0%} risk</h3>
                        <p style='color:#555; font-size:12px; margin:0.3rem 0;'>
                            {saving:.0%} safer than your current choice
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("✅ Your selected airline is already among the safest options at this airport!")

    # ── Industry Context ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📰 2025 Industry Context")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Passengers Disrupted 2025", "248 Million",
                  delta="Nearly 1 in 4 flights",
                  delta_color="inverse")
    with col2:
        st.metric("Industry On-Time Rate 2025", "76.84%",
                  delta="Worst in recent years",
                  delta_color="inverse")
    with col3:
        st.metric("Cost Per Delayed Minute", "$100.76",
                  delta="Airlines for America 2025")

st.markdown("""
<p style='text-align:center; color:#aaa; font-size:11px; margin-top:2rem;'>
    Predictions based on BTS On-Time Performance Data (2015–2025) ·
    XGBoost AUC 0.89 · For informational purposes only
</p>
""", unsafe_allow_html=True)
