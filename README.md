# ✈️ AeroRisk Intelligence Platform
### Flight Cancellation Prediction & Carrier Benchmarking System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aerorisk-sgj8edbw5sfz3urjaqzpnk.streamlit.app)

---

## 🚨 2025 Aviation Crisis
- **248 million passengers** disrupted in 2025 *(AirHelp 2025)*
- **76.84%** average on-time performance — worst in recent years *(BTS via Kiplinger 2026)*
- **$30B–$34B** annual flight disruption cost *(DOT + FAA/Nextor)*

## 📌 Problem Statement
No major booking platform offers ML-based cancellation risk scoring at point of purchase.
AeroRisk fills this gap using 10 years of publicly available BTS flight data.

## 🛠️ Three Decision Tools

| Tool | User | What it does |
|---|---|---|
| 🔍 Cancellation Risk Checker | Passengers | XGBoost risk score + safer alternatives |
| 📉 Delay Cause Breakdown | OCC Teams | Root cause attribution + OCC action |
| 🏆 Safest Airline Recommender | Airport Analysts | Normalized safety ranking by station |

## 📊 Key Findings
- **220,000+** BTS flight records analyzed (2015–2025)
- **73%** of U.S. flight delays are airline-caused — not weather
- **26x** cancellation gap — Delta (0.6%) vs Peninsula Airways (15.6%)
- **XGBoost AUC 0.89** · 82% recall · 8,016 high-risk flights flagged

## ⚙️ Setup

### 1. Add your files:
```
model/xgboost_model.pkl    ← your trained XGBoost model
data/cleaned_data.csv      ← your cleaned BTS dataset
```

### 2. Install and run:
```bash
pip install -r requirements.txt
streamlit run Home.py
```

## 🗂️ Project Structure
```
aerorisk/
├── Home.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── model/
│   └── xgboost_model.pkl
├── data/
│   └── cleaned_data.csv
└── pages/
    ├── 1_Cancellation_Risk_Checker.py
    ├── 2_Delay_Cause_Breakdown.py
    └── 3_Safest_Airline_Recommender.py
```

## 🚀 Future Roadmap
- [ ] Amadeus Flight API integration — risk scores at point of booking
- [ ] Real-time AviationStack API for live predictions
- [ ] Twilio SMS alerts for high-risk passengers
- [ ] MLOps pipeline with automated quarterly retraining

## 🔧 Tech Stack
Python · Pandas · NumPy · Scikit-learn · XGBoost · SHAP · Streamlit · Microsoft Azure · BTS Database

## 🎓 Author
MS Business Analytics — University of North Texas
Built on BTS On-Time Performance Data (2015–2025)

## 📚 Sources
- AirHelp 2025 USA Flight Disruption Report
- BTS On-Time Performance Database (transtats.bts.gov)
- DOT Air Travel Consumer Report Full Year 2024
- Airlines for America 2025 Delay Cost Report
- Flighty Global Passport Report 2025
- U.S. PIRG Plane Truth 2025 Report
