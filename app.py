import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Koshka Crypto AI Agent", layout="wide")

st.markdown("""
<style>
section[data-testid="stSidebar"] { width: 360px !important; }
section[data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, #111827, #1f2937);
}
.hero {
    background: linear-gradient(135deg, #111827, #1f2937);
    padding: 28px;
    border-radius: 28px;
    margin-bottom: 24px;
}
.card {
    background: linear-gradient(135deg, #1f1f29, #28283a);
    padding: 24px;
    border-radius: 24px;
    margin-bottom: 16px;
}
.decision-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    padding: 28px;
    border-radius: 28px;
    border: 1px solid #334155;
}
.market-card {
    background: linear-gradient(135deg, #18181b, #27272a);
    padding: 24px;
    border-radius: 24px;
    border: 1px solid #3f3f46;
}
.coin-symbol {
    font-size: 44px;
    font-weight: 900;
}
.big-price {
    font-size: 34px;
    font-weight: 900;
    margin-top: 12px;
}
.badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 14px;
}
.badge-green { background:#064e3b; color:#86efac; }
.badge-yellow { background:#713f12; color:#fde68a; }
.badge-red { background:#7f1d1d; color:#fca5a5; }
.small-muted { color: #9ca3af; font-size: 14px; }
.title {
    font-size: 44px;
    font-weight: 950;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
cat_black = Path("cat_black.png")
cat_orange = Path("cat_orange.png")

h1, h2, h3 = st.columns([1, 4, 1])

with h1:
    if cat_black.exists():
        st.image(str(cat_black), width=130)

with h2:
    st.markdown("""
    <div class="hero">
        <div class="title">Koshka Crypto AI Agent</div>
        <p class="small-muted">
        Early-signal crypto scanner. Avoids chasing coins that already pumped.
        Educational only — not financial advice.
        </p>
    </div>
    """, unsafe_allow_html=True)

with h3:
    if cat_orange.exists():
        st.image(str(cat_orange), width=130)

# ---------- SIDEBAR ----------
st.sidebar.markdown("""
# ⚙️ Scanner Settings
🟢 **LIVE MARKET MODE**  
Real-time crypto market scan
""")

currency = st.sidebar.selectbox("💱 Currency", ["usd", "aed", "eur", "gbp", "rub"], index=1)
risk_mode = st.sidebar.selectbox("⚠️ Risk mode", ["Conservative", "Balanced", "Aggressive"], index=1)
scan_size = st.sidebar.slider("🌍 Market scan size", 20, 200, 100, step=10)

# ---------- HELPERS ----------
def format_price(price):
    if price is None:
        return "N/A"
    if price >= 1000:
        return f"{price:,.0f}"
    if price >= 1:
        return f"{price:.2f}"
    return f"{price:.5f}"

def signal_badge(score):
    if score >= 8:
        return "STRONG SETUP", "badge-green"
    elif score >= 5:
        return "WATCH", "badge-yellow"
    return "RISKY / WEAK", "badge-red"

@st.cache_data(ttl=300)
def get_market_data(currency, scan_size):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": scan_size,
        "page": 1,
        "price_change_percentage": "1h,24h,7d"
    }
    headers = {"accept": "application/json", "User-Agent": "Koshka-Crypto-AI-Agent"}
    response = requests.get(url, params=params, headers=headers, timeout=20)

    if response.status_code == 429:
        return {"error": "API rate limit reached. Please wait 5 minutes and refresh."}
    if response.status_code != 200:
        return {"error": f"API error: {response.status_code}"}

    market = []
    for coin in response.json():
        market.append({
            "id": coin.get("id"),
            "name": coin.get("name"),
            "symbol": coin.get("symbol", "").upper(),
            "price": coin.get("current_price"),
            "market_cap": coin.get("market_cap") or 0,
            "volume": coin.get("total_volume") or 0,
            "change_1h": coin.get("price_change_percentage_1h_in_currency") or 0,
            "change_24h": coin.get("price_change_percentage_24h_in_currency") or 0,
            "change_7d": coin.get("price_change_percentage_7d_in_currency") or 0,
        })
    return {"data": market}

def score_emerging_setup(coin, risk_mode):
    score = 0
    reasons = []

    c1, c24, c7 = coin["change_1h"], coin["change_24h"], coin["change_7d"]
    market_cap, volume = coin["market_cap"], coin["volume"]

    if risk_mode == "Conservative":
        max_24h, max_7d, min_market_cap, min_volume = 5, 18, 1_000_000_000, 100_000_000
    elif risk_mode == "Aggressive":
        max_24h, max_7d, min_market_cap, min_volume = 9, 35, 200_000_000, 20_000_000
    else:
        max_24h, max_7d, min_market_cap, min_volume = 6, 25, 500_000_000, 50_000_000

    if 0.3 <= c1 <= 2.5:
        score += 3
        reasons.append("early 1h momentum")
    if 1 <= c24 <= max_24h:
        score += 4
        reasons.append("healthy 24h move")
    if -5 <= c7 <= 3 and c24 > 0:
        score += 2
        reasons.append("possible recovery setup")
    if market_cap >= min_market_cap and volume >= min_volume:
        score += 2
        reasons.append("good liquidity")

    if c24 > max_24h:
        score -= 3
        reasons.append("24h may be overextended")
    if c24 > 10:
        score -= 4
        reasons.append("too pumped recently")
    if c7 > max_7d:
        score -= 4
        reasons.append("7d trend overheated")
    if c24 < -5:
        score -= 3
        reasons.append("falling momentum risk")

    if not reasons:
        reasons.append("no strong early setup")

    return score, reasons

def get_top_signals(market, risk_mode, limit=5):
    scored = []
    for coin in market:
        score, reasons = score_emerging_setup(coin, risk_mode)
        scored.append({**coin, "score": score, "reasons": reasons})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:limit]

def get_coin_decision(coin, risk_mode):
    if not coin:
        return "NO DATA ⚠️", "Live data unavailable.", 0, [], 0

    score, reasons = score_emerging_setup(coin, risk_mode)
    confidence = min(max(score * 10, 40), 90)

    if score >= 8:
        return "STRONG SETUP 🚀", "Selected coin shows a strong early setup.", confidence, reasons, score
    elif score >= 5:
        return "WATCH 👀", "Some positive signals, but not enough for aggressive action.", confidence, reasons, score
    return "CAUTION ⚠️", "No clean setup right now.", confidence, reasons, score

# ---------- LOAD ----------
with st.spinner("Loading live market data..."):
    market_response = get_market_data(currency, scan_size)

if "error" in market_response:
    st.error(market_response["error"])
    st.info("CoinGecko free API can rate-limit. Wait few minutes, then refresh.")
    market_data = []
else:
    market_data = market_response["data"]

if market_data:
    coin_options = {f"{c['symbol']} — {c['name']}": c for c in market_data}
    selected_label = st.sidebar.selectbox("🎯 Coin for decision", list(coin_options.keys()), index=0)
    selected_coin = coin_options[selected_label]
else:
    selected_coin = None

top_signals = get_top_signals(market_data, risk_mode, 5) if market_data else []
best_signal = top_signals[0] if top_signals else None
decision, reason, confidence, decision_reasons, decision_score = get_coin_decision(selected_coin, risk_mode)

# ---------- SECTION 1: SELECTED COIN + DECISION ----------
st.subheader("🎯 Selected Coin Decision")

left, right = st.columns([1, 1.4])

with left:
    if selected_coin:
        color = "#86efac" if selected_coin["change_24h"] >= 0 else "#f87171"
        arrow = "▲" if selected_coin["change_24h"] >= 0 else "▼"

        st.markdown(f"""
        <div class="decision-card">
            <div class="coin-symbol">{selected_coin['symbol']}</div>
            <h3>{selected_coin['name']}</h3>
            <div class="big-price">{format_price(selected_coin['price'])} {currency.upper()}</div>
            <p style="color:{color}; font-size:20px;">{arrow} {selected_coin['change_24h']:.2f}% / 24h</p>
            <p class="small-muted">1h: {selected_coin['change_1h']:.2f}% | 7d: {selected_coin['change_7d']:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No selected coin data available.")

with right:
    badge_text, badge_class = signal_badge(decision_score)
    st.markdown(f"""
    <div class="decision-card">
        <span class="badge {badge_class}">{badge_text}</span>
        <h2>{decision}</h2>
        <p>{reason}</p>
        <p><b>Setup score:</b> {decision_score}</p>
        <p><b>Confidence:</b> {confidence}%</p>
        <p><b>Why:</b> {', '.join(decision_reasons) if decision_reasons else 'No signal reasons available'}</p>
        <p class="small-muted">Decision is based only on selected coin.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- SECTION 2: MARKET SCANNER ----------
st.subheader("🌍 Market Scanner — Early Signals")

m1, m2 = st.columns([1, 1.4])

with m1:
    if best_signal:
        badge, badge_class = signal_badge(best_signal["score"])
        st.markdown(f"""
        <div class="market-card">
            <span class="badge {badge_class}">{badge}</span>
            <h2>{best_signal['symbol']} — {best_signal['name']}</h2>
            <div class="big-price">{format_price(best_signal['price'])} {currency.upper()}</div>
            <p><b>1h:</b> {best_signal['change_1h']:.2f}% | <b>24h:</b> {best_signal['change_24h']:.2f}% | <b>7d:</b> {best_signal['change_7d']:.2f}%</p>
            <p><b>Score:</b> {best_signal['score']}</p>
            <p><b>Why:</b> {', '.join(best_signal['reasons'])}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write("No early signal found.")

with m2:
    if top_signals:
        rows = []
        for coin in top_signals:
            label, _ = signal_badge(coin["score"])
            rows.append({
                "Coin": f"{coin['symbol']} — {coin['name']}",
                "Price": f"{format_price(coin['price'])} {currency.upper()}",
                "1h %": round(coin["change_1h"], 2),
                "24h %": round(coin["change_24h"], 2),
                "7d %": round(coin["change_7d"], 2),
                "Score": coin["score"],
                "Signal": label,
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

if top_signals:
    fig = px.bar(
        x=[c["symbol"] for c in top_signals],
        y=[c["score"] for c in top_signals],
        labels={"x": "Coin", "y": "Setup Score"},
        title="Top early-signal setup scores"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- EXPORT ----------
st.subheader("📤 Export Report")

report = f"""
Koshka Crypto AI Agent Report
Generated: {datetime.now()}

Currency: {currency.upper()}
Risk mode: {risk_mode}
Scan size: Top {scan_size}

Selected coin:
{selected_coin}

Decision:
{decision}
Reason: {reason}
Setup score: {decision_score}
Confidence: {confidence}%
Why: {decision_reasons}

Best early signal:
{best_signal}

Top 5 signals:
{top_signals}

Disclaimer:
This is not financial advice. Educational early-signal scanner only.
"""

st.download_button("Download Report", report, file_name="koshka_crypto_ai_report.txt")

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()