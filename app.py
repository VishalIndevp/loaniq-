import streamlit as st
import pandas as pd
import joblib

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LoanIQ · Approval Predictor",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────
#  FIX TOP PADDING (CSS only - works on Streamlit Cloud)
# ─────────────────────────────────────────────
st.markdown("""
<style>
.css-18e3th9 { padding-top: 0 !important; }
.css-1d391kg { padding-top: 0 !important; }
.css-z5fcl4  { padding-top: 1rem !important; }
.css-1y4p8pa { padding-top: 0 !important; }
[data-testid="stHeader"] { background: transparent !important; border: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
.stDeployButton { display: none !important; }
/* Make the native sidebar toggle always visible and styled */
[data-testid="collapsedControl"] {
    position: fixed !important;
    top: 0.5rem !important;
    left: 0.5rem !important;
    z-index: 999999 !important;
    background: #111827 !important;
    border: 1px solid #00d4a1 !important;
    border-radius: 8px !important;
    width: 2.2rem !important;
    height: 2.2rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 16px rgba(0,212,161,0.3) !important;
    color: #00d4a1 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
[data-testid="collapsedControl"]:hover {
    background: #1a2235 !important;
    box-shadow: 0 4px 24px rgba(0,212,161,0.5) !important;
    transform: scale(1.1) !important;
}
[data-testid="collapsedControl"] svg { color: #00d4a1 !important; fill: #00d4a1 !important; }

/* ── Native sidebar open/close arrow button ── */
/* The < button inside the open sidebar */
[data-testid="stSidebar"] button[kind="header"],
[data-testid="stSidebar"] [data-testid="baseButton-header"] {
    position: fixed !important;
    top: 0.6rem !important;
    right: -1rem !important;
    z-index: 999999 !important;
    background: #111827 !important;
    border: 1px solid #00d4a1 !important;
    border-radius: 8px !important;
    color: #00d4a1 !important;
    width: 2.2rem !important;
    height: 2.2rem !important;
    box-shadow: 0 4px 16px rgba(0,212,161,0.3) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] button[kind="header"]:hover,
[data-testid="stSidebar"] [data-testid="baseButton-header"]:hover {
    background: #1a2235 !important;
    box-shadow: 0 4px 24px rgba(0,212,161,0.5) !important;
}

/* The >> button when sidebar is collapsed */
[data-testid="collapsedControl"] button,
[data-testid="collapsedControl"] [data-testid="baseButton-header"] {
    background: #111827 !important;
    border: 1px solid #00d4a1 !important;
    border-radius: 8px !important;
    color: #00d4a1 !important;
    width: 2.2rem !important;
    height: 2.2rem !important;
    box-shadow: 0 4px 16px rgba(0,212,161,0.4) !important;
    transition: all 0.2s ease !important;
}
[data-testid="collapsedControl"] button:hover {
    background: #1a2235 !important;
    box-shadow: 0 4px 24px rgba(0,212,161,0.6) !important;
    transform: scale(1.12) !important;
}
[data-testid="collapsedControl"] svg,
[data-testid="stSidebar"] button[kind="header"] svg {
    color: #00d4a1 !important;
    fill: #00d4a1 !important;
    width: 1rem !important;
    height: 1rem !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root variables ── */
:root {
    --bg:          #0b0f1a;
    --surface:     #111827;
    --surface2:    #1a2235;
    --border:      #1e2d45;
    --accent:      #00d4a1;
    --accent2:     #0ea5e9;
    --danger:      #f43f5e;
    --text:        #e2e8f0;
    --muted:       #64748b;
    --gold:        #f5c518;
}

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Remove top black space – keep sidebar toggle visible ── */
#root > div:nth-child(1) > div > div > div > div > section > div { padding-top: 0rem !important; }

/* Hide header bar but KEEP the sidebar toggle button */
[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
    height: 0px !important;
    min-height: 0px !important;
    overflow: visible !important;
}
/* Hide decorative elements inside header */
[data-testid="stDecoration"]   { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
.stDeployButton                { display: none !important; }
[data-testid="stToolbar"]      { display: none !important; }

/* Make sidebar collapse button always visible and styled */
[data-testid="collapsedControl"] {
    display: flex !important;
    top: 1rem !important;
    background: #111827 !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 50% !important;
    width: 2rem !important;
    height: 2rem !important;
    align-items: center !important;
    justify-content: center !important;
    color: #00d4a1 !important;
    box-shadow: 0 4px 12px rgba(0,212,161,0.2) !important;
    transition: all 0.2s ease !important;
    z-index: 9999 !important;
}
[data-testid="collapsedControl"]:hover {
    background: #1a2235 !important;
    border-color: #00d4a1 !important;
    box-shadow: 0 4px 20px rgba(0,212,161,0.4) !important;
    transform: scale(1.1) !important;
}

/* Sidebar expand button (the >> arrow when collapsed) */
button[kind="header"] {
    background: #111827 !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 50% !important;
    color: #00d4a1 !important;
}

div[data-testid="stAppViewContainer"] > section > div.block-container { padding-top: 1rem !important; }

/* ── Main container ── */
.main .block-container {
    padding: 1rem 3rem 4rem 3rem !important;
    max-width: 1100px;
    margin-top: 0 !important;
}

/* ── MOBILE RESPONSIVE ── */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 1rem 3rem 1rem !important;
    }
    .hero-wrap {
        padding: 1.6rem 1.4rem !important;
        border-radius: 14px !important;
    }
    .hero-title {
        font-size: 1.8rem !important;
    }
    .hero-sub {
        font-size: 0.85rem !important;
    }
    .hero-badge {
        font-size: 0.65rem !important;
        padding: 3px 10px !important;
    }
    .cards-row {
        grid-template-columns: 1fr !important;
        gap: 0.7rem !important;
        margin-bottom: 1.2rem !important;
    }
    .card {
        padding: 1rem 1.1rem !important;
    }
    .card-value {
        font-size: 1.15rem !important;
    }
    .profile-grid {
        grid-template-columns: 1fr !important;
        gap: 0.45rem !important;
    }
    .profile-row {
        padding: 0.5rem 0.75rem !important;
    }
    .section-label {
        font-size: 0.65rem !important;
        letter-spacing: 0.1em !important;
    }
    .result-approved, .result-rejected {
        padding: 1.4rem 1rem !important;
        border-radius: 12px !important;
    }
    .result-title {
        font-size: 1.6rem !important;
    }
    .footer-wrap {
        padding: 2rem 1rem 1.5rem 1rem !important;
    }
    .footer-tagline {
        font-size: 0.95rem !important;
    }
    .footer-socials {
        gap: 0.6rem !important;
        flex-wrap: wrap !important;
    }
    .social-btn {
        padding: 0.45rem 0.85rem !important;
        font-size: 0.72rem !important;
    }
    .footer-copy {
        font-size: 0.63rem !important;
        line-height: 1.8 !important;
        letter-spacing: 0.04em !important;
    }
}
@media (max-width: 480px) {
    .hero-title { font-size: 1.45rem !important; }
    .footer-socials {
        flex-direction: column !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }
    .social-btn {
        width: 190px !important;
        justify-content: center !important;
    }
    .cards-row {
        grid-template-columns: 1fr !important;
    }
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stNumberInput label {
    font-size: 0.78rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted) !important;
}

/* Sidebar inputs */
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stNumberInput input,
section[data-testid="stSidebar"] .stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Slider accent */
section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
    background: var(--accent) !important;
    color: #000 !important;
}
section[data-testid="stSidebar"] .stSlider [role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* ── Hero header ── */
.hero-wrap {
    background: linear-gradient(135deg, #0f1f35 0%, #0b1628 60%, #0f1a2e 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.4s ease, box-shadow 0.4s ease;
}
.hero-wrap:hover {
    border-color: rgba(0,212,161,0.3);
    box-shadow: 0 8px 48px rgba(0,212,161,0.08), inset 0 0 80px rgba(0,212,161,0.03);
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(0,212,161,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(14,165,233,0.09) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,212,161,0.12);
    border: 1px solid rgba(0,212,161,0.3);
    color: var(--accent) !important;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 100px;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 900;
    line-height: 1.1;
    margin: 0 0 0.6rem 0;
    background: linear-gradient(135deg, #ffffff 30%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: var(--muted) !important;
    font-size: 1rem;
    font-weight: 300;
    margin: 0;
}

/* ── Result box ── */
.result-approved {
    background: linear-gradient(135deg, rgba(0,212,161,0.1) 0%, rgba(0,212,161,0.03) 100%);
    border: 1px solid var(--accent);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    animation: fadeSlideUp 0.5s ease forwards;
}
.result-rejected {
    background: linear-gradient(135deg, rgba(244,63,94,0.1) 0%, rgba(244,63,94,0.03) 100%);
    border: 1px solid var(--danger);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    animation: fadeSlideUp 0.5s ease forwards;
}
.result-approved:hover {
    box-shadow: 0 0 40px rgba(0,212,161,0.2), 0 8px 32px rgba(0,0,0,0.3);
    transform: translateY(-2px);
}
.result-rejected:hover {
    box-shadow: 0 0 40px rgba(244,63,94,0.2), 0 8px 32px rgba(0,0,0,0.3);
    transform: translateY(-2px);
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Sidebar input hover glow */
section[data-testid="stSidebar"] .stSelectbox > div > div:hover,
section[data-testid="stSidebar"] .stNumberInput input:hover,
section[data-testid="stSidebar"] .stNumberInput input:focus {
    border-color: rgba(0,212,161,0.5) !important;
    box-shadow: 0 0 0 2px rgba(0,212,161,0.1) !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}

/* ── Result shared styles ── */
.result-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 900;
    margin-bottom: 0.4rem;
}
.result-approved .result-title { color: var(--accent) !important; }
.result-rejected .result-title { color: var(--danger) !important; }
.result-conf {
    font-size: 0.9rem;
    color: var(--muted) !important;
    margin-bottom: 1.2rem;
}
.conf-bar-wrap {
    background: var(--border);
    border-radius: 100px;
    height: 8px;
    width: 100%;
    margin: 0.6rem 0 1rem 0;
    overflow: hidden;
}
.conf-bar-fill-green {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, var(--accent2), var(--accent));
    animation: barGrow 1s ease forwards;
}
.conf-bar-fill-red {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #f97316, var(--danger));
    animation: barGrow 1s ease forwards;
}
@keyframes barGrow {
    from { width: 0% !important; }
}

/* ── Profile summary ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent) !important;
    margin-bottom: 1rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
    position: relative;
    overflow: hidden;
}
.section-label::after {
    content: '';
    position: absolute;
    bottom: 0; left: -100%;
    width: 100%; height: 1px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: left 0.4s ease;
}
.section-label:hover::after { left: 0; }

/* ── Summary cards ── */
.cards-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
    cursor: default;
}
.card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at var(--mx, 50%) var(--my, 50%), rgba(0,212,161,0.07) 0%, transparent 65%);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}
.card:hover {
    border-color: var(--accent);
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 40px rgba(0,212,161,0.15), 0 2px 8px rgba(0,0,0,0.4);
    background: #131f33;
}
.card:hover::after { opacity: 1; }
.card-accent:hover { box-shadow: 0 12px 40px rgba(0,212,161,0.2), 0 2px 8px rgba(0,0,0,0.4); }
.card-blue:hover   { border-color: var(--accent2) !important; box-shadow: 0 12px 40px rgba(14,165,233,0.2), 0 2px 8px rgba(0,0,0,0.4); }
.card-gold:hover   { border-color: var(--gold) !important; box-shadow: 0 12px 40px rgba(245,197,24,0.2), 0 2px 8px rgba(0,0,0,0.4); }
.card-icon {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
    transition: transform 0.3s ease;
    display: inline-block;
}
.card:hover .card-icon { transform: scale(1.2) rotate(-5deg); }
.card-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted) !important;
    margin-bottom: 0.25rem;
}
.card-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text) !important;
    transition: color 0.3s ease;
}
.card-accent:hover .card-value { color: var(--accent) !important; }
.card-blue:hover   .card-value { color: var(--accent2) !important; }
.card-gold:hover   .card-value { color: var(--gold) !important; }
.card-accent { border-top: 3px solid var(--accent); }
.card-blue   { border-top: 3px solid var(--accent2); }
.card-gold   { border-top: 3px solid var(--gold); }

/* ── Predict button ── */
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 4px 24px rgba(0,212,161,0.25); }
    50%       { box-shadow: 0 4px 36px rgba(0,212,161,0.5), 0 0 0 6px rgba(0,212,161,0.08); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--accent) 0%, #00b087 100%) !important;
    color: #000 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 24px rgba(0,212,161,0.25) !important;
    margin-top: 0.5rem !important;
    animation: pulse-glow 2.5s ease-in-out infinite !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
    background: linear-gradient(105deg, transparent 30%, rgba(255,255,255,0.25) 50%, transparent 70%) !important;
    background-size: 200% auto !important;
    opacity: 0 !important;
    transition: opacity 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 10px 40px rgba(0,212,161,0.45), 0 0 0 4px rgba(0,212,161,0.12) !important;
    animation: none !important;
    background: linear-gradient(135deg, #00edb4 0%, #00c99a 100%) !important;
}
.stButton > button:hover::before {
    opacity: 1 !important;
    animation: shimmer 0.6s linear !important;
}
.stButton > button:active {
    transform: translateY(0px) scale(0.99) !important;
    box-shadow: 0 4px 16px rgba(0,212,161,0.3) !important;
}

/* ── Risk meter ── */
.risk-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem;
    margin-top: 1.5rem;
}
.profile-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.6rem;
}
.profile-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 0.55rem 0.9rem;
    transition: border-color 0.2s ease, background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
}
.profile-row:hover {
    border-color: rgba(0,212,161,0.4);
    background: #1e2d42;
    transform: translateX(3px);
    box-shadow: -3px 0 0 var(--accent), 0 2px 12px rgba(0,0,0,0.3);
}
.profile-row:hover .profile-key { color: var(--accent) !important; }
.profile-row:hover .profile-val  { color: #fff !important; }
.profile-key {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    transition: color 0.2s ease;
}
.profile-val {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text) !important;
    transition: color 0.2s ease;
}

/* ── Risk meter ── */
.risk-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem;
    margin-top: 1.5rem;
}

/* ── Sidebar section divider ── */
.sidebar-section {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent) !important;
    padding: 0.8rem 0 0.3rem 0;
    border-top: 1px solid var(--border);
    margin-top: 0.8rem;
}

/* ── Streamlit overrides ── */
div[data-testid="stMetric"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
div[data-testid="stMetric"] label { color: var(--muted) !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: var(--accent) !important; }

/* scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD MODEL FILES
# ─────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model         = joblib.load("model_XGB.pkl")
    scaler        = joblib.load("scaler.pkl")
    model_columns = joblib.load("model_columns.pkl")
    return model, scaler, model_columns

model, scaler, model_columns = load_artifacts()

num_cols = ['Age','Annual_Income','Co_Applicant_Income',
            'Savings_Balance','Existing_Loans','Loan_Amount','Loan_Term']

# ─────────────────────────────────────────────
#  SIDEBAR  –  APPLICANT DETAILS
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div style="padding:1rem 0 0.5rem 0;">'
                '<span style="font-family:Playfair Display,serif;font-size:1.4rem;'
                'font-weight:900;background:linear-gradient(135deg,#fff 30%,#00d4a1 100%);'
                '-webkit-background-clip:text;-webkit-text-fill-color:transparent;">'
                'LoanIQ</span>'
                '<span style="font-size:0.7rem;color:#64748b;display:block;'
                'letter-spacing:.12em;text-transform:uppercase;margin-top:2px;">'
                'Applicant Profile</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Personal</div>', unsafe_allow_html=True)
    Gender         = st.selectbox("Gender",          ["Female","Male"])
    Age            = st.slider   ("Age",              18, 70, 30)
    Education      = st.selectbox("Education",        ["Graduate","Not Graduate","Undergraduate"])
    Marital_Status = st.selectbox("Marital Status",   ["Single","Married","Divorced"])

    st.markdown('<div class="sidebar-section">Employment & Income</div>', unsafe_allow_html=True)
    Employment_Status  = st.selectbox("Employment Status", ["Employed","Self-employed","Unemployed"])
    Annual_Income      = st.number_input("Annual Income (₹)",       0, 10_000_000, 300_000, step=10_000)
    Co_Applicant_Income= st.number_input("Co-Applicant Income (₹)", 0, 10_000_000, 0,       step=10_000)
    Savings_Balance    = st.number_input("Savings Balance (₹)",     0, 10_000_000, 50_000,  step=5_000)
    Existing_Loans     = st.slider("Existing Loans", 0, 10, 0)

    st.markdown('<div class="sidebar-section">Location & Property</div>', unsafe_allow_html=True)
    State = st.selectbox("State", sorted([
        'Bihar','Madhya Pradesh','Uttar Pradesh','Meghalaya','Gujarat',
        'Puducherry','Haryana','Maharashtra','Chhattisgarh','Sikkim',
        'Ladakh','Jharkhand','Tripura','Dadra and Nagar Haveli and Daman and Diu',
        'Tamil Nadu','Uttarakhand','Punjab','Mizoram','Andhra Pradesh','Nagaland',
        'Rajasthan','Himachal Pradesh','Arunachal Pradesh','Odisha','Telangana',
        'Karnataka','Delhi','Chandigarh','Jammu and Kashmir','Assam',
        'West Bengal','Kerala','Manipur','Lakshadweep','Goa',
        'Andaman and Nicobar Islands'
    ]))
    Home_Ownership = st.selectbox("Home Ownership", ["Rent","Own","Family"])
    Property_Area  = st.selectbox("Property Area",  ["Urban","Semiurban","Rural"])

    st.markdown('<div class="sidebar-section">Loan Details</div>', unsafe_allow_html=True)
    Loan_Types = st.selectbox("Loan Type", [
        'Home Loan','Car Loan / Vehicle Loan','Education Loan','Gold Loan',
        'Travel Loan','Business Loan','Personal Loan','Startup Loan',
        'Consumer Durable Loan','Credit Card Loan','Farm Equipment Loan',
        'Wedding Loan','Medical Loan'
    ])
    Loan_Amount    = st.number_input("Loan Amount (₹)",   0, 10_000_000, 200_000, step=10_000)
    Loan_Term      = st.slider("Loan Term (months)",       6, 480, 120, step=6)
    Mortgage       = st.selectbox("Mortgage Type", [
        'Land/Plot','Car / Vehicle','Agricultural Land','Gold','Home','House',
        'Commercial Property','Apartment/Flat','Other','Vehicle',
        'Fixed Deposit','Farm Equipment'
    ])
    Credit_History = st.selectbox("Credit History", ["Bad","Good"])

# ─────────────────────────────────────────────
#  MAIN CONTENT
# ─────────────────────────────────────────────

# Topbar + Hero
st.markdown(f"""
<style>
.topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.5rem;
    background: rgba(11,15,26,0.95);
    border-bottom: 1px solid #1e2d45;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    margin-bottom: 1.5rem;
    border-radius: 14px;
    position: relative;
    overflow: hidden;
}}
.topbar::before {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #00d4a1, #0ea5e9, transparent);
}}
.topbar-left {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}
.topbar-logo {{
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #fff 30%, #00d4a1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}}
.topbar-divider {{
    width: 1px;
    height: 20px;
    background: #1e2d45;
}}
.topbar-tagline {{
    font-size: 0.72rem;
    color: #64748b;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 500;
}}
.topbar-right {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
}}
.topbar-pill {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.75rem;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    transition: all 0.25s ease;
    cursor: default;
}}
.topbar-pill.model {{
    background: rgba(0,212,161,0.1);
    border: 1px solid rgba(0,212,161,0.25);
    color: #00d4a1;
}}
.topbar-pill.model:hover {{
    background: rgba(0,212,161,0.18);
    box-shadow: 0 0 16px rgba(0,212,161,0.2);
    transform: translateY(-1px);
}}
.topbar-pill.accuracy {{
    background: rgba(245,197,24,0.1);
    border: 1px solid rgba(245,197,24,0.25);
    color: #f5c518;
}}
.topbar-pill.accuracy:hover {{
    background: rgba(245,197,24,0.18);
    box-shadow: 0 0 16px rgba(245,197,24,0.2);
    transform: translateY(-1px);
}}
.topbar-pill.live {{
    background: rgba(14,165,233,0.1);
    border: 1px solid rgba(14,165,233,0.25);
    color: #0ea5e9;
}}
.topbar-dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00d4a1;
    animation: blink 1.5s ease-in-out infinite;
    display: inline-block;
}}
@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50%       {{ opacity: 0.2; }}
}}
@media (max-width: 600px) {{
    .topbar-tagline {{ display: none; }}
    .topbar-divider  {{ display: none; }}
    .topbar-pill.live {{ display: none; }}
}}
</style>

