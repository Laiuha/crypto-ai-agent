import streamlit as st
import requests
import pandas as pd
from pathlib import Path
from textwrap import dedent

# =========================================================
# KOSHKA CRYPTO AI AGENT
# Setup Check Scanner
# Educational only — not financial advice.
# =========================================================

st.set_page_config(
    page_title="Trust Me Bro Crypto Scanner",
    page_icon="🐈",
    layout="wide"
)

def html(content):
    # Streamlit may render indented HTML as a code block.
    # This normalizes indentation before rendering.
    cleaned = dedent(content).strip()
    cleaned = "\n".join(line.lstrip() for line in cleaned.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)

# ---------- STYLES ----------
html("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 1500px;
}

.stApp {
    background:
    radial-gradient(circle at top left, #1f2a44 0%, transparent 30%),
    radial-gradient(circle at bottom right, #111827 0%, transparent 35%),
    #0b1020;
}



h1 { font-size: 1.7rem !important; }
h2 { font-size: 1.35rem !important; }
h3 { font-size: 1.05rem !important; }
[data-testid="stMarkdownContainer"] h1 { font-size: 1.7rem !important; }
[data-testid="stMarkdownContainer"] h2 { font-size: 1.35rem !important; }
[data-testid="stMarkdownContainer"] h3 { font-size: 1.05rem !important; }

.hero, .card, .settings-box, .macro-box {
    background: linear-gradient(135deg,#182035,#25314f);
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 20px;
}

.big-title {
    font-size: 40px;
    font-weight: 900;
    color: white;
}

.subtitle {
    color: #b0b8d1;
    font-size: 16px;
    margin-top: 14px;
}

.coin-title {
    font-size: 38px;
    font-weight: 900;
    color: white;
}

.coin-name {
    font-size: 18px;
    color: #c7d2fe;
    margin-bottom: 22px;
}

.price {
    font-size: 34px;
    font-weight: 900;
    color: white;
}

.metric-positive {
    color: #4ade80;
    font-size: 18px;
    font-weight: 700;
}

.metric-negative {
    color: #f87171;
    font-size: 18px;
    font-weight: 700;
}

.small-muted {
    color: #b0b8d1;
    font-size: 17px;
}

.macro-value {
    font-size: 32px;
    font-weight: 900;
    color: white;
    margin: 8px 0;
}

.macro-label {
    color: #b0b8d1;
    font-size: 15px;
    margin-bottom: 6px;
}

.macro-desc {
    font-size: 16px;
    font-weight: 700;
    margin-top: 4px;
}

.badge {
    display:inline-block;
    padding:10px 18px;
    border-radius:999px;
    font-weight:900;
    font-size:16px;
    margin-bottom:18px;
}

.green { background:#064e3b; color:#86efac; }
.yellow { background:#713f12; color:#fde68a; }
.red { background:#7f1d1d; color:#fca5a5; }
.blue { background:#1e3a8a; color:#bfdbfe; }
.purple { background:#581c87; color:#e9d5ff; }

.fg-extreme-fear { color: #f87171; }
.fg-fear { color: #fb923c; }
.fg-neutral { color: #facc15; }
.fg-greed { color: #a3e635; }
.fg-extreme-greed { color: #4ade80; }

.warning-box {
    background: rgba(251,146,60,0.12);
    border: 1px solid #fb923c;
    border-radius: 14px;
    padding: 14px 18px;
    margin-top: 14px;
    color: #fed7aa;
    font-size: 15px;
}

.info-box {
    background: rgba(99,102,241,0.12);
    border: 1px solid #6366f1;
    border-radius: 14px;
    padding: 14px 18px;
    margin-top: 14px;
    color: #c7d2fe;
    font-size: 15px;
}

.macro-summary-box {
    background: rgba(16,185,129,0.10);
    border: 1px solid #10b981;
    border-radius: 18px;
    padding: 18px 22px;
    margin-top: 10px;
    color: #a7f3d0;
    font-size: 16px;
}

.reason-row {
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: #b0b8d1;
    font-size: 14px;
    line-height:1.35;
}

.reason-label {
    color: white;
    font-weight: 700;
}

.trade-plan-box {
    background: rgba(15,23,42,0.55);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 18px 22px;
    margin-top: 14px;
    color: #dbeafe;
    font-size: 16px;
}

.kpi {
    min-height: 190px;
    overflow-wrap: break-word;
    word-break: normal;
    background: rgba(15,23,42,0.55);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 18px;
    color: white;
}

.clean-macro-card {
    background: linear-gradient(135deg,#182035,#25314f);
    border-radius: 24px;
    padding: 24px;
    min-height: 220px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.06);
}

.clean-macro-title {
    color: #b0b8d1;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 14px;
}

.clean-macro-value {
    color: white;
    font-size: 34px;
    font-weight: 900;
    line-height: 1.05;
    margin-bottom: 12px;
}

.clean-macro-status {
    display:inline-block;
    padding:8px 14px;
    border-radius:999px;
    font-size:15px;
    font-weight:900;
    margin-bottom:14px;
}

.clean-macro-desc {
    color:#cbd5e1;
    font-size:15px;
    line-height:1.45;
    margin-top:8px;
}

.clean-summary {
    background: rgba(99,102,241,0.12);
    border: 1px solid #6366f1;
    border-radius: 18px;
    padding: 18px 22px;
    margin-top: 8px;
    margin-bottom: 20px;
    color: #dbeafe;
    font-size: 16px;
    line-height: 1.45;
}

.kpi {
    min-height: 190px;
    overflow-wrap: break-word;
    word-break: normal;
    background: rgba(15,23,42,0.55);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 18px;
    color: white;
}


/* ---------- POLISHED DASHBOARD LAYOUT ---------- */
.dashboard-grid {
    display: grid;
    grid-template-columns: minmax(360px, 0.9fr) minmax(520px, 1.1fr);
    gap: 22px;
    align-items: stretch;
    margin-top: 14px;
}
@media (max-width: 1000px) {
    .dashboard-grid { grid-template-columns: 1fr; }
}
.glass-card {
    background: linear-gradient(145deg, rgba(17,24,39,0.98), rgba(31,42,68,0.96));
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 14px 40px rgba(0,0,0,0.24);
    color: white;
}
.coin-card-main {
    min-height: auto;
}
.coin-head-row {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:14px;
    margin-bottom: 14px;
}
.coin-symbol-round {
    width:50px;
    height:50px;
    border-radius:16px;
    display:flex;
    align-items:center;
    justify-content:center;
    background: radial-gradient(circle at 30% 30%, #ffcc66, #f97316 70%);
    font-size:27px;
    font-weight:900;
    box-shadow: 0 8px 22px rgba(249,115,22,0.22);
}
.coin-title-small {
    color:white;
    font-size:28px;
    font-weight:900;
    line-height:1.0;
}
.coin-subtitle-small {
    color:#aab4cf;
    font-size:14px;
    margin-top:5px;
}
.price-line {
    display:flex;
    justify-content:space-between;
    align-items:flex-end;
    gap:14px;
    margin: 6px 0 14px 0;
}
.price-main {
    font-size:30px;
    font-weight:900;
    letter-spacing:-0.03em;
    color:white;
    margin-bottom:0;
}
.metric-grid {
    display:grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap:8px;
    margin-top:12px;
}
@media (max-width: 1200px) { .metric-grid { grid-template-columns: repeat(2, 1fr); } }
.metric-tile {
    background: rgba(15,23,42,0.62);
    border: 1px solid rgba(148,163,184,0.16);
    border-radius:13px;
    padding:10px 12px;
    min-height:70px;
}
.metric-tile-wide { grid-column: span 1; }
.metric-title-mini {
    color:#aab4cf;
    font-size:12px;
    margin-bottom:5px;
    line-height:1.2;
}
.metric-value-mini {
    color:white;
    font-size:17px;
    font-weight:850;
}
.metric-helper-mini {
    color:#7f8aa8;
    font-size:10.5px;
    margin-top:3px;
    line-height:1.2;
}
.metric-status-mini {
    display:inline-flex;
    align-items:center;
    gap:6px;
    margin-top:7px;
    padding:5px 9px;
    border-radius:999px;
    font-size:11px;
    font-weight:850;
    line-height:1.15;
}
.metric-status-green { background:rgba(22,101,52,0.34); color:#86efac; }
.metric-status-yellow { background:rgba(113,63,18,0.38); color:#fde68a; }
.metric-status-red { background:rgba(127,29,29,0.38); color:#fca5a5; }
.score-breakdown-head {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:12px;
    margin-bottom:12px;
}
.score-chip {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    border-radius:999px;
    padding:8px 14px;
    font-size:15px;
    font-weight:950;
    background:rgba(127,29,29,0.30);
    color:#fca5a5;
    border:1px solid rgba(248,113,113,0.35);
    white-space:nowrap;
}
.reason-mini-summary {
    display:grid;
    grid-template-columns: repeat(2, 1fr);
    gap:8px;
    margin:8px 0 10px 0;
}
@media (max-width: 760px) { .reason-mini-summary { grid-template-columns:1fr; } }
.reason-summary-box {
    background: rgba(15,23,42,0.45);
    border:1px solid rgba(148,163,184,0.14);
    border-radius:13px;
    padding:10px 12px;
    color:#cbd5e1;
    font-size:12.5px;
    line-height:1.35;
}
.reason-summary-title {
    color:white;
    font-size:13px;
    font-weight:900;
    margin-bottom:6px;
}
.reason-details-title {
    color:#aab4cf;
    font-size:13px;
    font-weight:850;
    margin:10px 0 6px 0;
}
.score-intro-box {
    background: rgba(99,102,241,0.10);
    border:1px solid rgba(99,102,241,0.28);
    border-radius:13px;
    padding:10px 12px;
    color:#cbd5e1;
    font-size:12.5px;
    line-height:1.45;
    margin-bottom:10px;
}
.factor-row {
    display:grid;
    grid-template-columns: 78px 1fr;
    gap:10px;
    padding:9px 0;
    border-bottom:1px solid rgba(255,255,255,0.06);
}
.factor-row:last-child { border-bottom:0; }
.factor-impact {
    align-self:start;
    display:inline-flex;
    justify-content:center;
    align-items:center;
    border-radius:999px;
    padding:5px 8px;
    font-size:11px;
    font-weight:950;
    white-space:nowrap;
}
.factor-impact.positive { background:rgba(22,101,52,0.45); color:#86efac; }
.factor-impact.negative { background:rgba(127,29,29,0.45); color:#fca5a5; }
.factor-impact.neutral { background:rgba(113,63,18,0.45); color:#fde68a; }
.factor-title { color:white; font-weight:900; font-size:14px; margin-bottom:3px; }
.factor-desc { color:#aab4cf; font-size:12.5px; line-height:1.4; }
.factor-plain { color:#cbd5e1; font-size:12px; margin-top:3px; line-height:1.35; }

.positive-text { color:#4ade80 !important; }
.negative-text { color:#f87171 !important; }
.decision-top {
    display:grid;
    grid-template-columns: minmax(220px, auto) 150px;
    gap:16px;
    align-items:center;
    margin:18px 0 20px 0;
}
@media (max-width: 720px) { .decision-top { grid-template-columns: 1fr; } }
.big-decision-badge {
    display:flex;
    align-items:center;
    justify-content:center;
    gap:12px;
    border-radius:999px;
    padding:20px 26px;
    font-size:28px;
    font-weight:950;
    text-transform:uppercase;
    letter-spacing:-0.02em;
}
.score-box {
    background: rgba(15,23,42,0.62);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius:16px;
    padding:16px;
}
.score-box-label { color:#cbd5e1; font-size:14px; }
.score-box-value { color:#f87171; font-size:28px; font-weight:950; }
.alert-summary {
    display:flex;
    gap:14px;
    align-items:center;
    background: rgba(127,29,29,0.16);
    border:1px solid rgba(248,113,113,0.42);
    border-radius:16px;
    padding:15px 18px;
    color:#e5e7eb;
    margin-bottom:22px;
}
.alert-icon {
    width:34px;
    height:34px;
    flex:0 0 34px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    background:#ef4444;
    color:white;
    font-weight:900;
}
.decision-row {
    display:grid;
    grid-template-columns: 1fr auto;
    gap:18px;
    align-items:center;
    padding:16px 0;
    border-bottom: 1px solid rgba(255,255,255,0.09);
}
.decision-row:last-child { border-bottom:0; }
.decision-label-wrap {
    display:flex;
    gap:14px;
    align-items:center;
}
.decision-icon {
    width:42px;
    height:42px;
    border-radius:14px;
    display:flex;
    align-items:center;
    justify-content:center;
    background: rgba(99,102,241,0.14);
    border:1px solid rgba(99,102,241,0.30);
    font-size:22px;
}
.decision-title { color:white; font-weight:850; font-size:17px; }
.decision-sub { color:#aab4cf; font-size:14px; margin-top:3px; }
.pill-mini {
    display:inline-flex;
    align-items:center;
    gap:8px;
    border-radius:16px;
    padding:12px 16px;
    font-size:15px;
    font-weight:900;
    min-width:185px;
    justify-content:center;
}
.plan-grid-modern {
    display:grid;
    grid-template-columns: repeat(4, 1fr);
    gap:10px;
    margin-top:14px;
}
@media (max-width: 900px) { .plan-grid-modern { grid-template-columns: repeat(2, 1fr); } }
.plan-tile {
    background: rgba(15,23,42,0.62);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius:14px;
    padding:14px 12px;
    text-align:center;
    min-height:105px;
}
.plan-title { font-size:15px; font-weight:950; margin-bottom:8px; }
.plan-value { color:white; font-size:15px; font-weight:800; line-height:1.35; }
.plan-desc {
    color:#aab4cf;
    font-size:12.5px;
    line-height:1.45;
    margin-top:10px;
    text-align:left;
}
.plan-desc b { color:#dbeafe; }
.plan-tile { display:flex; flex-direction:column; justify-content:flex-start; }
.border-blue { border-color: rgba(59,130,246,0.55); }
.border-red { border-color: rgba(248,113,113,0.55); }
.border-green { border-color: rgba(74,222,128,0.45); }
.compact-section-title {
    color:white;
    font-size:20px;
    font-weight:900;
    margin-bottom:12px;
}
.reasons-card {
    margin-top:18px;
}

/* ---------- COMPACT CONTROLS ---------- */
.controls-panel {
    background: rgba(15,23,42,0.50);
    border: 1px solid rgba(99,102,241,0.28);
    border-radius: 14px;
    padding: 10px 14px;
    margin: 8px 0 10px 0;
    box-shadow: 0 8px 22px rgba(0,0,0,0.14);
}
.controls-title {
    color: #ffffff;
    font-size: 16px;
    font-weight: 900;
    letter-spacing: -0.02em;
}
.controls-subtitle {
    color: #aab4cf;
    font-size: 12px;
    margin-left: 8px;
}
.compact-row-title {
    color:white;
    font-size:15px;
    font-weight:900;
    margin: 10px 0 4px 2px;
}
.section-marker {
    background: rgba(15,23,42,0.46);
    border: 1px solid rgba(148,163,184,0.14);
    border-left: 3px solid #818cf8;
    border-radius: 14px;
    padding: 9px 12px;
    margin: 8px 0 8px 0;
}
.section-marker-title {
    color: white;
    font-size: 15px;
    font-weight: 900;
}
.section-marker-sub {
    color: #aab4cf;
    font-size: 12px;
    margin-top: 2px;
}
.selected-coin-banner {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.22);
    border-radius: 12px;
    padding: 8px 12px;
    margin: 8px 0 12px 0;
    color: #dbeafe;
    font-size: 12.5px;
}
.selected-coin-banner b { color: white; }
[data-testid="stSelectbox"] {
    background: rgba(15,23,42,0.34);
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 12px;
    padding: 3px 8px 5px 8px;
}
[data-testid="stSelectbox"] label p {
    font-size: 12px !important;
    font-weight: 800 !important;
}
[data-baseweb="select"] > div {
    min-height: 36px !important;
}
[data-testid="stSlider"] {
    background: rgba(15,23,42,0.34);
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 12px;
    padding: 8px 12px 10px 12px;
}
button[data-baseweb="tab"] {
    font-weight: 850;
    font-size: 16px;
}



/* ---------- PREMIUM FILTER ROW ---------- */
.filter-bar-wrap {
    margin: 18px 0 24px 0;
    padding: 18px;
    border: 1px solid rgba(59,130,246,0.22);
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(2,6,23,0.42), rgba(15,23,42,0.58));
    box-shadow: 0 18px 45px rgba(0,0,0,0.22);
}
.filter-helper-line {
    color:#8f9ab8;
    font-size:12px;
    margin: 10px 0 0 4px;
}
/* make all three filters the same clean blue style */
.filter-bar-wrap [data-testid="stSelectbox"] {
    min-height: 118px;
    background: linear-gradient(145deg, rgba(15,23,42,0.86), rgba(30,41,59,0.66)) !important;
    border: 1px solid rgba(96,165,250,0.28) !important;
    border-radius: 18px !important;
    padding: 16px 18px 14px 18px !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18) !important;
}
.filter-bar-wrap [data-testid="stSelectbox"]:hover {
    border-color: rgba(96,165,250,0.55) !important;
    box-shadow: 0 0 0 1px rgba(96,165,250,0.18), 0 14px 34px rgba(0,0,0,0.22) !important;
}
.filter-bar-wrap [data-testid="stSelectbox"] label p {
    color:#ffffff !important;
    font-size:15px !important;
    font-weight:900 !important;
    letter-spacing:-0.01em !important;
}
.filter-bar-wrap [data-baseweb="select"] > div {
    min-height: 52px !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,0.045) !important;
    border: 1px solid rgba(148,163,184,0.16) !important;
}
.filter-bar-wrap [data-baseweb="select"] span,
.filter-bar-wrap [data-baseweb="select"] div {
    font-size: 19px !important;
}
/* first filter is wider but same style, with a slightly stronger border */
.filter-bar-wrap div[data-testid="column"]:first-child [data-testid="stSelectbox"] {
    border-color: rgba(96,165,250,0.48) !important;
    box-shadow: 0 0 0 1px rgba(96,165,250,0.12), 0 14px 36px rgba(0,0,0,0.24) !important;
}
@media (max-width: 900px) {
    .filter-bar-wrap { padding: 12px; }
    .filter-bar-wrap [data-testid="stSelectbox"] { min-height: auto; }
}

</style>
""")

cat_black = Path("cat_black.png")
cat_orange = Path("cat_orange.png")

# ---------- REASON EXPLANATIONS ----------
REASON_EXPLAIN = {
    "early 1h momentum": (
        "early 1h momentum",
        "Цена растёт последний час — возможно начало движения. / Price rising in the last hour — possible start of a move."
    ),
    "healthy 24h move": (
        "healthy 24h move",
        "Рост за 24ч умеренный — не слишком много, не слишком мало. / 24h gain is moderate."
    ),
    "healthy momentum": (
        "healthy momentum",
        "Общий импульс монеты в здоровом диапазоне. / Overall coin momentum is healthy."
    ),
    "momentum overheated": (
        "momentum overheated ⚠️",
        "Монета выросла слишком быстро — риск отката. / Coin rose too fast — pullback risk is high."
    ),
    "weak momentum": (
        "weak momentum",
        "Импульс слабый — монета не двигается активно. / Momentum is weak."
    ),
    "strong volume activity": (
        "strong volume activity",
        "Много людей торгуют этой монетой прямо сейчас — сильный интерес. / Strong trading interest."
    ),
    "normal volume activity": (
        "normal volume activity",
        "Объём торгов нормальный — стандартная активность. / Standard trading activity."
    ),
    "weak volume activity": (
        "weak volume activity ⚠️",
        "Мало торгов — монету могут легко двигать крупные игроки. / Low liquidity risk."
    ),
    "good liquidity": (
        "good liquidity",
        "Монета крупная — проще купить и продать. / Large coin — easier to buy and sell."
    ),
    "already pumped too much": (
        "already pumped too much ⛔",
        "Монета уже сильно выросла — поздний вход опасен. / Coin already pumped — late entry risk."
    ),
    "24h move overextended": (
        "24h move overextended ⚠️",
        "Рост за 24ч выше здорового предела. / 24h move is overextended."
    ),
    "7d overheated": (
        "7d overheated ⚠️",
        "За неделю монета выросла слишком сильно. / Weekly move looks overheated."
    ),
    "falling momentum": (
        "falling momentum ⛔",
        "Монета падает — входить против тренда рискованно. / Coin is falling."
    ),
    "no strong setup": (
        "no strong setup",
        "Нет сильного сигнала. / No strong setup."
    ),
}

def factor_impact(reason):
    low = reason.lower()
    negative_keys = ["weak", "overheated", "pumped", "overextended", "falling", "no strong"]
    positive_keys = ["early", "healthy", "strong", "normal", "good"]

    if any(k in low for k in negative_keys):
        return "negative", "- score", "Понижает score"
    if any(k in low for k in positive_keys):
        return "positive", "+ score", "Повышает score"
    return "neutral", "info", "Контекст"

def explain_reasons(reasons):
    rows = []
    for r in reasons:
        label, desc = REASON_EXPLAIN.get(r, (r, ""))
        impact_class, impact_en, impact_ru = factor_impact(r)
        rows.append(f"""
        <div class="factor-row">
            <div class="factor-impact {impact_class}">{impact_en}</div>
            <div>
                <div class="factor-title">{label}</div>
                <div class="factor-desc">{desc}</div>
                <div class="factor-plain"><b>{impact_ru}</b> — этот фактор является одним из основных сигналов, которые сработали сейчас.</div>
            </div>
        </div>
        """)
    return "".join(rows)


def score_reason_summary(reasons):
    positive_keys = ["early", "healthy", "strong", "normal", "good"]
    negative_keys = ["weak", "overheated", "pumped", "overextended", "falling", "no strong"]

    positives = []
    negatives = []

    for r in reasons:
        label, _ = REASON_EXPLAIN.get(r, (r, ""))
        clean = label.replace("⚠️", "").replace("⛔", "").strip()
        low = r.lower()
        if any(k in low for k in negative_keys):
            negatives.append(clean)
        elif any(k in low for k in positive_keys):
            positives.append(clean)

    if not positives:
        positives = ["no clear positive signal / нет явного сильного плюса"]
    if not negatives:
        negatives = ["no major red flag / нет сильного красного флага"]

    pos_html = "<br>".join([f"✅ {p}" for p in positives[:3]])
    neg_html = "<br>".join([f"⚠️ {n}" for n in negatives[:3]])
    return pos_html, neg_html

# ---------- HEADER ----------
h1, h2 = st.columns([1, 5])

with h1:
    if cat_black.exists():
        st.image(str(cat_black), width=120)
    else:
        st.markdown("🐈")

with h2:
    html("""
    <div class="hero">
        <div class="big-title">Trust Me Bro Crypto Scanner</div>
        <div class="subtitle"> Крипто сканер «Кофейная гуща»
        <div class="subtitle"> AI-assisted scoring engine for high-probability crypto setups.
        </div>
    </div>
    """)

# ---------- PAGE TABS ----------
tab_coin, tab_opps, tab_market = st.tabs([
    "🔍 Coin Analysis",
    "🚀 Best Opportunities",
    "🌐 Market Overview"
])

# ---------- TAB-SPECIFIC CONTROLS ----------
# Coin Analysis filters: all controls in one clean row.
with tab_coin:
    html('<div class="filter-bar-wrap">')
    f_coin, f_currency, f_risk = st.columns([1.45, 1.0, 1.0], gap="medium")

    with f_coin:
        coin_selector_slot = st.empty()

    with f_currency:
        currency = st.selectbox(
            "💲 Currency",
            ["usd", "aed", "eur", "gbp", "rub"],
            index=1
        )

    with f_risk:
        risk_mode = st.selectbox(
            "🛡️ Risk Mode",
            ["Conservative", "Average", "Aggressive"],
            index=1
        )
    html('</div>')

# Best Opportunities keeps scanner-only controls.
with tab_opps:
    html("""
    <div class="controls-panel">
        <span class="controls-title">⚙️ Settings</span>
        <span class="controls-subtitle">Scanner size + minimum opportunity score control opportunities.</span>
    </div>
    """)

    s1, s2 = st.columns(2)
    with s1:
        scan_size = st.selectbox(
            "Coins To Scan",
            [100, 250, 500, 750],
            index=1
        )
        st.caption("100 = fast scan • 250 = balanced • 750 = deep scan")

    with s2:
        min_score_filter = st.slider(
            "Minimum Opportunity Score",
            min_value=0,
            max_value=100,
            value=50,
            step=5
        )

# ---------- MACRO APIs ----------

@st.cache_data(ttl=300)
def load_fear_greed():
    try:
        r = requests.get(
            "https://api.alternative.me/fng/?limit=1",
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            item = data["data"][0]
            return {
                "value": int(item["value"]),
                "label": item["value_classification"]
            }
    except Exception:
        pass
    return None

@st.cache_data(ttl=300)
def load_btc_dominance():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/global",
            headers={"User-Agent": "Koshka-Agent"},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            btc_dom = data["data"]["market_cap_percentage"].get("btc", None)
            total_mcap = data["data"].get("total_market_cap", {}).get("usd", None)
            return {
                "btc_dominance": round(btc_dom, 1) if btc_dom else None,
                "total_mcap": total_mcap
            }
    except Exception:
        pass
    return None

# ---------- MARKET API ----------
@st.cache_data(ttl=300)
def load_market(currency, scan_size):

    url = "https://api.coingecko.com/api/v3/coins/markets"

    headers = {
        "accept": "application/json",
        "User-Agent": "Koshka-Agent"
    }

    all_data = []
    per_page = 250
    pages_needed = (scan_size + per_page - 1) // per_page

    try:
        for page in range(1, pages_needed + 1):

            params = {
                "vs_currency": currency,
                "order": "market_cap_desc",
                "per_page": per_page,
                "page": page,
                "sparkline": "false",
                "price_change_percentage": "1h,24h,7d"
            }

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=20
            )

            if response.status_code == 429:
                return {"error": "API limit reached. Please wait a few minutes and refresh."}

            if response.status_code != 200:
                return {"error": f"API error {response.status_code}"}

            page_data = response.json()

            if not page_data:
                break

            all_data.extend(page_data)

        if not all_data:
            return {"error": "No market data returned. Please refresh later."}

        return {"data": all_data[:scan_size]}

    except Exception as e:
        return {"error": str(e)}

# ---------- HELPERS ----------
def fmt(value):
    if value is None:
        return "N/A"

    try:
        value = float(value)
    except Exception:
        return "N/A"

    if value < 0:
        return f"-{fmt(abs(value))}"

    if value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"

    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if value >= 1000:
        return f"{value:,.0f}"

    if value >= 1:
        return f"{value:,.2f}"

    return f"{value:.6f}"

def change(coin, key):
    return coin.get(key) or 0

def momentum_proxy(ch1, ch24, ch7):
    # Transparent proxy, not real RSI.
    score = 50
    score += ch1 * 3
    score += ch24 * 1.5
    score += ch7 * 0.35
    return round(max(0, min(score, 100)), 1)

def volume_ratio(volume, market_cap):
    if market_cap <= 0:
        return 0
    return volume / market_cap

def get_market_bias(fg, btc_global):
    if not fg or not btc_global or not btc_global.get("btc_dominance"):
        return "UNKNOWN", 0, "Market data incomplete."

    val = fg["value"]
    dom = btc_global["btc_dominance"]

    if val >= 75:
        return "OVERHEATED", -10, "Extreme greed — market can be overheated."
    if val <= 24 and dom < 55:
        return "ACCUMULATION", 8, "Extreme fear — possible accumulation zone."
    if dom >= 55:
        return "BTC_SEASON", -6, "BTC dominance is high — altcoins may underperform."
    if dom < 48 and val <= 74:
        return "ALT_FRIENDLY", 8, "BTC dominance is low — altcoin market looks more favorable."

    return "MIXED", 0, "Mixed market — no strong macro edge."

def coin_health_score(coin, risk_mode, market_bias_score=0):
    score = 0
    reasons = []

    ch1 = coin["1h"]
    ch24 = coin["24h"]
    ch7 = coin["7d"]
    volume = coin["volume"]
    market_cap = coin["market_cap"]
    proxy = coin["momentum_proxy"]
    vr = volume_ratio(volume, market_cap)

    if risk_mode == "Conservative":
        max_24h = 6
        max_7d = 25
    elif risk_mode == "Aggressive":
        max_24h = 12
        max_7d = 40
    else:
        max_24h = 8
        max_7d = 30

    # Early momentum
    if 0.3 <= ch1 <= 2.5:
        score += 18
        reasons.append("early 1h momentum")
    elif ch1 > 5:
        score -= 10
        reasons.append("momentum overheated")

    # Healthy daily move
    if 1 <= ch24 <= max_24h:
        score += 25
        reasons.append("healthy 24h move")
    elif ch24 > 12:
        score -= 30
        reasons.append("already pumped too much")
    elif ch24 > max_24h:
        score -= 15
        reasons.append("24h move overextended")

    # Momentum proxy
    if 45 <= proxy <= 70:
        score += 20
        reasons.append("healthy momentum")
    elif proxy > 78:
        score -= 20
        reasons.append("momentum overheated")
    elif proxy < 35:
        score -= 10
        reasons.append("weak momentum")

    # Volume / liquidity
    if vr > 0.08:
        score += 20
        reasons.append("strong volume activity")
    elif vr > 0.03:
        score += 10
        reasons.append("normal volume activity")
    else:
        score -= 10
        reasons.append("weak volume activity")

    if market_cap > 500_000_000:
        score += 10
        reasons.append("good liquidity")
    elif market_cap < 100_000_000:
        score -= 10
        reasons.append("weak volume activity")

    # Weekly overheating
    if ch7 > max_7d:
        score -= 20
        reasons.append("7d overheated")

    # Falling / bad trend
    if ch24 < -6:
        score -= 20
        reasons.append("falling momentum")

    # Macro bias
    score += market_bias_score

    # Risk mode adjustment
    if risk_mode == "Aggressive":
        score += 5
    elif risk_mode == "Conservative":
        score -= 5

    score = max(0, min(score, 100))

    if not reasons:
        reasons.append("no strong setup")

    return score, reasons

def signal_decision(score):
    if score >= 75:
        return "🟢 STRONG SIGNAL", "green"
    if score >= 50:
        return "🟡 NEUTRAL", "yellow"
    return "🔴 HIGH RISK", "red"

def entry_quality(coin):
    ch1 = coin["1h"]
    ch24 = coin["24h"]
    ch7 = coin["7d"]
    proxy = coin["momentum_proxy"]

    if 0.2 <= ch1 <= 3.5 and 0.5 <= ch24 <= 10 and ch7 <= 35 and proxy <= 74:
        return "🟢 Early", "green", "Хороший ранний момент: движение только формируется."

    if ch24 > 12 or ch7 > 35 or proxy > 78 or ch1 > 5:
        return "🔴 Too Late", "red", "Цена уже сильно выросла — вход может быть поздним."

    if ch24 >= 0 and proxy >= 40:
        return "🟡 Wait For Better Entry", "yellow", "Пока не лучший вход. Лучше ждать цену лучше или подтверждение."

    return "🔴 Bad Timing", "red", "Сейчас слабый момент для входа."

def risk_level(coin):
    ch24 = coin["24h"]
    ch7 = coin["7d"]
    proxy = coin["momentum_proxy"]
    market_cap = coin["market_cap"]
    vr = volume_ratio(coin["volume"], market_cap)

    risk_points = 0

    if market_cap < 100_000_000:
        risk_points += 3
    elif market_cap < 500_000_000:
        risk_points += 2

    if ch24 > 12:
        risk_points += 3
    elif ch24 > 8:
        risk_points += 2

    if ch7 > 35:
        risk_points += 2

    if proxy > 78:
        risk_points += 2

    if vr < 0.02:
        risk_points += 2

    if risk_points >= 6:
        return "🔴 High Risk", "red"
    if risk_points >= 3:
        return "🟡 Elevated Risk", "yellow"
    return "🟢 Average Risk", "green"

def what_to_do(coin, fg=None):
    """Immediate action for this coin right now.
    This is NOT an exit/sell signal. It answers: what should I do with this coin now?
    """
    score = coin.get("score", 0)
    eq, _, _ = entry_quality(coin)
    risk, _ = risk_level(coin)

    if "Too Late" in eq:
        return "⏳ Wait", "yellow", "Цена уже убежала. Лучше ждать откат или новый setup."

    if "High Risk" in risk:
        return "🚫 Skip This Coin", "red", "Риск высокий — лучше пропустить сейчас."

    if score >= 68 and "Early" in eq:
        return "🛒 Small Entry Possible", "green", "Можно рассмотреть маленький осторожный вход, не all-in."

    if score >= 50:
        return "👀 Add To Watchlist", "green", "Монета не плохая, но сильного сигнала на вход пока нет."

    return "👀 Add To Watchlist", "green", "Сильного сигнала на действие нет — просто наблюдать."


def profit_status(coin, fg=None):
    """Exit/profit assessment for someone who already holds the coin.
    This answers: hold, consider taking profit, or take profit?
    """
    ch1 = coin["1h"]
    ch24 = coin["24h"]
    ch7 = coin["7d"]
    proxy = coin["momentum_proxy"]
    fg_value = fg["value"] if fg else None

    if ch24 > 18 or ch7 > 45 or proxy > 85:
        return "🔴 Take Profit", "red", "Монета выглядит перегретой. Если уже держишь — можно фиксировать часть прибыли."

    if fg_value and fg_value >= 75 and ch24 > 8:
        return "🟡 Consider Taking Profit", "yellow", "Рынок в жадности, монета уже выросла — можно забрать часть прибыли."

    if ch24 < -6 or ch1 < -3:
        return "🔴 Exit / Avoid", "red", "Momentum сломался — риск дальнейшего падения выше."

    return "🟢 Hold / No Exit Signal", "green", "Сильного сигнала на выход нет. Можно просто наблюдать."


def exit_signal(coin, fg=None):
    # Backward-compatible alias for older parts of the app.
    return profit_status(coin, fg)

def trade_action(coin, fg=None, btc_global=None):
    score = coin["score"]
    eq, _, _ = entry_quality(coin)
    risk, _ = risk_level(coin)
    ps, _, _ = profit_status(coin, fg)

    market_bias, _, _ = get_market_bias(fg, btc_global)

    overheated = "Too Late" in eq or "Take Profit" in ps
    high_risk = "High Risk" in risk

    if overheated and score >= 65:
        return "💰 Take Profit / Don’t Chase", "red", "Цена уже убежала. Лучше не покупать на FOMO."

    if high_risk and score < 85:
        return "🔴 AVOID", "red", "Setup может быть интересным, но риск слишком высокий."

    if score >= 68 and "Good Early Setup" in eq and not high_risk:
        if market_bias in ["ALT_FRIENDLY", "ACCUMULATION", "MIXED"]:
            return "🟢 GOOD SETUP", "green", "Монета выглядит интересно: есть ранний momentum, объём и приемлемый риск."
        return "🟡 WATCH", "yellow", "Setup неплохой, но рынок сейчас не идеальный."

    if score >= 55:
        return "🟡 WATCH", "yellow", "Монета интересная, но лучше ждать подтверждение или откат."

    return "🔴 AVOID", "red", "Слабый setup или слишком высокий риск."

def trade_plan(coin, action):
    """Always calculate reference levels for the selected coin.
    The user may already hold the coin or may only be watching it, so Stop/TP1/TP2
    should always be visible as reference levels, not only when the app says BUY.
    """
    price = coin["price"]
    risk, _ = risk_level(coin)
    eq, _, _ = entry_quality(coin)
    ps, _, _ = profit_status(coin, fg)

    if price is None or price <= 0:
        return {
            "entry": "N/A",
            "stop": "N/A",
            "tp1": "N/A",
            "tp2": "N/A",
            "stop_pct": "N/A",
            "tp1_pct": "N/A",
            "tp2_pct": "N/A",
            "note_ru": "Нет цены для расчёта уровней.",
            "note_en": "No price available to calculate levels."
        }

    # Risk-based reference levels from current price.
    # These are simple educational levels, not a trading recommendation.
    if "High Risk" in risk:
        stop_pct = 10
        tp1_pct = 8
        tp2_pct = 15
    elif "Elevated Risk" in risk:
        stop_pct = 7
        tp1_pct = 8
        tp2_pct = 15
    else:
        stop_pct = 5
        tp1_pct = 6
        tp2_pct = 12

    stop_price = price * (1 - stop_pct / 100)
    tp1_price = price * (1 + tp1_pct / 100)
    tp2_price = price * (1 + tp2_pct / 100)

    if "GOOD SETUP" in action:
        entry_text = f"🛒 Current / near {fmt(price)}"
        note_ru = f"Если входишь сейчас — лучше маленькой суммой и частями. Stop ~-{stop_pct}%, TP1 +{tp1_pct}%, TP2 +{tp2_pct}%."
        note_en = f"If entering now, use small staged entry. Stop ~-{stop_pct}%, TP1 +{tp1_pct}%, TP2 +{tp2_pct}%."
    elif "WATCH" in action:
        entry_text = f"👀 Watch near {fmt(price)}"
        note_ru = f"Setup не идеальный, но уровни всё равно рассчитаны от текущей цены: Stop ~-{stop_pct}%, TP1 +{tp1_pct}%, TP2 +{tp2_pct}%."
        note_en = f"Setup is not ideal, but reference levels are calculated from current price: Stop ~-{stop_pct}%, TP1 +{tp1_pct}%, TP2 +{tp2_pct}%."
    elif "Take Profit" in action or "Take Profit" in ps:
        entry_text = f"⚠️ Current {fmt(price)}"
        note_ru = f"Цена может быть перегрета. Если уже держишь — TP/exit логика важнее нового входа. Reference Stop ~-{stop_pct}%, TP1 +{tp1_pct}%, TP2 +{tp2_pct}%."
        note_en = f"Coin may be overheated. If already holding, profit/exit logic matters more than new entry. Reference Stop ~-{stop_pct}%, TP1 +{tp1_pct}%, TP2 +{tp2_pct}%."
    else:
        entry_text = f"🚫 Avoid new entry near {fmt(price)}"
        note_ru = f"Для нового входа setup слабый, но если монета уже куплена — можно использовать ориентиры: Stop ~-{stop_pct}%, TP1 +{tp1_pct}%, TP2 +{tp2_pct}%."
        note_en = f"For a new entry the setup is weak, but if already holding, use reference levels: Stop ~-{stop_pct}%, TP1 +{tp1_pct}%, TP2 +{tp2_pct}%."

    return {
        "entry": entry_text,
        "stop": f"{fmt(stop_price)} ({stop_pct}% below)",
        "tp1": f"{fmt(tp1_price)} (+{tp1_pct}%)",
        "tp2": f"{fmt(tp2_price)} (+{tp2_pct}%)",
        "stop_pct": stop_pct,
        "tp1_pct": tp1_pct,
        "tp2_pct": tp2_pct,
        "note_ru": note_ru,
        "note_en": note_en
    }


def factor_interpretations(coin):
    """Human-readable interpretation for the raw metric cards.
    This answers: is each number good, neutral, or bad?
    """
    ch1 = coin["1h"]
    ch7 = coin["7d"]
    mcap = coin["market_cap"]
    vr = coin["volume_ratio"]
    proxy = coin["momentum_proxy"]

    # 1h movement
    if 0.3 <= ch1 <= 2.5:
        h1 = ("metric-status-green", "🟢 Good", "healthy early momentum / хороший ранний импульс")
    elif ch1 > 5:
        h1 = ("metric-status-red", "🔴 Risk", "too sharp, may pull back / слишком резкий скачок")
    elif ch1 > 2.5:
        h1 = ("metric-status-yellow", "🟡 Watch", "moving fast, wait confirmation / быстро растёт, жди подтверждение")
    elif ch1 < -1:
        h1 = ("metric-status-red", "🔴 Weak", "short-term pressure / краткосрочное давление")
    else:
        h1 = ("metric-status-yellow", "🟡 Neutral", "no strong short-term move / нет сильного движения")

    # 7d movement
    if ch7 > 35:
        d7 = ("metric-status-red", "🔴 Overheated", "weekly move too hot / неделя перегрета")
    elif 0 <= ch7 <= 30:
        d7 = ("metric-status-green", "🟢 Healthy", "weekly trend is OK / недельный тренд нормальный")
    elif ch7 < -10:
        d7 = ("metric-status-red", "🔴 Weak", "weekly trend is falling / недельный тренд падает")
    else:
        d7 = ("metric-status-yellow", "🟡 Mixed", "trend is not clear / тренд неясный")

    # Market cap / size
    if mcap >= 500_000_000:
        mcap_i = ("metric-status-green", "🟢 Safer", "large liquid coin / крупная ликвидная монета")
    elif mcap >= 100_000_000:
        mcap_i = ("metric-status-yellow", "🟡 Mid cap", "medium risk size / средний риск по размеру")
    else:
        mcap_i = ("metric-status-red", "🔴 Small cap", "higher manipulation risk / выше риск манипуляций")

    # Volume ratio / activity
    if vr > 0.08:
        vol = ("metric-status-green", "🟢 Strong", "strong trader interest / сильный интерес трейдеров")
    elif vr > 0.03:
        vol = ("metric-status-yellow", "🟡 Normal", "normal activity / обычная активность")
    else:
        vol = ("metric-status-red", "🔴 Low", "low activity, weaker signal / мало торгов, слабее сигнал")

    # Momentum proxy
    if 45 <= proxy <= 70:
        mom = ("metric-status-green", "🟢 Balanced", "healthy momentum zone / здоровая зона импульса")
    elif proxy > 78:
        mom = ("metric-status-red", "🔴 Hot", "overheated momentum / импульс перегрет")
    elif proxy < 35:
        mom = ("metric-status-red", "🔴 Weak", "momentum is weak / слабый импульс")
    else:
        mom = ("metric-status-yellow", "🟡 Mixed", "not ideal yet / пока не идеально")

    return {"h1": h1, "d7": d7, "mcap": mcap_i, "vol": vol, "mom": mom}



def opportunity_analysis(coin):
    """Scanner-specific ranking for Best Opportunities.
    It evaluates all loaded coins and tries to find realistic opportunities,
    not only the highest raw setup score.
    """
    score = coin.get("score", 0)
    ch1 = coin["1h"]
    ch24 = coin["24h"]
    ch7 = coin["7d"]
    vr = coin["volume_ratio"]
    mcap = coin["market_cap"]
    proxy = coin["momentum_proxy"]
    entry, _, _ = entry_quality(coin)
    risk, _ = risk_level(coin)
    ps, _, _ = profit_status(coin, fg)

    opp = score
    positives = []
    negatives = []

    if "Early" in entry:
        opp += 14
        positives.append("early entry timing")
    elif "Wait" in entry:
        opp -= 4
        negatives.append("entry is not ideal yet")
    elif "Too Late" in entry:
        opp -= 28
        negatives.append("already looks late / overheated")
    else:
        opp -= 12
        negatives.append("weak buy timing")

    if 0.5 <= ch24 <= 10:
        opp += 10
        positives.append("healthy 24h move")
    elif ch24 > 12:
        opp -= 26
        negatives.append("24h pump is too high")
    elif ch24 < -6:
        opp -= 18
        negatives.append("falling hard in 24h")

    if 0 <= ch7 <= 30:
        opp += 8
        positives.append("healthy weekly trend")
    elif ch7 > 35:
        opp -= 18
        negatives.append("weekly move may be overheated")
    elif ch7 < -12:
        opp -= 12
        negatives.append("weekly trend is weak")

    if vr > 0.08:
        opp += 12
        positives.append("strong trading volume")
    elif vr > 0.03:
        opp += 6
        positives.append("normal trading activity")
    else:
        opp -= 18
        negatives.append("low volume / weaker signal")

    if mcap >= 500_000_000:
        opp += 8
        positives.append("good liquidity")
    elif mcap < 100_000_000:
        opp -= 15
        negatives.append("small cap risk")

    if 45 <= proxy <= 70:
        opp += 8
        positives.append("balanced momentum")
    elif proxy > 78:
        opp -= 15
        negatives.append("momentum overheated")
    elif proxy < 35:
        opp -= 12
        negatives.append("weak momentum")

    if "High Risk" in risk:
        opp -= 25
        negatives.append("high risk setup")
    elif "Elevated Risk" in risk:
        opp -= 8
        negatives.append("risk is elevated")

    if "Take Profit" in ps or "Exit" in ps:
        opp -= 16
        negatives.append("exit/profit warning")

    opp = round(max(0, min(100, opp)), 1)

    if ch24 > 12 or ch7 > 35 or proxy > 78:
        category = "💰 Already Pumped / Don’t Chase"
        cat_color = "red"
    elif "High Risk" in risk or (mcap < 100_000_000 and vr < 0.03):
        category = "⚠️ Risky / Avoid"
        cat_color = "red"
    elif opp >= 75 and "Early" in entry:
        category = "🔥 Best Opportunity"
        cat_color = "green"
    elif opp >= 55:
        category = "👀 Watchlist Candidate"
        cat_color = "yellow"
    else:
        category = "🚫 Low Priority"
        cat_color = "red"

    if not positives:
        positives = ["no strong positive edge yet"]
    if not negatives:
        negatives = ["no major red flag"]

    return {
        "opportunity_score": opp,
        "category": category,
        "category_color": cat_color,
        "positive_reasons": positives[:4],
        "negative_reasons": negatives[:4],
    }

def plan_explanation(plan_key, action):
    if plan_key == "entry":
        if "AVOID" in action:
            return "🇬🇧 Not a fresh-buy signal. Use this only as a reference if you already hold the coin.<br>🇷🇺 Это не сигнал на новую покупку. Используй как ориентир, если монета уже куплена."
        if "WATCH" in action:
            return "🇬🇧 Better to wait for confirmation or a better price.<br>🇷🇺 Лучше ждать подтверждение или более хорошую цену."
        return "🇬🇧 Possible entry area based on current price.<br>🇷🇺 Возможная зона входа от текущей цены."

    if plan_key == "stop":
        return "🇬🇧 If price falls below this level, the idea may be wrong.<br>🇷🇺 Если цена падает ниже этого уровня, идея может быть ошибочной."

    if plan_key == "target1":
        return "🇬🇧 First area to consider taking partial profit.<br>🇷🇺 Первый уровень, где можно частично зафиксировать прибыль."

    if plan_key == "target2":
        return "🇬🇧 Second profit area if momentum continues.<br>🇷🇺 Второй уровень прибыли, если движение продолжится."

    return ""

# ---------- LOAD DATA ----------
fg = load_fear_greed()
btc_global = load_btc_dominance()

market = load_market(currency, scan_size)

if "error" in market:
    st.error(market["error"])
    st.stop()

market_data = market["data"]
market_bias, market_bias_score, market_bias_desc = get_market_bias(fg, btc_global)


# ---------- BUILD SIGNALS ----------
signals = []

for coin in market_data:
    ch1 = change(coin, "price_change_percentage_1h_in_currency")
    ch24 = change(coin, "price_change_percentage_24h")
    ch7 = change(coin, "price_change_percentage_7d_in_currency")

    signal = {
        "id": coin["id"],
        "coin": coin["name"],
        "symbol": coin["symbol"].upper(),
        "price": coin["current_price"],
        "1h": ch1,
        "24h": ch24,
        "7d": ch7,
        "volume": coin.get("total_volume") or 0,
        "market_cap": coin.get("market_cap") or 0
    }

    signal["volume_ratio"] = volume_ratio(signal["volume"], signal["market_cap"])
    signal["momentum_proxy"] = momentum_proxy(ch1, ch24, ch7)
    signal["score"], signal["reasons"] = coin_health_score(signal, risk_mode, market_bias_score)

    signal["signal"], signal["signal_color"] = signal_decision(signal["score"])
    signal["entry_quality"], signal["entry_color"], signal["entry_reason"] = entry_quality(signal)
    signal["risk_level"], signal["risk_color"] = risk_level(signal)
    signal["what_to_do"], signal["what_color"], signal["what_reason"] = what_to_do(signal, fg)
    signal["profit_status"], signal["profit_color"], signal["profit_reason"] = profit_status(signal, fg)
    # Keep old names for export/table compatibility, but they now mean Profit Status.
    signal["exit_signal"], signal["exit_color"], signal["exit_reason"] = signal["profit_status"], signal["profit_color"], signal["profit_reason"]
    signal["action"], signal["action_color"], signal["action_reason"] = trade_action(signal, fg, btc_global)
    signal["plan"] = trade_plan(signal, signal["action"])
    opp = opportunity_analysis(signal)
    signal.update(opp)

    signals.append(signal)

signals = sorted(signals, key=lambda x: x["score"], reverse=True)

filtered_signals = [s for s in signals if s["score"] >= min_score_filter]

# Part 1: selected coin analysis uses ALL loaded coins.
# Part 2: market scanner uses only coins passing the score filter.
best = filtered_signals[0] if filtered_signals else None
top10 = filtered_signals[:10]

with tab_coin:
    # ---------- SELECTED COIN ANALYSIS / POLISHED DASHBOARD ----------
    coin_options = {s["id"]: s for s in signals}
    coin_ids = list(coin_options.keys())

    default_coin_id = "bitcoin" if "bitcoin" in coin_options else coin_ids[0]

    if "coin_selector" in st.session_state and st.session_state["coin_selector"] not in coin_options:
        st.session_state["coin_selector"] = default_coin_id

    with coin_selector_slot.container():
        selected_coin_id = st.selectbox(
            "🔎 Choose coin to analyse",
            coin_ids,
            index=coin_ids.index(st.session_state.get("coin_selector", default_coin_id)),
            format_func=lambda coin_id:
                f"{coin_options[coin_id]['symbol']} — {coin_options[coin_id]['coin']}",
            key="coin_selector"
        )

    selected = coin_options[selected_coin_id]
    html(f"""
    <div class="selected-coin-banner">
        🔍 <b>{selected['symbol']} — {selected['coin']}</b> analysed in <b>{currency.upper()}</b> with <b>{risk_mode}</b> risk mode.
    </div>
    """)
    plan = selected["plan"]
    positive_reasons_html, negative_reasons_html = score_reason_summary(selected["reasons"])
    metric_class = "positive-text" if selected["24h"] >= 0 else "negative-text"
    h1_class = "positive-text" if selected["1h"] >= 0 else "negative-text"
    d7_class = "positive-text" if selected["7d"] >= 0 else "negative-text"
    factor_view = factor_interpretations(selected)
    h1_status_class, h1_status_label, h1_status_desc = factor_view["h1"]
    d7_status_class, d7_status_label, d7_status_desc = factor_view["d7"]
    mcap_status_class, mcap_status_label, mcap_status_desc = factor_view["mcap"]
    vol_status_class, vol_status_label, vol_status_desc = factor_view["vol"]
    mom_status_class, mom_status_label, mom_status_desc = factor_view["mom"]
    coin_icon = "₿" if selected["symbol"] == "BTC" else selected["symbol"][:1]

    is_small_cap = selected["market_cap"] < 500_000_000
    small_cap_warning = ""
    if is_small_cap and selected["score"] >= 65:
        small_cap_warning = """
        <div class="warning-box">
            ⚠️ <b>Small cap risk!</b><br>
            Маленькая монета: выше риск резких движений, низкой ликвидности и манипуляций.
        </div>
        """

    html(f"""
    <div class="dashboard-grid">
        <div>
            <div class="glass-card coin-card-main">
                <div class="coin-head-row">
                    <div style="display:flex; gap:16px; align-items:center;">
                        <div class="coin-symbol-round">{coin_icon}</div>
                        <div>
                            <div class="coin-title-small">{selected["symbol"]}</div>
                            <div class="coin-subtitle-small">{selected["coin"]}</div>
                        </div>
                    </div>
                    <span class="badge {selected["what_color"]}" style="margin:0; font-size:13px; padding:8px 12px;">Watchlist</span>
                </div>

                <div class="price-line">
                    <div class="price-main">{fmt(selected["price"])} {currency.upper()}</div>
                    <div class="{metric_class}" style="font-size:16px; font-weight:900; white-space:nowrap;">24h: {selected["24h"]:.2f}%</div>
                </div>

                <div class="metric-grid">
                    <div class="metric-tile">
                        <div class="metric-title-mini">1h Move / за час</div>
                        <div class="metric-value-mini {h1_class}">{selected["1h"]:.2f}%</div>
                        <div class="metric-status-mini {h1_status_class}">{h1_status_label}</div>
                        <div class="metric-helper-mini">{h1_status_desc}</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-title-mini">7d Move / за неделю</div>
                        <div class="metric-value-mini {d7_class}">{selected["7d"]:.2f}%</div>
                        <div class="metric-status-mini {d7_status_class}">{d7_status_label}</div>
                        <div class="metric-helper-mini">{d7_status_desc}</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-title-mini">Market Cap / размер</div>
                        <div class="metric-value-mini">{fmt(selected["market_cap"])}</div>
                        <div class="metric-status-mini {mcap_status_class}">{mcap_status_label}</div>
                        <div class="metric-helper-mini">{mcap_status_desc}</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-title-mini">Volume / интерес</div>
                        <div class="metric-value-mini">{selected["volume_ratio"]:.2%}</div>
                        <div class="metric-status-mini {vol_status_class}">{vol_status_label}</div>
                        <div class="metric-helper-mini">{vol_status_desc}</div>
                    </div>
                    <div class="metric-tile metric-tile-wide">
                        <div class="metric-title-mini">Momentum / импульс</div>
                        <div class="metric-value-mini">{selected["momentum_proxy"]}/100</div>
                        <div class="metric-status-mini {mom_status_class}">{mom_status_label}</div>
                        <div class="metric-helper-mini">{mom_status_desc}</div>
                    </div>
                </div>
                {small_cap_warning}
            </div>

            <div class="glass-card reasons-card">
                <div class="score-breakdown-head">
                    <div class="compact-section-title" style="margin-bottom:0;">🧮 What Affected The Score / Что повлияло на оценку</div>
                    <div class="score-chip">{selected["score"]}/100</div>
                </div>
                <div class="score-intro-box">
                    <b>AI checks multiple signals:</b> momentum, 24h/7d movement, volume, liquidity, overheating, market cap, risk mode and market conditions.<br>
                    <b>AI анализирует несколько сигналов:</b> импульс, движение за 24ч/7д, объём, ликвидность, перегрев, размер монеты, risk mode и состояние рынка.<br><br>
                    Below are the <b>main factors that affected this score right now</b> / Ниже — <b>главные факторы, которые повлияли на текущий score</b>.
                </div>
                <div class="reason-mini-summary">
                    <div class="reason-summary-box">
                        <div class="reason-summary-title">✅ Positive signals (+score) / Плюсы</div>
                        {positive_reasons_html}
                    </div>
                    <div class="reason-summary-box">
                        <div class="reason-summary-title">⚠️ Negative signals (-score) / Минусы</div>
                        {negative_reasons_html}
                    </div>
                </div>
                <div class="reason-details-title">Main triggered factors / Главные сработавшие факторы</div>
                {explain_reasons(selected["reasons"])}
            </div>
        </div>

        <div>
            <div class="glass-card">
                <div class="compact-section-title">🎯 Final Decision / Итоговая оценка</div>
                <div class="small-muted">Main summary for the selected coin / Главный вывод по выбранной монете</div>

                <div class="decision-top">
                    <div class="big-decision-badge {selected["action_color"]}">{selected["action"]}</div>
                    <div class="score-box">
                        <div class="score-box-label">Setup Score</div>
                        <div class="score-box-value">{selected["score"]}/100</div>
                    </div>
                </div>

                <div class="alert-summary">
                    <div class="alert-icon">!</div>
                    <div><b>{selected["action_reason"]}</b><br><span style="color:#cbd5e1;">Better opportunities may be available.</span></div>
                </div>

                <div class="decision-row">
                    <div class="decision-label-wrap">
                        <div class="decision-icon">🕒</div>
                        <div>
                            <div class="decision-title">Buy Timing</div>
                            <div class="decision-sub">When is the best time to buy?</div>
                        </div>
                    </div>
                    <div class="pill-mini {selected["entry_color"]}">{selected["entry_quality"]}</div>
                </div>

                <div class="decision-row">
                    <div class="decision-label-wrap">
                        <div class="decision-icon">🛡️</div>
                        <div>
                            <div class="decision-title">Risk</div>
                            <div class="decision-sub">Overall risk level of this setup</div>
                        </div>
                    </div>
                    <div class="pill-mini {selected["risk_color"]}">{selected["risk_level"]}</div>
                </div>

                <div class="decision-row">
                    <div class="decision-label-wrap">
                        <div class="decision-icon">👀</div>
                        <div>
                            <div class="decision-title">What To Do</div>
                            <div class="decision-sub">Recommended action now</div>
                        </div>
                    </div>
                    <div class="pill-mini {selected["what_color"]}">{selected["what_to_do"]}</div>
                </div>

                <div class="decision-row">
                    <div class="decision-label-wrap">
                        <div class="decision-icon">💰</div>
                        <div>
                            <div class="decision-title">Profit Status / Exit</div>
                            <div class="decision-sub">Should you take profit or exit?</div>
                        </div>
                    </div>
                    <div class="pill-mini {selected["profit_color"]}">{selected["profit_status"]}</div>
                </div>

                <div style="margin-top:22px; border-top:1px solid rgba(255,255,255,0.10); padding-top:18px;">
                    <div class="compact-section-title">📋 Action Plan / План сделки</div>
                    <div class="plan-grid-modern">
                        <div class="plan-tile border-blue">
                            <div class="plan-title positive-text">Entry / Вход</div>
                            <div class="plan-value">{plan["entry"]}</div>
                            <div class="plan-desc">{plan_explanation("entry", selected["action"])}</div>
                        </div>
                        <div class="plan-tile border-red">
                            <div class="plan-title negative-text">Stop Loss / Защитный стоп</div>
                            <div class="plan-value">{plan["stop"]}</div>
                            <div class="plan-desc">{plan_explanation("stop", selected["action"])}</div>
                        </div>
                        <div class="plan-tile border-green">
                            <div class="plan-title positive-text">First Profit Target / Первая цель</div>
                            <div class="plan-value">{plan["tp1"]}</div>
                            <div class="plan-desc">{plan_explanation("target1", selected["action"])}</div>
                        </div>
                        <div class="plan-tile border-green">
                            <div class="plan-title positive-text">Second Profit Target / Вторая цель</div>
                            <div class="plan-value">{plan["tp2"]}</div>
                            <div class="plan-desc">{plan_explanation("target2", selected["action"])}</div>
                        </div>
                    </div>
                    <div class="info-box" style="margin-top:14px;">
                        <b>How to read this / Как читать:</b><br>
                        🇬🇧 These are reference levels from the current price. They do not mean “buy now”. If the coin is already bought, they help you think about risk and profit zones.<br><br>
                        🇷🇺 Это ориентиры от текущей цены. Они не означают “покупай сейчас”. Если монета уже куплена, они помогают понять риск и зоны фиксации прибыли.<br><br>
                        🇬🇧 {plan["note_en"]}<br>
                        🇷🇺 {plan["note_ru"]}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)


with tab_opps:
    # ---------- PART 2: REAL OPPORTUNITY SCANNER ----------
    st.divider()
    st.subheader("🚀 Best Opportunities / Лучшие варианты")
    st.caption("Scanner checks all loaded coins and ranks realistic opportunities — not only raw setup score.")

    # Rank all loaded coins by Opportunity Score, not only by setup score.
    opportunity_ranked = sorted(signals, key=lambda x: x["opportunity_score"], reverse=True)
    clean_candidates = [s for s in opportunity_ranked if s["category"] in ["🔥 Best Opportunity", "👀 Watchlist Candidate"]]
    pumped_candidates = [s for s in opportunity_ranked if "Already Pumped" in s["category"]]
    risky_candidates = [s for s in opportunity_ranked if "Risky" in s["category"] or "Low Priority" in s["category"]]

    best_opp = clean_candidates[0] if clean_candidates else opportunity_ranked[0]

    pos_html = "<br>".join([f"✅ {x}" for x in best_opp["positive_reasons"]])
    neg_html = "<br>".join([f"⚠️ {x}" for x in best_opp["negative_reasons"]])

    html(f"""
    <div class="glass-card" style="margin-top:14px;">
        <div style="display:flex; justify-content:space-between; gap:18px; align-items:flex-start; flex-wrap:wrap;">
            <div>
                <div class="compact-section-title" style="font-size:24px; margin-bottom:8px;">🏆 Best Opportunity Now</div>
                <div class="small-muted">Best realistic setup found across <b>{len(signals)}</b> loaded coins.</div>
            </div>
            <span class="badge {best_opp['category_color']}" style="margin:0;">{best_opp['category']}</span>
        </div>

        <div class="decision-top" style="grid-template-columns:minmax(260px,1fr) 170px; margin-top:18px;">
            <div>
                <div class="coin-title-small">{best_opp['symbol']} — {best_opp['coin']}</div>
                <div class="price-main" style="margin-top:10px;">{fmt(best_opp['price'])} {currency.upper()}</div>
                <div class="{'metric-positive' if best_opp['24h'] >= 0 else 'metric-negative'}">24h: {best_opp['24h']:.2f}%</div>
            </div>
            <div class="score-box" style="min-width:210px;">
                <div class="score-box-label">🏆 Opportunity Score</div>
                <div class="score-box-value" style="color:#86efac;">{best_opp['opportunity_score']}/100</div>
                <div style="color:#cbd5e1; font-size:13px; line-height:1.35; margin-top:8px;">
                    <b>Setup Quality:</b> {best_opp['score']}/100<br>
                    <span style="color:#94a3b8;">How good this coin looks by itself.</span><br><br>
                    <b>Market Ranking:</b> Best match now<br>
                    <span style="color:#94a3b8;">Compared with other scanned coins.</span>
                </div>
            </div>
        </div>

        <div class="score-intro-box" style="margin-top:10px; margin-bottom:12px;">
            <b>Opportunity Score = Setup Quality + Market Ranking</b><br>
            <span style="color:#cbd5e1;">Setup Quality shows whether this coin is strong by itself. Market Ranking shows whether it is better than other scanned coins right now.</span><br>
            <span style="color:#aab4cf;">Opportunity Score = качество самой монеты + сравнение с другими монетами рынка.</span>
        </div>

        <div class="reason-mini-summary" style="grid-template-columns:repeat(2,1fr);">
            <div class="reason-summary-box">
                <div class="reason-summary-title">Why it is interesting / Почему интересно</div>
                {pos_html}
            </div>
            <div class="reason-summary-box">
                <div class="reason-summary-title">What can block it / Что мешает</div>
                {neg_html}
            </div>
        </div>

        <div class="info-box">
            <b>Action:</b> {best_opp['what_to_do']}<br>
            <b>Entry:</b> {best_opp['entry_quality']} &nbsp; | &nbsp;
            <b>Risk:</b> {best_opp['risk_level']} &nbsp; | &nbsp;
            <b>Profit Status:</b> {best_opp['profit_status']}<br><br>
            🇷🇺 Это не “точно покупать”. Это лучший setup среди загруженных монет по текущим данным: импульс, объём, ликвидность, риск и отсутствие сильного перегрева.
        </div>
    </div>
    """)

    # Category overview
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Best/Watch candidates", len(clean_candidates))
    c2.metric("💰 Already pumped", len(pumped_candidates))
    c3.metric("⚠️ Risky / low priority", len(risky_candidates))
    c4.metric("🌍 Coins scanned", len(signals))

    st.subheader("🔎 Opportunity Scanner Results")
    st.caption("Sorted by Opportunity Score. The scanner still shows all loaded coins, but separates good setups from risky/pumped coins.")

    show_group = st.selectbox(
        "Show group",
        ["Best + Watchlist", "All coins", "Already pumped", "Risky / Low priority"],
        index=0
    )

    if show_group == "Best + Watchlist":
        table_source = clean_candidates
    elif show_group == "Already pumped":
        table_source = pumped_candidates
    elif show_group == "Risky / Low priority":
        table_source = risky_candidates
    else:
        table_source = opportunity_ranked

    # Optional table threshold: applies only to visible table, not to best-opportunity ranking.
    table_source = [s for s in table_source if s["opportunity_score"] >= min_score_filter]

    rows = []
    for s in table_source[:50]:
        rows.append({
            "Coin": f"{s['symbol']} — {s['coin']}",
            "Price": f"{fmt(s['price'])} {currency.upper()}",
            "Opportunity": s["opportunity_score"],
            "Setup": s["score"],
            "Category": s["category"],
            "1h %": round(s["1h"], 2),
            "24h %": round(s["24h"], 2),
            "7d %": round(s["7d"], 2),
            "Vol/MCap": f"{s['volume_ratio']:.2%}",
            "Entry": s["entry_quality"].replace("Wait For Better Entry", "Wait").replace("Bad Timing", "Bad"),
            "Risk": s["risk_level"],
            "Action": s["what_to_do"],
        })

    if not rows:
        st.warning("No coins in this group match the current Minimum Score filter. Lower Minimum Score or choose another group.")
    else:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    csv_df = pd.DataFrame(rows)
    csv = csv_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Opportunity Scanner CSV",
        data=csv,
        file_name="koshka_opportunity_scanner.csv",
        mime="text/csv"
    )


with tab_market:
    # ---------- MACRO SECTION ----------
    st.divider()
    st.subheader("🌐 Market Overview / Обзор рынка")
    st.caption("Bottom section: macro context for all coins — useful after reviewing selected coin and opportunities.")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        if fg:
            val = fg["value"]
            label = fg["label"]

            if val <= 24:
                fg_color = "red"
                simple_status = "Extreme Fear"
                simple_desc = "Рынок боится. Иногда это даёт хорошие точки для осторожного накопления."
                emoji = "😱"
            elif val <= 44:
                fg_color = "yellow"
                simple_status = "Fear"
                simple_desc = "Рынок осторожный. Лучше не спешить и ждать подтверждения."
                emoji = "😰"
            elif val <= 55:
                fg_color = "yellow"
                simple_status = "Neutral"
                simple_desc = "Рынок спокойный. Сильного общего сигнала сейчас нет."
                emoji = "😐"
            elif val <= 74:
                fg_color = "green"
                simple_status = "Greed"
                simple_desc = "Импульс есть, но риск отката уже выше."
                emoji = "😏"
            else:
                fg_color = "red"
                simple_status = "Extreme Greed"
                simple_desc = "Рынок может быть перегрет. Осторожно с новыми покупками."
                emoji = "🤑"

            html(f"""
            <div class="clean-macro-card">
                <div class="clean-macro-title">{emoji} Fear & Greed</div>
                <div class="clean-macro-value">{val}</div>
                <span class="clean-macro-status {fg_color}">{simple_status}</span>
                <div class="clean-macro-desc">{simple_desc}</div>
            </div>
            """)
        else:
            html("""
            <div class="clean-macro-card">
                <div class="clean-macro-title">😐 Fear & Greed</div>
                <div class="clean-macro-value">N/A</div>
                <div class="clean-macro-desc">Данные сейчас недоступны.</div>
            </div>
            """)

    with m2:
        if btc_global and btc_global["btc_dominance"]:
            dom = btc_global["btc_dominance"]

            if dom >= 55:
                dom_color = "red"
                dom_status = "BTC Strong"
                dom_desc = "Bitcoin сейчас сильнее. Альтам может быть сложнее расти."
                dom_emoji = "🟠"
            elif dom >= 48:
                dom_color = "yellow"
                dom_status = "Mixed"
                dom_desc = "Смешанный рынок. Нет явного преимущества BTC или альтов."
                dom_emoji = "⚖️"
            else:
                dom_color = "green"
                dom_status = "Alt Friendly"
                dom_desc = "Деньги больше идут в альты. Для альткоинов условия лучше."
                dom_emoji = "🚀"

            html(f"""
            <div class="clean-macro-card">
                <div class="clean-macro-title">{dom_emoji} BTC Dominance</div>
                <div class="clean-macro-value">{dom}%</div>
                <span class="clean-macro-status {dom_color}">{dom_status}</span>
                <div class="clean-macro-desc">{dom_desc}</div>
            </div>
            """)
        else:
            html("""
            <div class="clean-macro-card">
                <div class="clean-macro-title">🟠 BTC Dominance</div>
                <div class="clean-macro-value">N/A</div>
                <div class="clean-macro-desc">Данные сейчас недоступны.</div>
            </div>
            """)

    with m3:
        if btc_global and btc_global["total_mcap"]:
            mcap = btc_global["total_mcap"]
            html(f"""
            <div class="clean-macro-card">
                <div class="clean-macro-title">💰 Crypto Market Cap</div>
                <div class="clean-macro-value">${fmt(mcap)}</div>
                <span class="clean-macro-status blue">Market Size</span>
                <div class="clean-macro-desc">Общий размер всего крипторынка.</div>
            </div>
            """)
        else:
            html("""
            <div class="clean-macro-card">
                <div class="clean-macro-title">💰 Market Cap</div>
                <div class="clean-macro-value">N/A</div>
                <div class="clean-macro-desc">Данные сейчас недоступны.</div>
            </div>
            """)

    with m4:
        if market_bias == "BTC_SEASON":
            bias_color = "red"
            bias_title = "BTC Season"
            bias_desc = "Сейчас Bitcoin выглядит сильнее большинства альтов."
            bias_emoji = "🟠"
        elif market_bias == "ALT_FRIENDLY":
            bias_color = "green"
            bias_title = "Altcoin Friendly"
            bias_desc = "Условия для альткоинов выглядят лучше."
            bias_emoji = "🚀"
        elif market_bias == "OVERHEATED":
            bias_color = "red"
            bias_title = "Overheated"
            bias_desc = "Рынок может быть перегрет. Не стоит гнаться за свечами."
            bias_emoji = "🔥"
        elif market_bias == "ACCUMULATION":
            bias_color = "green"
            bias_title = "Accumulation"
            bias_desc = "Рынок в страхе. Можно искать осторожные точки входа."
            bias_emoji = "🧊"
        elif market_bias == "MIXED":
            bias_color = "yellow"
            bias_title = "Mixed Market"
            bias_desc = "Нет сильного направления. Лучше выбирать только лучшие setups."
            bias_emoji = "⚖️"
        else:
            bias_color = "yellow"
            bias_title = "Unknown"
            bias_desc = "Часть данных недоступна."
            bias_emoji = "🧭"

        html(f"""
        <div class="clean-macro-card">
            <div class="clean-macro-title">{bias_emoji} Market Bias</div>
            <div class="clean-macro-value" style="font-size:34px;">{bias_title}</div>
            <span class="clean-macro-status {bias_color}">Market Mode</span>
            <div class="clean-macro-desc">{bias_desc}</div>
        </div>
        """)

    html(f"""
    <div class="clean-summary">
        <b>🔍 Короткий вывод:</b> {bias_desc}
    </div>
    """)

    st.divider()



# ---------- REFRESH ----------
st.divider()

if st.button("🔄 Refresh Market Data"):
    st.cache_data.clear()
    st.rerun()

st.caption("Educational only. Not financial advice")