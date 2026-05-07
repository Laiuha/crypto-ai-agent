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

.hero, .card, .settings-box, .macro-box {
    background: linear-gradient(135deg,#182035,#25314f);
    border-radius: 28px;
    padding: 28px;
    margin-bottom: 20px;
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
    font-size: 48px;
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

.macro-value {
    font-size: 42px;
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
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: #b0b8d1;
    font-size: 16px;
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
    font-size: 44px;
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

def explain_reasons(reasons):
    rows = []
    for r in reasons:
        label, desc = REASON_EXPLAIN.get(r, (r, ""))
        rows.append(f"""
        <div class="reason-row">
            <span class="reason-label">{label}</span><br>
            <span style="font-size:14px;">{desc}</span>
        </div>
        """)
    return "".join(rows)

# ---------- HEADER ----------
h1, h2 = st.columns([1, 5])

with h1:
    if cat_black.exists():
        st.image(str(cat_black), width=170)
    else:
        st.markdown("🐈")

with h2:
    html("""
    <div class="hero">
        <div class="big-title">🚀 Trust Me Bro Crypto Scanner</div>
        <div class="subtitle">
            AI-assisted scoring engine for high-probability crypto setups.
        </div>
    </div>
    """)

# ---------- SETTINGS ----------
html("""
<div class="settings-box">
    <h2>⚙️ Scanner Settings</h2>
</div>
""")

s1, s2, s3, s4 = st.columns(4)

with s1:
    currency = st.selectbox(
        "💱 Currency",
        ["usd", "aed", "eur", "gbp", "rub"],
        index=1
    )

with s2:
    risk_mode = st.selectbox(
        "⚠️ Risk Mode",
        ["Conservative", "Average", "Aggressive"],
        index=1
    )

with s3:
    scan_size = st.selectbox(
        "🌍 Coins To Scan",
        [100, 250, 500, 750],
        index=1
    )

with s4:
    min_score_filter = st.slider(
        "Scanner Minimum Score",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        help="This filter affects only Best Setup / Top Setups scanner. Coin analysis dropdown still shows all loaded coins."
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

def plan_explanation(plan_key, action):
    if plan_key == "entry":
        return "Текущая цена выбранной монеты. Уровни ниже рассчитаны от неё, потому что мы не знаем, ты уже купила или только смотришь."

    if plan_key == "stop":
        return "Stop — ориентир, где идея становится неправильной. Особенно полезно, если монета уже куплена."

    if plan_key == "tp1":
        return "TP1 — первый уровень частичной фиксации прибыли. Не обязательно продавать всё."

    if plan_key == "tp2":
        return "TP2 — второй уровень прибыли, если движение продолжится."

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


# ---------- MACRO SECTION ----------
st.subheader("🌐 Market Mood")

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

    signals.append(signal)

signals = sorted(signals, key=lambda x: x["score"], reverse=True)

filtered_signals = [s for s in signals if s["score"] >= min_score_filter]

# Part 1: selected coin analysis uses ALL loaded coins.
# Part 2: market scanner uses only coins passing the score filter.
best = filtered_signals[0] if filtered_signals else None
top10 = filtered_signals[:10]

# ---------- PART 1: SELECTED COIN ANALYSIS ----------
html("""
<div class="card">
    <div style="font-size:34px; font-weight:900; color:white;">
        🧠 Coin Analysis / Анализ монеты
    </div>
    <div class="small-muted" style="margin-top:10px;">
        Part 1: analyze any coin from the loaded market list. This is independent from the Top Setups scanner filter.
    </div>
</div>
""")

coin_options = {s["id"]: s for s in signals}
coin_ids = list(coin_options.keys())

# Default to real Bitcoin if it is loaded, otherwise first available coin.
default_coin_id = "bitcoin" if "bitcoin" in coin_options else coin_ids[0]

# If the previous selection disappears after changing scan size/currency, reset safely.
if "coin_selector" in st.session_state and st.session_state["coin_selector"] not in coin_options:
    st.session_state["coin_selector"] = default_coin_id

selected_coin_id = st.selectbox(
    "Choose coin / Выбери монету",
    coin_ids,
    index=coin_ids.index(st.session_state.get("coin_selector", default_coin_id)),
    format_func=lambda coin_id:
        f"{coin_options[coin_id]['symbol']} — {coin_options[coin_id]['coin']}",
    key="coin_selector"
)

selected = coin_options[selected_coin_id]

metric_class = "metric-positive" if selected["24h"] >= 0 else "metric-negative"

is_small_cap = selected["market_cap"] < 500_000_000
small_cap_warning = ""
if is_small_cap and selected["score"] >= 65:
    small_cap_warning = """
    <div class="warning-box">
        ⚠️ <b>Small cap risk!</b><br><br>
        🇷🇺 Это маленькая монета. Даже при хорошем setup риск выше: резкие движения, низкая ликвидность, манипуляции.<br><br>
        🇬🇧 Small-cap coin. Even with a good setup, risk is higher: sharp moves, low liquidity, manipulation.
    </div>
    """

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
            Market Cap: {fmt(selected["market_cap"])} &nbsp;&nbsp;|&nbsp;&nbsp;
            Volume Ratio: {selected["volume_ratio"]:.2%}<br>
            Momentum Proxy: {selected["momentum_proxy"]}/100
        </div>
        {small_cap_warning}
    </div>
    """)

with right:
    html(f"""
    <div class="card">
        <h2>🎯 Coin Setup</h2>
        <span class="badge {selected["action_color"]}" style="font-size:22px; padding:14px 24px;">{selected["action"]}</span>
        <h3>Score: {selected["score"]}/100</h3>

        <div class="reason-row">
            <span class="reason-label">Buy Timing:</span><br>
            <span class="badge {selected["entry_color"]}">{selected["entry_quality"]}</span><br>
            <span style="font-size:14px;">{selected["entry_reason"]}</span>
        </div>

        <div class="reason-row">
            <span class="reason-label">Risk:</span><br>
            <span class="badge {selected["risk_color"]}">{selected["risk_level"]}</span>
        </div>

        <div class="reason-row">
            <span class="reason-label">What To Do:</span><br>
            <span class="badge {selected["what_color"]}">{selected["what_to_do"]}</span><br>
            <span style="font-size:14px;">{selected["what_reason"]}</span>
        </div>

        <div class="reason-row">
            <span class="reason-label">Profit Status / Exit:</span><br>
            <span class="badge {selected["profit_color"]}">{selected["profit_status"]}</span><br>
            <span style="font-size:14px;">{selected["profit_reason"]}</span>
        </div>

        <div class="info-box">
            <b>Final answer / Итог:</b><br>
            {selected["action_reason"]}
        </div>
    </div>
    """)

# ---------- TRADE PLAN ----------
plan = selected["plan"]

st.subheader("🧾 Action Plan / План по выбранной монете")
st.caption("Levels are always shown because you may already hold this coin or may only be watching it. Educational only, not financial advice.")

tp1, tp2, tp3, tp4 = st.columns(4)

with tp1:
    html(f"""
    <div class="kpi">
        <div class="macro-label">Entry / Вход</div>
        <div style="font-size:22px;font-weight:900;line-height:1.25;">{plan["entry"]}</div>
        <div style="font-size:13px;color:#b0b8d1;margin-top:10px;line-height:1.45;">
            {plan_explanation("entry", selected["action"])}
        </div>
    </div>
    """)

with tp2:
    html(f"""
    <div class="kpi">
        <div class="macro-label">Stop / Стоп</div>
        <div style="font-size:22px;font-weight:900;line-height:1.25;">{plan["stop"]}</div>
        <div style="font-size:13px;color:#b0b8d1;margin-top:10px;line-height:1.45;">
            {plan_explanation("stop", selected["action"])}
        </div>
    </div>
    """)

with tp3:
    html(f"""
    <div class="kpi">
        <div class="macro-label">TP1 / Первая прибыль</div>
        <div style="font-size:22px;font-weight:900;line-height:1.25;">{plan["tp1"]}</div>
        <div style="font-size:13px;color:#b0b8d1;margin-top:10px;line-height:1.45;">
            {plan_explanation("tp1", selected["action"])}
        </div>
    </div>
    """)

with tp4:
    html(f"""
    <div class="kpi">
        <div class="macro-label">TP2 / Вторая прибыль</div>
        <div style="font-size:22px;font-weight:900;line-height:1.25;">{plan["tp2"]}</div>
        <div style="font-size:13px;color:#b0b8d1;margin-top:10px;line-height:1.45;">
            {plan_explanation("tp2", selected["action"])}
        </div>
    </div>
    """)

html(f"""
<div class="trade-plan-box">
    🇷🇺 {plan["note_ru"]}<br><br>
    🇬🇧 {plan["note_en"]}
</div>
""")

# ---------- PRICE MOVEMENT ----------
st.subheader("📈 Price Movement / Движение цены")

p1, p2, p3, p4, p5 = st.columns(5)

p1.metric("1 Hour / 1 час", f"{selected['1h']:.2f}%")
p2.metric("24 Hours / 24 часа", f"{selected['24h']:.2f}%")
p3.metric("7 Days / 7 дней", f"{selected['7d']:.2f}%")
p4.metric("Momentum Proxy", f"{selected['momentum_proxy']}/100")
p5.metric("Volume / MCap", f"{selected['volume_ratio']:.2%}")

# ---------- REASONS ----------
st.subheader("🧠 Why this score? / Почему такой скор?")
html(f"""
<div class="card">
    {explain_reasons(selected["reasons"])}
</div>
""")

# ---------- PART 2: MARKET SCANNER ----------
st.divider()
st.subheader("🔎 Market Scanner / Лучшие варианты")
st.caption("Part 2 scans the loaded market and shows only coins above the Scanner Minimum Score.")

if not filtered_signals:
    st.warning("No coins match the selected scanner score. Lower Scanner Minimum Score to see market setups.")
    rows = []
else:
    st.subheader("🔥 Best Setup Now")

    b1, b2 = st.columns([3, 1])

    with b1:
        html(f"""
<div class="card">
    <span class="badge {best["action_color"]}">{best["action"]}</span>
    <h1>{best["symbol"]} — {best["coin"]}</h1>
    <div class="price">{fmt(best["price"])} {currency.upper()}</div>
    <div class="{'metric-positive' if best["24h"] >= 0 else 'metric-negative'}">24h: {best["24h"]:.2f}%</div>
    <br>
    <div class="small-muted">
        Score: {best["score"]}/100 &nbsp;&nbsp;|&nbsp;&nbsp;
        Entry: {best["entry_quality"]} &nbsp;&nbsp;|&nbsp;&nbsp;
        Risk: {best["risk_level"]} &nbsp;&nbsp;|&nbsp;&nbsp;
        Profit Status: {best["profit_status"]}
    </div>
    <div class="info-box">
        {best["action_reason"]}
    </div>
    <br>
    <div class="small-muted"><b>Trade Plan:</b><br>
    Entry: {best["plan"]["entry"]}<br>
    Stop: {best["plan"]["stop"]}<br>
    TP1: {best["plan"]["tp1"]}<br>
    TP2: {best["plan"]["tp2"]}
    </div>
</div>
        """)

    with b2:
        if cat_orange.exists():
            st.image(str(cat_orange), width=220)
        else:
            st.markdown("🐈")

    # ---------- TOP SETUPS TABLE ----------
    st.subheader("🏆 Top Setups")

    rows = []

    for s in top10:
        rows.append({
            "Coin": f"{s['symbol']} — {s['coin']}",
            "Price": f"{fmt(s['price'])} {currency.upper()}",
            "1h %": round(s["1h"], 2),
            "24h %": round(s["24h"], 2),
            "7d %": round(s["7d"], 2),
            "Vol/MCap": f"{s['volume_ratio']:.2%}",
            "Momentum": s["momentum_proxy"],
            "Score": s["score"],
            "Action": s["action"],
            "Entry": s["entry_quality"].replace("Wait For Better Entry", "Wait").replace("Bad Timing", "Bad"),
            "Risk": s["risk_level"],
            "Exit": s["exit_signal"]
        })

st.dataframe(
    pd.DataFrame(rows),
    use_container_width=True,
    hide_index=True
)

# ---------- DOWNLOAD ----------
csv_df = pd.DataFrame(rows)
csv = csv_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Scanner Results CSV",
    data=csv,
    file_name="koshka_top_setups.csv",
    mime="text/csv"
)

# ---------- REFRESH ----------
st.divider()

if st.button("🔄 Refresh Market Data"):
    st.cache_data.clear()
    st.rerun()

st.caption("Educational only. Not financial advice. Probably not a rug.")