import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Delay Cause Breakdown",
    page_icon="📉",
    layout="wide"
)

# ── Constants ─────────────────────────────────────────────────────────────────
DELAY_COLS = {
    'carrier_delay':       '🏢 Carrier Delay',
    'weather_delay':       '🌩️ Weather Delay',
    'nas_delay':           '🗼 NAS Delay',
    'security_delay':      '🔒 Security Delay',
    'late_aircraft_delay': '✈️ Late Aircraft'
}

DELAY_COLORS  = ['#4361ee','#f77f00','#2dc653','#e63946','#9b5de5']
INDUSTRY_AVG  = {
    'carrier_delay': 35.0, 'weather_delay': 17.0,
    'nas_delay': 22.0, 'security_delay': 4.0,
    'late_aircraft_delay': 22.0
}

DESCRIPTIONS = {
    'carrier_delay':       'Delays caused directly by the airline — crew issues, maintenance, gate conflicts, fueling.',
    'weather_delay':       'Delays caused by significant meteorological conditions — storms, snow, fog.',
    'nas_delay':           'Delays caused by National Airspace System — heavy traffic, ATC decisions, airport operations.',
    'security_delay':      'Delays caused by security screening, terminal evacuations, or security breaches.',
    'late_aircraft_delay': 'Delays caused by the previous flight with the same aircraft arriving late — cascade effect.'
}

RECOMMENDATIONS = {
    'carrier_delay': {
        'action':   'Review crew scheduling efficiency, maintenance turnaround times, and gate management processes. Target buffer time reduction between rotations.',
        'priority': 'CRITICAL',
        'color':    '#dc3545'
    },
    'late_aircraft_delay': {
        'action':   'Add 15-20 minute rotation buffers on high-risk routes. Pre-position reserve aircraft at key hub airports during peak months (January, July).',
        'priority': 'HIGH',
        'color':    '#fd7e14'
    },
    'weather_delay': {
        'action':   'Implement weather-aware scheduling with proactive rebooking triggers 24-48 hours before severe weather events.',
        'priority': 'MEDIUM',
        'color':    '#f4a261'
    },
    'nas_delay': {
        'action':   'Optimize slot timing at congested airports. Coordinate with ATC for preferred routing during peak traffic hours.',
        'priority': 'MEDIUM',
        'color':    '#f4a261'
    },
    'security_delay': {
        'action':   'Coordinate with TSA for additional staffing during peak travel periods. Review passenger flow at security checkpoints.',
        'priority': 'LOW',
        'color':    '#2dc653'
    }
}

DEMO_DATA = {
    "American Airlines":  [38, 18, 22, 4, 18],
    "Delta Air Lines":    [28, 15, 25, 3, 29],
    "United Airlines":    [33, 20, 24, 5, 18],
    "Southwest Airlines": [42, 12, 20, 3, 23],
    "Alaska Airlines":    [30, 22, 21, 4, 23],
    "JetBlue Airways":    [35, 16, 23, 4, 22],
    "Spirit Airlines":    [45, 14, 19, 3, 19],
    "Frontier Airlines":  [44, 13, 20, 4, 19],
    "Peninsula Airways":  [50, 10, 18, 3, 19],
    "SkyWest Airlines":   [31, 19, 22, 4, 24],
}

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_data.csv")
    return pd.read_csv(path)

try:
    df = load_data()
    data_loaded = True
except Exception:
    data_loaded = False
    df = None

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 📉 Airline Delay Cause Breakdown")
st.markdown("*Select any carrier to see a full breakdown of delay causes — with the biggest driver flagged for immediate OCC action*")
st.markdown("---")

if not data_loaded:
    st.info("ℹ️ Running in demo mode — showing representative delay patterns based on BTS historical data.")

# ── Carrier Select ────────────────────────────────────────────────────────────
st.markdown("### 🏷️ Select Airline to Analyze")
col1, col2 = st.columns([2, 1])

with col1:
    if data_loaded and df is not None:
        carrier_col = 'carrier_name' if 'carrier_name' in df.columns else 'carrier'
        carriers = sorted(df[carrier_col].dropna().unique().tolist())
    else:
        carriers = sorted(DEMO_DATA.keys())
    selected_carrier = st.selectbox("Choose an airline:", carriers)

with col2:
    selected_year = st.selectbox(
        "Filter by year (optional):",
        ["All Years", "2024", "2023", "2022", "2021", "2020", "2019"]
    )

analyze_btn = st.button(
    "📊 Analyze Delay Causes",
    type="primary",
    use_container_width=True
)