<div class="topbar">
  <div class="topbar-left">
    <span class="topbar-logo">LoanIQ</span>
    <div class="topbar-divider"></div>
    <span class="topbar-tagline">Credit Decision Engine</span>
  </div>
  <div class="topbar-right">
    <span class="topbar-pill model">⚡ XGBoost</span>
    <span class="topbar-pill accuracy">🎯 84.44% Accuracy</span>
    <span class="topbar-pill live"><span class="topbar-dot"></span>&nbsp;Live</span>
  </div>
</div>

<div class="hero-wrap">
  <div class="hero-badge">✦ AI-Powered Decision Engine</div>
  <h1 class="hero-title">Loan Approval<br>Predictor</h1>
  <p class="hero-sub">Instant credit decisions powered by XGBoost · Trained on real applicant data</p>
</div>
""", unsafe_allow_html=True)

# Summary cards
emi_est = round((Loan_Amount * 0.009), 0)  # rough estimate
dti     = round((Loan_Amount / Annual_Income * 100), 1) if Annual_Income > 0 else 0
total_income = Annual_Income + Co_Applicant_Income

st.markdown(f"""
<div class="cards-row">
  <div class="card card-accent">
    <div class="card-icon">💼</div>
    <div class="card-label">Total Household Income</div>
    <div class="card-value">₹{total_income:,.0f}</div>
  </div>
  <div class="card card-blue">
    <div class="card-icon">📊</div>
    <div class="card-label">Debt-to-Income Ratio</div>
    <div class="card-value">{dti}%</div>
  </div>
  <div class="card card-gold">
    <div class="card-icon">📅</div>
    <div class="card-label">Est. Monthly EMI</div>
    <div class="card-value">₹{emi_est:,.0f}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Two-column layout
