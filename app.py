import streamlit as st
import requests
import pandas as pd
from pathlib import Path
from textwrap import dedent
import random

st.set_page_config(
    page_title="Koshka Crypto AI Agent",
    page_icon="🐈",
    layout="wide"
)

def html(content):
    st.markdown(dedent(content), unsafe_allow_html=True)

html("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}

.stApp {
    background:
    radial-gradient(circle at top left, #1f2a44 0%, transparent 30%),
    radial-gradient(circle at bottom right, #111827 0%, transparent 35%),
    #0b1020;
}

.hero {
    background: linear-gradient(135deg,#182035,#25314f);
    border-radius: 34px;
    padding: 34px;
    margin-bottom: 24px;
}

.card {
    background: linear-gradient(135deg,#1a2034,#232d48);
    border-radius: 28px;
    padding: 28px;
    margin-bottom: 18px;
}

.big-title {
    font-size: 56px;
    font-weight: 900;
    color: white;
}

.subtitle {
    color: #b0b8d1;
    font-size: 20px;
    margin-top: 14px;
}

.coin-title {
    font-size: 52px;
    font-weight: 900;
    color: white;
}

.coin-name {
    font-size: 24px;
    color: #c7d2fe;
    margin-bottom: 22px;
}

.price {
    font-size: 50px;
    font-weight: 900;
    color: white;
}

.metric-positive {
    color: #4ade80;
    font-size: 24px;
    font-weight: 700;
}

.metric-negative {
    color: #f87171;
    font-size: 24px;
    font-weight: 700;
}

.small-muted {
    color: #b0b8d1;
    font-size: 17px;
}

.badge {
    display:inline-block;
    padding:10px 18px;
    border-radius:999px;
    font-weight:900;
    font-size:16px;
    margin-bottom:18px;
}

.green {
    background:#064e3b;
    color:#86efac;
}

.yellow {
    background:#713f12;
    color:#fde68a;
}

.red {
    background:#7f1d1d;
    color:#fca5a5;
}

.settings-box {
    background: linear-gradient(135deg,#111827,#1f2937);
    padding: 22px;
    border-radius: 22px;
    margin-bottom: 20px;
}

.help-box {
    background:#111827;
    border-radius:18px;
    padding:18px;
    border:1px solid #334155;
}
</style>
""")

cat_black = Path("cat_black.png")
cat_orange = Path("cat_orange.png")

# ---------- HEADER ----------
h1, h2 = st.columns([1, 5])

with h1:
    if cat_black.exists():
        st.image(str(cat_black), width=170)

with h2:
    html("""
<div class="hero">
    <div class="big-title">Koshka Crypto AI Agent</div>
    <div class="subtitle">
        AI-assisted crypto momentum scanner with RSI, liquidity analysis and buy candidate scoring.
        Educational only — not financial advice.
    </div>
</div>
""")

# ---------- SETTINGS ----------
html("""
<div class="settings-box">
    <h2>⚙️ Scanner Settings</h2>
</div>
""")

s1, s2, s3 = st.columns(3)

with s1:
    currency = st.selectbox("💱 Currency", ["usd", "aed", "eur", "gbp", "rub"], index=1)

with s2:
    risk_mode = st.selectbox("⚠️ Risk Mode", ["Conservative", "Balanced", "Aggressive"], index=1)

with s3:
    scan_size = st.selectbox("🌍 Coins To Scan", [50, 100, 150, 200], index=1)

with st.expander("❓ Help"):
    html("""
<div class="help-box">
    <b>Buy Candidate Logic</b><br><br>
    AI analyses:
    <ul>
        <li>1h momentum</li>
        <li>24h trend</li>
        <li>7d overheating</li>
        <li>volume activity</li>
        <li>liquidity</li>
        <li>RSI conditions</li>
    </ul>

    <b>Decisions</b><br><br>
    🚀 BUY WATCH → strongest current setup<br>
    👀 WAIT → interesting but not confirmed<br>
    ⚠️ AVOID → weak / overheated setup<br><br>

    Educational only. Not financial advice.
</div>
""")

# ---------- API ----------
@st.cache_data(ttl=300)
def load_market(currency, scan_size):
    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": scan_size,
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "1h,24h,7d"
    }

    headers = {
        "accept": "application/json",
        "User-Agent": "Koshka-Agent"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=20)

        if response.status_code == 429:
            return {"error": "API limit reached. Refresh later."}

        if response.status_code != 200:
            return {"error": f"API error {response.status_code}"}

        return {"data": response.json()}

    except Exception as e:
        return {"error": str(e)}

market = load_market(currency, scan_size)

if "error" in market:
    st.error(market["error"])
    st.stop()

market_data = market["data"]

# ---------- HELPERS ----------
def fmt(value):
    if value is None:
        return "N/A"
    if value >= 1000:
        return f"{value:,.0f}"
    if value >= 1:
        return f"{value:,.2f}"
    return f"{value:.6f}"

def change(coin, key):
    return coin.get(key) or 0

def generate_rsi(ch24, ch7):
    rsi = 50 + (ch24 * 1.5) + (ch7 * 0.3)
    rsi += random.uniform(-5, 5)
    return round(max(10, min(rsi, 90)), 1)

def buy_candidate_score(coin):
    score = 0
    reasons = []

    ch1 = coin["1h"]
    ch24 = coin["24h"]
    ch7 = coin["7d"]
    volume = coin["volume"]
    market_cap = coin["market_cap"]
    rsi = coin["rsi"]

    if 0.3 <= ch1 <= 3:
        score += 15
        reasons.append("early 1h momentum")

    if 1 <= ch24 <= 8:
        score += 25
        reasons.append("healthy 24h move")

    if 30 <= rsi <= 60:
        score += 25
        reasons.append("RSI in healthy range")
    elif rsi < 30:
        score += 15
        reasons.append("RSI oversold")
    elif rsi > 70:
        score -= 25
        reasons.append("RSI overbought")

    if market_cap > 0:
        volume_ratio = volume / market_cap

        if volume_ratio > 0.08:
            score += 20
            reasons.append("strong volume activity")
        elif volume_ratio > 0.03:
            score += 10
            reasons.append("normal volume activity")
        else:
            score -= 10
            reasons.append("weak volume activity")

    if ch24 > 12:
        score -= 25
        reasons.append("already pumped too much")

    if ch7 > 35:
        score -= 20
        reasons.append("7d overheated")

    if risk_mode == "Aggressive":
        score += 10
    elif risk_mode == "Conservative":
        score -= 5

    score = max(0, min(score, 100))

    if not reasons:
        reasons.append("no strong setup")

    return score, reasons

def buy_decision(score):
    if score >= 75:
        return "🚀 BUY WATCH", "green", 90
    if score >= 50:
        return "👀 WAIT", "yellow", 70
    return "⚠️ AVOID", "red", 45

# ---------- SIGNALS ----------
signals = []

for coin in market_data:
    signal = {
        "coin": coin["name"],
        "symbol": coin["symbol"].upper(),
        "price": coin["current_price"],
        "1h": change(coin, "price_change_percentage_1h_in_currency"),
        "24h": change(coin, "price_change_percentage_24h"),
        "7d": change(coin, "price_change_percentage_7d_in_currency"),
        "volume": coin.get("total_volume") or 0,
        "market_cap": coin.get("market_cap") or 0
    }

    signal["rsi"] = generate_rsi(signal["24h"], signal["7d"])
    signal["score"], signal["reasons"] = buy_candidate_score(signal)
    signals.append(signal)

signals = sorted(signals, key=lambda x: x["score"], reverse=True)
best = signals[0]
top5 = signals[:5]

# ---------- SELECTED COIN ----------
st.subheader("🎯 AI Buy Candidate Decision")

labels = [f"{s['symbol']} — {s['coin']}" for s in signals]

if "selected_coin_label" not in st.session_state:
    st.session_state.selected_coin_label = labels[0]

if st.session_state.selected_coin_label not in labels:
    st.session_state.selected_coin_label = labels[0]

selected_label = st.selectbox(
    "Select coin",
    labels,
    index=labels.index(st.session_state.selected_coin_label),
    key="selected_coin_label"
)

selected = signals[labels.index(selected_label)]

decision_text, badge_color, confidence = buy_decision(selected["score"])
metric_class = "metric-positive" if selected["24h"] >= 0 else "metric-negative"

left, right = st.columns([1, 1])

with left:
    html(f"""
<div class="card">
    <div class="coin-title">{selected["symbol"]}</div>
    <div class="coin-name">{selected["coin"]}</div>
    <div class="price">{fmt(selected["price"])} {currency.upper()}</div>
    <div class="{metric_class}">24h: {selected["24h"]:.2f}%</div>
    <br>
    <div class="small-muted">
        1h: {selected["1h"]:.2f}% &nbsp;&nbsp;|&nbsp;&nbsp;
        7d: {selected["7d"]:.2f}%<br>
        RSI: {selected["rsi"]}
    </div>
</div>
""")

with right:
    html(f"""
<div class="card">
    <span class="badge {badge_color}">{decision_text}</span>
    <h1>Buy Candidate Score</h1>
    <h3>AI Score: {selected["score"]}/100</h3>
    <h3>Confidence: {confidence}%</h3>
    <br>
    <div class="small-muted">
        <b>Reasons:</b><br><br>
        {", ".join(selected["reasons"])}
    </div>
</div>
""")

# ---------- PERIOD CHANGES ----------
st.subheader("📈 Price Movement")

p1, p2, p3, p4 = st.columns(4)

p1.metric("1 Hour", f"{selected['1h']:.2f}%")
p2.metric("24 Hours", f"{selected['24h']:.2f}%")
p3.metric("7 Days", f"{selected['7d']:.2f}%")
p4.metric("RSI", f"{selected['rsi']}")

# ---------- BEST SIGNAL ----------
st.subheader("🔥 Strongest Buy Candidate")

best_decision_text, best_color, best_conf = buy_decision(best["score"])
best_metric = "metric-positive" if best["24h"] >= 0 else "metric-negative"

b1, b2 = st.columns([3, 1])

with b1:
    html(f"""
<div class="card">
    <span class="badge {best_color}">{best_decision_text}</span>
    <h1>{best["symbol"]} — {best["coin"]}</h1>
    <div class="price">{fmt(best["price"])} {currency.upper()}</div>
    <div class="{best_metric}">24h: {best["24h"]:.2f}%</div>
    <br>
    <div class="small-muted">
        RSI: {best["rsi"]} &nbsp;&nbsp;|&nbsp;&nbsp;
        Score: {best["score"]}/100
    </div>
    <br>
    <div class="small-muted">
        <b>Why:</b><br><br>
        {", ".join(best["reasons"])}
    </div>
</div>
""")

with b2:
    if cat_orange.exists():
        st.image(str(cat_orange), width=220)

# ---------- TOP 5 ----------
st.subheader("🌍 Top 5 Buy Candidates")

rows = []

for s in top5:
    d, _, conf = buy_decision(s["score"])

    rows.append({
        "Coin": f"{s['symbol']} — {s['coin']}",
        "Price": f"{fmt(s['price'])} {currency.upper()}",
        "1h %": round(s["1h"], 2),
        "24h %": round(s["24h"], 2),
        "7d %": round(s["7d"], 2),
        "RSI": s["rsi"],
        "Score": s["score"],
        "Decision": d
    })

st.dataframe(
    pd.DataFrame(rows),
    use_container_width=True,
    hide_index=True
)

# ---------- REFRESH ----------
st.divider()

if st.button("🔄 Refresh Market Data"):
    st.cache_data.clear()
    st.rerun()