if analyze_btn:
    st.markdown("---")

    # ── Get Delay Data ────────────────────────────────────────────────────────
    if data_loaded and df is not None:
        carrier_col = 'carrier_name' if 'carrier_name' in df.columns else 'carrier'
        cdf = df[df[carrier_col] == selected_carrier].copy()

        if selected_year != "All Years" and 'year' in cdf.columns:
            cdf = cdf[cdf['year'] == int(selected_year)]

        available = [c for c in DELAY_COLS.keys() if c in cdf.columns]
        if available and len(cdf) > 0:
            totals = cdf[available].sum()
            total  = totals.sum()
            delay_pct = (totals / total * 100).round(1) if total > 0 else totals
            biggest   = delay_pct.idxmax()
        else:
            data_loaded = False

    if not data_loaded or df is None:
        vals = DEMO_DATA.get(selected_carrier, DEMO_DATA["American Airlines"])
        delay_pct = pd.Series(vals, index=list(DELAY_COLS.keys()))
        biggest   = delay_pct.idxmax()

    # ── KPI Row ───────────────────────────────────────────────────────────────
    st.markdown(f"### 📊 Delay Profile — {selected_carrier}")
    cols = st.columns(5)
    for i, (key, label) in enumerate(DELAY_COLS.items()):
        val = delay_pct.get(key, 0)
        avg = INDUSTRY_AVG.get(key, 0)
        delta_val = val - avg
        with cols[i]:
            st.metric(
                label=label,
                value=f"{val:.1f}%",
                delta=f"{delta_val:+.1f}% vs industry",
                delta_color="inverse"
            )

    st.markdown("---")

    # ── Biggest Driver Alert ──────────────────────────────────────────────────
    driver_label = DELAY_COLS.get(biggest, biggest)
    driver_pct   = delay_pct[biggest]
    driver_desc  = DESCRIPTIONS.get(biggest, "")
    rec          = RECOMMENDATIONS.get(biggest, RECOMMENDATIONS['carrier_delay'])

    st.markdown(f"""
    <div style='background:{rec["color"]}15; border:3px solid {rec["color"]};
                border-radius:12px; padding:1.5rem; margin-bottom:1rem;'>
        <h3 style='color:{rec["color"]}; margin:0;'>
            🚨 Biggest Delay Driver — {driver_label}: {driver_pct:.1f}%
        </h3>
        <p style='color:#555; margin:0.5rem 0;'>{driver_desc}</p>
        <p style='color:{rec["color"]}; font-weight:bold; margin:0;'>
            Priority: {rec["priority"]} · OCC Action: {rec["action"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    labels = [DELAY_COLS[k] for k in delay_pct.index if k in DELAY_COLS]
    values = list(delay_pct.values)
    colors = DELAY_COLORS[:len(labels)]

    with col1:
        st.markdown("#### 📊 Delay Cause Distribution")
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.barh(labels, values, color=colors, edgecolor='white', height=0.6)
        ax.bar_label(bars, fmt='%.1f%%', padding=5, fontsize=10)
        ax.set_xlabel("% of Total Delay Minutes", fontsize=11)
        ax.set_title(f"Delay Causes — {selected_carrier}", fontweight='bold', fontsize=12)
        ax.set_xlim(0, max(values) * 1.25)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("#### 📏 vs Industry Average")
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        x    = np.arange(len(labels))
        w    = 0.35
        b1   = ax2.bar(x - w/2, values,
                       w, color=colors, alpha=0.9, label=selected_carrier)
        b2   = ax2.bar(x + w/2,
                       [INDUSTRY_AVG.get(k, 0) for k in delay_pct.index],
                       w, color='#cccccc', alpha=0.9, label='Industry Average')
        ax2.set_xticks(x)
        ax2.set_xticklabels(labels, rotation=15, ha='right', fontsize=8)
        ax2.set_ylabel("% of Total Delay Minutes")
        ax2.set_title("Carrier vs Industry Average", fontweight='bold', fontsize=12)
        ax2.legend(fontsize=9)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # ── All Airlines Comparison ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔍 How Does This Carrier Compare to All Others?")

    compare_data = []
    for airline, vals in DEMO_DATA.items():
        compare_data.append({
            'Airline': airline,
            'Carrier %': vals[0],
            'Weather %': vals[1],
            'NAS %':     vals[2],
            'Security %':vals[3],
            'Late AC %': vals[4]
        })
    compare_df = pd.DataFrame(compare_data).set_index('Airline')

    def highlight_selected(row):
        if row.name == selected_carrier:
            return ['background-color: #fff3cd'] * len(row)
        return [''] * len(row)

    st.dataframe(
        compare_df.style.apply(highlight_selected, axis=1),
        use_container_width=True
    )
    st.caption(f"🟡 Highlighted row = {selected_carrier}")

st.markdown("""
<p style='text-align:center; color:#aaa; font-size:11px; margin-top:2rem;'>
    Based on BTS On-Time Performance Data (2015–2025) · For OCC Decision Support Only
</p>
""", unsafe_allow_html=True)