col_left, col_right = st.columns([1.1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-label">Applicant Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="profile-grid">
      <div class="profile-row"><span class="profile-key">Name Status</span><span class="profile-val">{Gender} · {Age} yrs</span></div>
      <div class="profile-row"><span class="profile-key">Education</span><span class="profile-val">{Education}</span></div>
      <div class="profile-row"><span class="profile-key">Marital</span><span class="profile-val">{Marital_Status}</span></div>
      <div class="profile-row"><span class="profile-key">Employment</span><span class="profile-val">{Employment_Status}</span></div>
      <div class="profile-row"><span class="profile-key">State</span><span class="profile-val">{State}</span></div>
      <div class="profile-row"><span class="profile-key">Area</span><span class="profile-val">{Property_Area}</span></div>
      <div class="profile-row"><span class="profile-key">Home</span><span class="profile-val">{Home_Ownership}</span></div>
      <div class="profile-row"><span class="profile-key">Credit</span><span class="profile-val">{Credit_History}</span></div>
      <div class="profile-row"><span class="profile-key">Loan Type</span><span class="profile-val">{Loan_Types}</span></div>
      <div class="profile-row"><span class="profile-key">Mortgage</span><span class="profile-val">{Mortgage}</span></div>
      <div class="profile-row"><span class="profile-key">Loan Amount</span><span class="profile-val">₹{Loan_Amount:,.0f}</span></div>
      <div class="profile-row"><span class="profile-key">Term</span><span class="profile-val">{Loan_Term} months</span></div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-label">Decision Engine</div>', unsafe_allow_html=True)

    predict_btn = st.button("⚡  Run Credit Assessment", use_container_width=True)

    if predict_btn:
        # Build dataframe
        input_data = pd.DataFrame({
            'Gender':[Gender],'Age':[Age],'Education':[Education],
            'Marital_Status':[Marital_Status],'Employment_Status':[Employment_Status],
            'Annual_Income':[Annual_Income],'Co_Applicant_Income':[Co_Applicant_Income],
            'State':[State],'Loan_Types':[Loan_Types],'Savings_Balance':[Savings_Balance],
            'Existing_Loans':[Existing_Loans],'Home_Ownership':[Home_Ownership],
            'Mortgage':[Mortgage],'Loan_Amount':[Loan_Amount],'Loan_Term':[Loan_Term],
            'Credit_History':[Credit_History],'Property_Area':[Property_Area]
        })

        input_encoded = pd.get_dummies(input_data,
            columns=['Gender','Education','Marital_Status','Employment_Status',
                     'State','Loan_Types','Home_Ownership','Mortgage',
                     'Credit_History','Property_Area'],
            drop_first=True)

        input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
        input_encoded[num_cols] = scaler.transform(input_encoded[num_cols])

        prediction = model.predict(input_encoded)[0]
        prob       = model.predict_proba(input_encoded)[0][1]
        conf_pct   = prob * 100

        if prediction == 1:
            fill_class = "conf-bar-fill-green"
            st.markdown(f"""
            <div class="result-approved">
              <div style="font-size:2.5rem;margin-bottom:.5rem;">✅</div>
              <div class="result-title">Approved</div>
              <div class="result-conf">Model confidence: <strong style="color:#00d4a1">{conf_pct:.1f}%</strong></div>
              <div class="conf-bar-wrap">
                <div class="{fill_class}" style="width:{conf_pct:.1f}%"></div>
              </div>
              <div style="font-size:.82rem;color:#64748b;">
                This application meets the credit criteria based on income,<br>
                loan parameters, and applicant profile.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            fill_class = "conf-bar-fill-red"
            reject_conf = (1 - prob) * 100
            st.markdown(f"""
            <div class="result-rejected">
              <div style="font-size:2.5rem;margin-bottom:.5rem;">❌</div>
              <div class="result-title">Rejected</div>
              <div class="result-conf">Rejection confidence: <strong style="color:#f43f5e">{reject_conf:.1f}%</strong></div>
              <div class="conf-bar-wrap">
                <div class="{fill_class}" style="width:{reject_conf:.1f}%"></div>
              </div>
              <div style="font-size:.82rem;color:#64748b;">
                This application does not meet current approval criteria.<br>
                Consider improving savings, reducing existing loans, or credit history.
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Risk indicators
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Risk Indicators</div>', unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        dti_risk  = "🟢 Low" if dti < 30 else ("🟡 Medium" if dti < 50 else "🔴 High")
        loan_risk = "🟢 Good" if Credit_History == "Good" else "🔴 Poor"
        debt_risk = "🟢 Low" if Existing_Loans <= 2 else ("🟡 Moderate" if Existing_Loans <= 5 else "🔴 High")

        with r1:
            st.markdown(f"""<div class="card" style="text-align:center;padding:1rem;transition:all 0.3s ease">
                <div class="card-label">DTI Risk</div>
                <div style="font-size:1.1rem;font-weight:700;margin-top:.3rem">{dti_risk}</div>
            </div>""", unsafe_allow_html=True)
        with r2:
            st.markdown(f"""<div class="card" style="text-align:center;padding:1rem;transition:all 0.3s ease">
                <div class="card-label">Credit</div>
                <div style="font-size:1.1rem;font-weight:700;margin-top:.3rem">{loan_risk}</div>
            </div>""", unsafe_allow_html=True)
        with r3:
            st.markdown(f"""<div class="card" style="text-align:center;padding:1rem;transition:all 0.3s ease">
                <div class="card-label">Debt Load</div>
                <div style="font-size:1.1rem;font-weight:700;margin-top:.3rem">{debt_risk}</div>
            </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:var(--surface2);border:1px dashed var(--border);
                    border-radius:14px;padding:2.5rem;text-align:center;margin-top:0.5rem;">
          <div style="font-size:2.5rem;margin-bottom:0.8rem;">🔍</div>
          <div style="font-weight:600;font-size:1rem;margin-bottom:0.4rem;">Ready to Assess</div>
          <div style="color:#64748b;font-size:0.85rem;">
            Fill in the applicant details in the sidebar,<br>then click the button above to get an instant decision.
          </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<style>
@keyframes footerFadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.footer-wrap {
    margin-top: 4rem;
    padding: 2.5rem 2rem 2rem 2rem;
    border-top: 1px solid #1e2d45;
    text-align: center;
    animation: footerFadeIn 0.7s ease forwards;
    position: relative;
}
.footer-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 50%; transform: translateX(-50%);
    width: 120px; height: 1px;
    background: linear-gradient(90deg, transparent, #00d4a1, transparent);
}
.footer-tagline {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff 30%, #00d4a1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
}
.footer-sub {
    font-size: 0.82rem;
    color: #64748b;
    margin-bottom: 1.6rem;
    letter-spacing: 0.03em;
}
.footer-socials {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.8rem;
    flex-wrap: wrap;
}
.social-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1.1rem;
    border-radius: 100px;
    border: 1px solid #1e2d45;
    background: #111827;
    color: #94a3b8 !important;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-decoration: none !important;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.social-btn:hover { transform: translateY(-3px); color: #fff !important; text-decoration: none !important; }
.social-btn.linkedin:hover  { border-color: #0a66c2; box-shadow: 0 6px 24px rgba(10,102,194,0.35);  background: rgba(10,102,194,0.15);  color: #4d9eea !important; }
.social-btn.github:hover    { border-color: #6e7681; box-shadow: 0 6px 24px rgba(110,118,129,0.35); background: rgba(110,118,129,0.15); color: #e6edf3 !important; }
.social-btn.twitter:hover   { border-color: #e7e9ea; box-shadow: 0 6px 24px rgba(231,233,234,0.2);  background: rgba(231,233,234,0.08); color: #e7e9ea !important; }
.social-btn.instagram:hover { border-color: #e1306c; box-shadow: 0 6px 24px rgba(225,48,108,0.35);  background: linear-gradient(135deg,rgba(64,93,230,0.15),rgba(225,48,108,0.15)); color: #f77737 !important; }
.social-btn .s-icon { font-size: 1rem; transition: transform 0.25s ease; display: inline-block; }
.social-btn:hover .s-icon   { transform: scale(1.25) rotate(-8deg); }
.footer-copy { font-size: 0.72rem; color: #374151; letter-spacing: 0.07em; text-transform: uppercase; }
.footer-copy span { color: #4b5563; }
</style>

<div class="footer-wrap">
  <div class="footer-tagline">Join my journey and let's explore together.</div>
  <div class="footer-sub">I make predictions, not spoilers.</div>
  <div class="footer-socials">
    <a class="social-btn linkedin"   href="https://www.linkedin.com/in/vishal-singh-here/" target="_blank"><span class="s-icon">💼</span> LinkedIn</a>
    <a class="social-btn github"     href="https://github.com/VishalIndevp"               target="_blank"><span class="s-icon">🐙</span> GitHub</a>
    <a class="social-btn twitter"    href="https://x.com/vishalindev"                     target="_blank"><span class="s-icon">✦</span> X</a>
    <a class="social-btn instagram"  href="https://www.instagram.com/vishalindev?igsh=dW9vbWk3Z28xb2U=" target="_blank"><span class="s-icon">📸</span> Instagram</a>
  </div>
  <div class="footer-copy">© 2025 <span>Vishal Singh</span> &nbsp;·&nbsp; 01-03-2026 &nbsp;·&nbsp; LoanIQ · Powered by XGBoost &nbsp;·&nbsp; <span style="color:#00d4a1;">84.44% Accuracy</span></div>
</div>
""", unsafe_allow_html=True)