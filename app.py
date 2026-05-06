import streamlit as st
import requests
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Koshka Crypto AI Agent",
    page_icon="🐈",
    layout="wide"
)

# ---------- CSS ----------
st.markdown("""
<style>
.block-container { padding-top: 2rem; }

.hero {
    background: linear-gradient(135deg,#1a1f2e,#232b45);
    padding: 28px;
    border-radius: 28px;
    margin-bottom: 24px;
}

.title {
    font-size: 52px;
    font-weight: 900;
    line-height: 1.05;
}

.subtitle {
    font-size: 20px;
    color: #b0b8d1;
    margin-top: 12px;
}

.card {
    background: linear-gradient(135deg,#1c2233,#252f48);
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 18px;
}

.metric-text {
    font-size: 38px;
    font-weight: 800;
}

.green { color:#4ade80; }
.red { color:#f87171; }
.muted { color:#b0b8d1; font-size:15px; }

.badge {
    display:inline-block;
    padding:7px 14px;
    border-radius:999px;
    font-weight:800;
    font-size:14px;
}

.badge-green { background:#064e3b; color:#86efac; }
.badge-yellow { background:#713f12; color:#fde68a; }
.badge-red { background:#7f1d1d; color:#fca5a5; }

.help-card {
    background: linear-gradient(135deg,#111827,#1f2937);
    border-radius: 18px;
    padding: 16px;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
cat_black = Path("cat_black.png")
cat_orange = Path("cat_orange.png")

h1, h2 = st.columns([1, 5])

with h1:
    if cat_black.exists():
        st.image(str(cat_black), width=150)

with h2:
    st.markdown("""
    <div class="hero">
        <div class="title">Koshka Crypto AI Agent</div>
        <div class="subtitle">
        Early-signal crypto scanner. Avoids chasing coins that already pumped.
        Educational only — not financial advice.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- SETTINGS ----------
st.subheader("⚙️ Scanner Settings")

s1, s2, s3 = st.columns(3)

with s1:
    currency = st.selectbox("💱 Currency", ["usd", "aed", "eur", "gbp", "rub"], index=1)

with s2:
    risk_mode = st.selectbox("⚠️ Risk Mode", ["Conservative", "Balanced", "Aggressive"], index=1)

with s3:
    scan_size = st.selectbox("🌍 Market Scan Size", [50, 100, 150, 200], index=1)

# ---------- HELP AS EXPANDABLE QUESTION MARK ----------
with st.expander("❓ Help / How it works"):
    st.markdown("""
    <div class="help-card">

    **Currency** — display currency.

    **Risk Mode**
    - **Conservative** → safer signals
    - **Balanced** → normal mode
    - **Aggressive** → earlier/riskier signals

    **Market Scan Size** — number of coins scanned.

    **AI Decisions**
    - 🚀 **STRONG SETUP** → strong early signal
    - 👀 **WATCH** → interesting, but not confirmed
    - ⚠️ **CAUTION** → weak or risky setup

    **Best Early Signal** — best current setup across scanned market.

    Educational only. Not financial advice.

    </div>
    """, unsafe_allow_html=True)

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
        "User-Agent": "Koshka-Crypto-AI-Agent"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=20)

        if response.status_code == 429:
            return {"error": "API rate limit reached. Wait 5 minutes and refresh."}

        if response.status_code != 200:
            return {"error": f"API error: {response.status_code}"}

        return {"data": response.json()}

    except Exception as e:
        return {"error": f"Connection error: {e}"}

market_response = load_market(currency, scan_size)

if "error" in market_response:
    st.error(market_response["error"])
    st.info("CoinGecko free API can rate-limit. Wait a few minutes, then refresh.")
    st.stop()

market_data = market_response["data"]

# ---------- HELPERS ----------
def format_price(value):
    if value is None:
        return "N/A"
    if value >= 1000:
        return f"{value:,.0f}"
    if value >= 1:
        return f"{value:,.2f}"
    return f"{value:.6f}"

def get_change(coin, key):
    return coin.get(key) or 0

def calculate_score(coin):
    score = 0
    reasons = []

    ch1 = get_change(coin, "price_change_percentage_1h_in_currency")
    ch24 = get_change(coin, "price_change_percentage_24h")
    ch7 = get_change(coin, "price_change_percentage_7d_in_currency")
    market_cap = coin.get("market_cap") or 0
    volume = coin.get("total_volume") or 0

    if risk_mode == "Conservative":
        max24, max7, min_cap, min_vol = 5, 18, 1_000_000_000, 100_000_000
    elif risk_mode == "Aggressive":
        max24, max7, min_cap, min_vol = 9, 35, 200_000_000, 20_000_000
    else:
        max24, max7, min_cap, min_vol = 6, 25, 500_000_000, 50_000_000

    if 0.3 <= ch1 <= 2.5:
        score += 3
        reasons.append("early 1h momentum")

    if 1 <= ch24 <= max24:
        score += 4
        reasons.append("healthy 24h move")

    if -5 <= ch7 <= 3 and ch24 > 0:
        score += 2
        reasons.append("possible recovery setup")

    if market_cap >= min_cap and volume >= min_vol:
        score += 2
        reasons.append("good liquidity")

    if ch24 > max24:
        score -= 3
        reasons.append("24h move may be overextended")

    if ch24 > 10:
        score -= 4
        reasons.append("too pumped recently")

    if ch7 > max7:
        score -= 4
        reasons.append("7d trend looks overheated")

    if ch24 < -5:
        score -= 3
        reasons.append("falling momentum risk")

    if score < 5 and "good liquidity" in reasons:
        reasons.append("but no strong momentum yet")

    if not reasons:
        reasons.append("no strong early setup")

    return score, reasons

