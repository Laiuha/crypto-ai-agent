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
    background: linear-gradient(180deg, #171720, #252538);
}
.card {
    background: linear-gradient(135deg, #1f1f29, #28283a);
    padding: 22px;
    border-radius: 22px;
    margin-bottom: 16px;
}
.metric-card {
    background: #1f1f29;
    padding: 18px;
    border-radius: 18px;
    min-height: 145px;
}
.coin-symbol { font-size: 32px; font-weight: 800; }
.big-price { font-size: 28px; font-weight: 800; margin-top: 12px; }
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 14px;
}
.badge-green { background:#064e3b; color:#86efac; }
.badge-yellow { background:#713f12; color:#fde68a; }
.badge-red { background:#7f1d1d; color:#fca5a5; }
.small-muted { color: #9ca3af; font-size: 14px; }
.koshka-title {
    font-size: 42px;
    font-weight: 900;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CAT HEADER ----------------
cat_black = Path("cat_black.png")
cat_orange = Path("cat_orange.png")

c1, c2, c3 = st.columns([1, 3, 1])

with c1:
    if cat_black.exists():
        st.image(str(cat_black), width=150)

with c2:
    st.markdown("<div class='koshka-title'>🐈‍⬛ Koshka Crypto AI Agent</div>", unsafe_allow_html=True)
    st.caption("Early-signal crypto scanner. Avoids chasing coins that already pumped. Educational only — not financial advice.")

with c3:
    if cat_orange.exists():
        st.image(str(cat_orange), width=150)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("""
# ⚙️ AI Scanner Settings
Customize your market scanner

🟢 **LIVE MARKET MODE**  
Scanning real-time crypto data
""")

currency = st.sidebar.selectbox(
    "💱 Currency",
    ["usd", "aed", "eur", "gbp", "rub"],
    index=1
)

risk_mode = st.sidebar.selectbox(
    "⚠️ Risk mode",
    ["Conservative", "Balanced", "Aggressive"],
    index=1
)

scan_size = st.sidebar.slider(
    "🌍 Market scan size",
    20, 200, 100, step=10
)

coin_map = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "Cardano": "cardano",
    "Dogecoin": "dogecoin",
    "TRON": "tron",
    "Polkadot": "polkadot",
    "Chainlink": "chainlink",
    "Litecoin": "litecoin",
    "Avalanche": "avalanche-2",
    "Shiba Inu": "shiba-inu",
    "Toncoin": "the-open-network",
    "Polygon": "matic-network"
}

symbol_map = {
    "Bitcoin": "BTC",
    "Ethereum": "ETH",
    "Solana": "SOL",
    "BNB": "BNB",
    "XRP": "XRP",
    "Cardano": "ADA",
    "Dogecoin": "DOGE",
    "TRON": "TRX",
    "Polkadot": "DOT",
    "Chainlink": "LINK",
    "Litecoin": "LTC",
    "Avalanche": "AVAX",
    "Shiba Inu": "SHIB",
    "Toncoin": "TON",
    "Polygon": "MATIC"
}

selected_coin = st.sidebar.selectbox(
    "🪙 Coin for decision",
    list(coin_map.keys()),
    index=0
)

selected_coins = [selected_coin]

# ---------------- HELPERS ----------------
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

    headers = {
        "accept": "application/json",
        "User-Agent": "Koshka-Crypto-AI-Agent"
    }

    response = requests.get(url, params=params, headers=headers, timeout=20)

    if response.status_code == 429:
        return {"error": "API rate limit reached. Please wait 5 minutes and refresh."}

    if response.status_code != 200:
        return {"error": f"API error: {response.status_code}"}

    data = response.json()

    market = []
    for coin in data:
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


def get_selected_coin_from_market(market, selected_coin):
    coin_id = coin_map[selected_coin]

    for coin in market:
        if coin["id"] == coin_id:
            return {
                "name": selected_coin,
                "symbol": symbol_map.get(selected_coin, coin["symbol"]),
                "price": coin["price"],
                "change_1h": coin["change_1h"],
                "change_24h": coin["change_24h"],
                "change_7d": coin["change_7d"],
                "market_cap": coin["market_cap"],
                "volume": coin["volume"]
            }

    return None


def score_emerging_setup(coin, risk_mode):
    score = 0
    reasons = []

    c1 = coin["change_1h"]
    c24 = coin["change_24h"]
    c7 = coin["change_7d"]
    market_cap = coin["market_cap"]
    volume = coin["volume"]

    if risk_mode == "Conservative":
        max_24h = 5
        max_7d = 18
        min_market_cap = 1_000_000_000
        min_volume = 100_000_000
    elif risk_mode == "Aggressive":
        max_24h = 9
        max_7d = 35
        min_market_cap = 200_000_000
        min_volume = 20_000_000
    else:
        max_24h = 6
        max_7d = 25
        min_market_cap = 500_000_000
        min_volume = 50_000_000

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
        reasons.append("24h move may be overextended")

    if c24 > 10:
        score -= 4
        reasons.append("too pumped recently")

    if c7 > max_7d:
        score -= 4
        reasons.append("7d trend looks overheated")

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
        return "NO DATA ⚠️", "Live data is unavailable.", 0

    score, reasons = score_emerging_setup(coin, risk_mode)

    confidence = min(max(score * 10, 40), 90)

    if score >= 8:
        return "STRONG SETUP 🚀", "Selected coin shows a strong early setup.", confidence
    elif score >= 5:
        return "WATCH 👀", "Selected coin has some positive signals, but not enough for aggressive action.", confidence
    else:
        return "CAUTION ⚠️", "Selected coin does not show a strong clean setup right now.", confidence


# ---------------- LOAD DATA ----------------
with st.spinner("Loading live market data..."):
    market_response = get_market_data(currency, scan_size)

if "error" in market_response:
    st.error(market_response["error"])
    st.info("Tip: CoinGecko free API can rate-limit. Wait a few minutes, then refresh.")
    market_data = []
else:
    market_data = market_response["data"]

selected_data = get_selected_coin_from_market(market_data, selected_coin) if market_data else None
top_signals = get_top_signals(market_data, risk_mode, 5) if market_data else []
emerging_best = top_signals[0] if top_signals else None
decision, reason, confidence = get_coin_decision(selected_data, risk_mode)

# ---------------- SELECTED COIN ----------------
st.subheader("📊 Selected Coin")

if selected_data:
    color = "#86efac" if selected_data["change_24h"] >= 0 else "#f87171"
    arrow = "▲" if selected_data["change_24h"] >= 0 else "▼"

    st.markdown(f"""
    <div class="metric-card">
        <div class="coin-symbol">{selected_data['symbol']}</div>
        <div class="big-price">{format_price(selected_data['price'])} {currency.upper()}</div>
        <div style="color:{color}; font-size:18px; margin-top:12px;">
            {arrow} {selected_data['change_24h']:.2f}% / 24h
        </div>
        <p class="small-muted">
            1h: {selected_data['change_1h']:.2f}% | 7d: {selected_data['change_7d']:.2f}%
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("No selected coin data available. Increase market scan size or refresh later.")

# ---------------- BEST SIGNAL ----------------
st.subheader("🌱 Best Early Signal From Market")

if emerging_best:
    badge_text, badge_class = signal_badge(emerging_best["score"])

    st.markdown(f"""
    <div class="card">
        <span class="badge {badge_class}">{badge_text}</span>
        <h2>{emerging_best['symbol']} — {emerging_best['name']}</h2>
        <div class="big-price">{format_price(emerging_best['price'])} {currency.upper()}</div>
        <p><b>1h:</b> {emerging_best['change_1h']:.2f}% | 
           <b>24h:</b> {emerging_best['change_24h']:.2f}% | 
           <b>7d:</b> {emerging_best['change_7d']:.2f}%</p>
        <p><b>Setup score:</b> {emerging_best['score']}</p>
        <p><b>Why this coin:</b> {', '.join(emerging_best['reasons'])}</p>
        <p class="small-muted">Prefers moderate early movement and penalizes overheated assets.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.write("No early signal found.")

# ---------------- TOP 5 TABLE ----------------
if top_signals:
    st.subheader("🔥 Top 5 Early Signals")

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
            "Why": ", ".join(coin["reasons"])
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ---------------- CHART ----------------
if top_signals:
    st.subheader("📈 Top Signals Comparison")

    fig = px.bar(
        x=[c["symbol"] for c in top_signals],
        y=[c["score"] for c in top_signals],
        labels={"x": "Coin", "y": "Setup Score"},
        title="Top early-signal setup scores"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- DECISION ----------------
st.subheader("🤖 Decision for Selected Coin")

st.markdown(f"""
<div class="card">
    <h2>{decision}</h2>
    <p>{reason}</p>
    <p><b>Confidence:</b> {confidence}%</p>
    <p class="small-muted">Decision is based only on the selected coin, not on a basket average.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- EXPORT ----------------
st.subheader("📤 Export Report")

report = f"""
Koshka Crypto AI Agent Report
Generated: {datetime.now()}

Currency: {currency.upper()}
Risk mode: {risk_mode}
Scan size: Top {scan_size}

Selected coin:
{selected_data}

Best early signal:
{emerging_best}

Top 5 signals:
{top_signals}

Decision:
{decision}
Reason: {reason}
Confidence: {confidence}%

Disclaimer:
This is not financial advice. It is an educational early-signal market scanner.
"""

st.download_button(
    "Download Report",
    report,
    file_name="koshka_crypto_ai_report.txt"
)

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()