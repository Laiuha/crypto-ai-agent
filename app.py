import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AI Crypto Market Scanner", layout="wide")

st.markdown("""
<style>
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
.coin-symbol {
    font-size: 32px;
    font-weight: 800;
}
.big-price {
    font-size: 28px;
    font-weight: 800;
    margin-top: 12px;
}
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
.small-muted {
    color: #9ca3af;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Settings")

currency = st.sidebar.selectbox(
    "Currency",
    ["usd", "aed", "eur", "gbp", "rub"],
    index=1
)

risk_mode = st.sidebar.selectbox(
    "Risk mode",
    ["Conservative", "Balanced", "Aggressive"],
    index=1
)

scan_size = st.sidebar.slider(
    "Market scan size",
    20, 100, 50, step=10
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

selected_coins = st.sidebar.multiselect(
    "Selected coins — max 5",
    list(coin_map.keys()),
    default=["Bitcoin", "Ethereum", "Solana"]
)

if len(selected_coins) > 5:
    st.sidebar.error("Please select max 5 coins.")
    st.stop()

if not selected_coins:
    st.sidebar.warning("Select at least one coin.")
    st.stop()


# ---------------- HELPERS ----------------
def format_price(price):
    if price is None:
        return "N/A"
    if price >= 1000:
        return f"{price:,.0f}"
    elif price >= 1:
        return f"{price:.2f}"
    return f"{price:.5f}"


def signal_badge(score):
    if score >= 8:
        return "STRONG SETUP", "badge-green"
    elif score >= 5:
        return "WATCH", "badge-yellow"
    return "RISKY / WEAK", "badge-red"


def get_selected_prices(selected_coins, currency):
    ids = ",".join([coin_map[name] for name in selected_coins])

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ids,
        "vs_currencies": currency,
        "include_24hr_change": "true"
    }

    response = requests.get(url, params=params, timeout=15)

    if response.status_code != 200:
        st.error(f"API error: {response.status_code}. Please refresh.")
        return []

    data = response.json()
    coins = []

    for name in selected_coins:
        coin_id = coin_map[name]

        if coin_id in data and currency in data[coin_id]:
            coins.append({
                "name": name,
                "symbol": symbol_map.get(name, name),
                "price": data[coin_id][currency],
                "change_24h": data[coin_id].get(f"{currency}_24h_change", 0)
            })

    return coins


def get_market_data(currency, scan_size):
    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": scan_size,
        "page": 1,
        "price_change_percentage": "1h,24h,7d"
    }

    response = requests.get(url, params=params, timeout=20)

    if response.status_code != 200:
        st.warning("Global market scan unavailable. Please refresh.")
        return []

    data = response.json()
    market = []

    for coin in data:
        market.append({
            "name": coin.get("name"),
            "symbol": coin.get("symbol", "").upper(),
            "price": coin.get("current_price"),
            "market_cap": coin.get("market_cap") or 0,
            "volume": coin.get("total_volume") or 0,
            "change_1h": coin.get("price_change_percentage_1h_in_currency") or 0,
            "change_24h": coin.get("price_change_percentage_24h_in_currency") or 0,
            "change_7d": coin.get("price_change_percentage_7d_in_currency") or 0,
        })

    return market


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

    # Early signal, not late pump
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

    # Penalties
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

    if volume <= 0:
        score -= 3
        reasons.append("weak volume data")

    if not reasons:
        reasons.append("no strong early setup")

    return score, reasons


def get_top_signals(market, risk_mode, limit=5):
    scored = []

    for coin in market:
        score, reasons = score_emerging_setup(coin, risk_mode)
        scored.append({**coin, "score": score, "reasons": reasons})

    return sorted(scored, key=lambda x: x["score"], reverse=True)[:limit]


def get_selected_decision(coins):
    if not coins:
        return "NO DATA ⚠️", "Live data is unavailable.", 0

    avg_change = sum(c["change_24h"] for c in coins) / len(coins)
    volatility = sum(abs(c["change_24h"]) for c in coins) / len(coins)

    confidence = min(int(abs(avg_change) * 18), 90)

    if volatility > 5:
        confidence -= 15

    confidence = max(confidence, 50)

    if avg_change > 2:
        return "POSITIVE WATCH 🚀", "Selected coins show positive momentum.", confidence
    elif avg_change < -2:
        return "CAUTION ❌", "Selected coins show negative momentum.", confidence
    return "WATCH 👀", "Selected coins are unclear. No strong signal.", confidence


# ---------------- LOAD ----------------
with st.spinner("Loading selected coins..."):
    selected_data = get_selected_prices(selected_coins, currency)

with st.spinner("Scanning market for early signals..."):
    market_data = get_market_data(currency, scan_size)

top_signals = get_top_signals(market_data, risk_mode, 5) if market_data else []
emerging_best = top_signals[0] if top_signals else None
decision, reason, confidence = get_selected_decision(selected_data)

# ---------------- HEADER ----------------
st.title("🤖 AI Crypto Market Scanner")
st.caption("Early-signal scanner. Avoids chasing coins that already pumped. Educational only — not financial advice.")

# ---------------- SELECTED COINS ----------------
st.subheader("📊 Selected Coins")

if selected_data:
    cols = st.columns(3)

    for i, coin in enumerate(selected_data):
        with cols[i % 3]:
            color = "#86efac" if coin["change_24h"] >= 0 else "#f87171"
            arrow = "▲" if coin["change_24h"] >= 0 else "▼"

            st.markdown(f"""
            <div class="metric-card">
                <div class="coin-symbol">{coin['symbol']}</div>
                <div class="big-price">{format_price(coin['price'])} {currency.upper()}</div>
                <div style="color:{color}; font-size:18px; margin-top:12px;">
                    {arrow} {coin['change_24h']:.2f}% / 24h
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("No selected coin data available.")

# ---------------- EMERGING BEST ----------------
st.subheader("🌱 Best Early Signal")

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
        <p class="small-muted">The scanner prefers moderate early movement and penalizes overheated assets.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.write("No early signal found.")

# ---------------- TOP 5 TABLE ----------------
if top_signals:
    st.subheader("🔥 Top 5 Early Signals")

    table_rows = []
    for coin in top_signals:
        label, _ = signal_badge(coin["score"])
        table_rows.append({
            "Coin": f"{coin['symbol']} — {coin['name']}",
            "Price": f"{format_price(coin['price'])} {currency.upper()}",
            "1h %": round(coin["change_1h"], 2),
            "24h %": round(coin["change_24h"], 2),
            "7d %": round(coin["change_7d"], 2),
            "Score": coin["score"],
            "Signal": label,
            "Why": ", ".join(coin["reasons"])
        })

    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

# ---------------- CHART ----------------
if selected_data:
    st.subheader("📈 Selected Coins Comparison")

    fig = px.bar(
        x=[c["symbol"] for c in selected_data],
        y=[c["price"] for c in selected_data],
        labels={"x": "Coin", "y": currency.upper()},
        title=f"Selected coin prices in {currency.upper()}"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- DECISION ----------------
st.subheader("🤖 Selected Coins Decision")

st.markdown(f"""
<div class="card">
    <h2>{decision}</h2>
    <p>{reason}</p>
    <p><b>Confidence:</b> {confidence}%</p>
</div>
""", unsafe_allow_html=True)

# ---------------- EXPORT ----------------
st.subheader("📤 Export Report")

report = f"""
AI Crypto Market Scanner Report
Generated: {datetime.now()}

Currency: {currency.upper()}
Risk mode: {risk_mode}
Scan size: Top {scan_size}

Selected coins:
{selected_data}

Best early signal:
{emerging_best}

Top 5 signals:
{top_signals}

Selected coins decision:
{decision}
Reason: {reason}
Confidence: {confidence}%

Disclaimer:
This is not financial advice. It is an educational early-signal market scanner.
"""

st.download_button(
    "Download Report",
    report,
    file_name="crypto_market_scanner_report.txt"
)

if st.button("🔄 Refresh Data"):
    st.rerun()