def decision_from_score(score):
    if score >= 8:
        return "🚀 STRONG SETUP", "badge-green", 90
    if score >= 5:
        return "👀 WATCH", "badge-yellow", 70
    return "⚠️ CAUTION", "badge-red", 50

# ---------- SIGNALS ----------
signals = []

for coin in market_data:
    score, reasons = calculate_score(coin)

    signals.append({
        "coin": coin["name"],
        "symbol": coin["symbol"].upper(),
        "price": coin["current_price"],
        "change_1h": get_change(coin, "price_change_percentage_1h_in_currency"),
        "change_24h": get_change(coin, "price_change_percentage_24h"),
        "change_7d": get_change(coin, "price_change_percentage_7d_in_currency"),
        "score": score,
        "reasons": reasons,
        "raw": coin
    })

signals = sorted(signals, key=lambda x: x["score"], reverse=True)
top5 = signals[:5]
best = top5[0]

# ---------- SELECTED COIN DECISION ----------
st.subheader("🎯 AI Decision For Selected Coin")

coin_labels = [f"{s['symbol']} — {s['coin']}" for s in signals]
selected_label = st.selectbox("Select coin", coin_labels)
selected = signals[coin_labels.index(selected_label)]

selected_decision, selected_badge_class, selected_confidence = decision_from_score(selected["score"])
selected_color = "green" if selected["change_24h"] >= 0 else "red"

left, right = st.columns([1, 1.4])

with left:
    st.markdown(f"""
    <div class="card">
        <h2>{selected["symbol"]}</h2>
        <h3>{selected["coin"]}</h3>
        <div class="metric-text">{format_price(selected["price"])} {currency.upper()}</div>
        <p class="{selected_color}">
            24h: {selected["change_24h"]:.2f}%
        </p>
        <p class="muted">
            1h: {selected["change_1h"]:.2f}% | 7d: {selected["change_7d"]:.2f}%
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="card">
        <span class="badge {selected_badge_class}">{selected_decision}</span>
        <h2>Decision</h2>
        <p><b>Setup score:</b> {selected["score"]}</p>
        <p><b>Confidence:</b> {selected_confidence}%</p>
        <p><b>Why:</b> {", ".join(selected["reasons"])}</p>
        <p class="muted">Decision is calculated only for the selected coin.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- MARKET SCANNER ----------
st.subheader("🌍 Market Scanner — Early Signals")

best_decision, best_badge_class, best_confidence = decision_from_score(best["score"])
best_color = "green" if best["change_24h"] >= 0 else "red"

b1, b2 = st.columns([3, 1])

with b1:
    st.markdown(f"""
    <div class="card">
        <span class="badge {best_badge_class}">{best_decision}</span>
        <h2>Best Early Signal</h2>
        <h3>{best["symbol"]} — {best["coin"]}</h3>
        <div class="metric-text">{format_price(best["price"])} {currency.upper()}</div>
        <p class="{best_color}">
            24h: {best["change_24h"]:.2f}%
        </p>
        <p class="muted">
            1h: {best["change_1h"]:.2f}% | 7d: {best["change_7d"]:.2f}%
        </p>
        <p><b>Score:</b> {best["score"]}</p>
        <p><b>Why:</b> {", ".join(best["reasons"])}</p>
    </div>
    """, unsafe_allow_html=True)

with b2:
    if cat_orange.exists():
        st.image(str(cat_orange), width=170)

# ---------- TOP 5 BELOW BEST EARLY SIGNAL ----------
st.markdown("### 🔥 Top 5 Early Signals")

table = []
for s in top5:
    d, _, conf = decision_from_score(s["score"])
    table.append({
        "Coin": f"{s['symbol']} — {s['coin']}",
        "Price": f"{format_price(s['price'])} {currency.upper()}",
        "1h %": round(s["change_1h"], 2),
        "24h %": round(s["change_24h"], 2),
        "7d %": round(s["change_7d"], 2),
        "Score": s["score"],
        "Decision": d,
        "Why": ", ".join(s["reasons"])
    })

st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)

# ---------- EXPORT ----------
st.subheader("📤 Export Report")

report = f"""
Koshka Crypto AI Agent Report

Currency: {currency.upper()}
Risk Mode: {risk_mode}
Scan Size: Top {scan_size}

Selected Coin:
{selected}

Selected Decision:
{selected_decision}
Confidence: {selected_confidence}%

Best Early Signal:
{best}

Top 5 Signals:
{top5}

Disclaimer:
Educational only. Not financial advice.
"""

st.download_button("Download Report", report, file_name="koshka_crypto_ai_report.txt")

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()