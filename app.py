import streamlit as st
import requests
import pandas as pd
from pathlib import Path
from textwrap import dedent

st.set_page_config(
    page_title="Koshka Crypto AI Agent",
    page_icon="🐈",
    layout="wide"
)

def html(content):
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)

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
</style>
""")

cat_black = Path("cat_black.png")
cat_orange = Path("cat_orange.png")

# ---------- REASON EXPLANATIONS (bilingual) ----------
REASON_EXPLAIN = {
    "early 1h momentum": (
        "early 1h momentum",
        "Цена растёт последний час — возможно начало движения. / "
        "Price rising in the last hour — possible start of a move."
    ),
    "healthy 24h move": (
        "healthy 24h move",
        "Рост за 24ч умеренный — не слишком много, не слишком мало. / "
        "24h gain is moderate — not too much, not too little."
    ),
    "healthy momentum": (
        "healthy momentum",
        "Общий импульс монеты в здоровом диапазоне. / "
        "Overall coin momentum is in a healthy range."
    ),
    "momentum overheated": (
        "momentum overheated ⚠️",
        "Монета выросла слишком быстро — риск отката. / "
        "Coin rose too fast — pullback risk is high."
    ),
    "weak momentum": (
        "weak momentum",
        "Импульс слабый — монета не двигается активно. / "
        "Momentum is weak — coin is not moving actively."
    ),
    "strong volume activity": (
        "strong volume activity",
        "Много людей торгуют этой монетой прямо сейчас — сильный интерес. / "
        "Many people are trading this coin right now — strong interest."
    ),
    "normal volume activity": (
        "normal volume activity",
        "Объём торгов нормальный — стандартная активность. / "
        "Trading volume is normal — standard activity."
    ),
    "weak volume activity": (
        "weak volume activity ⚠️",
        "Мало торгов — монету могут легко двигать крупные игроки. / "
        "Low trading — big players can easily move this coin."
    ),
    "good liquidity": (
        "good liquidity",
        "Монета крупная — проще купить и продать без большого проскальзывания. / "
        "Large coin — easier to buy and sell without big slippage."
    ),
    "already pumped too much": (
        "already pumped too much ⛔",
        "Монета уже очень сильно выросла за 24ч — поздно входить, риск отката. / "
        "Coin already pumped heavily in 24h — late entry, high reversal risk."
    ),
    "24h move overextended": (
        "24h move overextended ⚠️",
        "Рост за 24ч превысил здоровый предел для выбранного режима риска. / "
        "24h move exceeded the healthy limit for your chosen risk mode."
    ),
    "7d overheated": (
        "7d overheated ⚠️",
        "За последнюю неделю монета выросла слишком сильно — осторожно. / "
        "Coin rose too much over the last week — be careful."
    ),
    "falling momentum": (
        "falling momentum ⛔",
        "Монета падает — входить против тренда очень рискованно. / "
        "Coin is falling — entering against the trend is very risky."
    ),
    "no strong setup": (
        "no strong setup",
        "Нет ни сильных позитивных, ни негативных сигналов — нейтрально. / "
        "No strong positive or negative signals — neutral."
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

with h2:
    html("""
    <div class="hero">
        <div class="big-title">Koshka Crypto AI Agent</div>
        <div class="subtitle">
            AI-assisted crypto momentum scanner using live market data, liquidity and coin health scoring.<br>
            Сканер крипто-моментума на живых данных. Только для обучения — не финансовый совет. / Educational only — not financial advice.
        </div>
    </div>
    """)

# ---------- SETTINGS ----------
html("""
<div class="settings-box">
    <h2>⚙️ Scanner Settings / Настройки</h2>
</div>
""")

s1, s2, s3 = st.columns(3)

with s1:
    currency = st.selectbox(
        "💱 Currency / Валюта",
        ["usd", "aed", "eur", "gbp", "rub"],
        index=1
    )

with s2:
    risk_mode = st.selectbox(
        "⚠️ Risk Mode / Режим риска",
        ["Conservative", "Balanced", "Aggressive"],
        index=1
    )

with s3:
    scan_size = st.selectbox(
        "🌍 Coins To Scan / Монет для сканирования",
        [50, 100, 150, 200],
        index=1
    )

with st.expander("❓ Help / Помощь для новичков"):
    st.markdown("""
### 🇷🇺 Для новичков

**Что такое этот инструмент?**
Это сканер который смотрит на движение цен криптовалют и выдаёт оценку — насколько интересна монета прямо сейчас по техническим признакам. Это НЕ предсказание будущего.

**Сигналы:**
- 🟢 **STRONG SIGNAL** — монета показывает хорошие краткосрочные признаки. Не значит "покупай"!
- 🟡 **NEUTRAL** — интересно, но нет подтверждения
- 🔴 **HIGH RISK** — слабые или опасные признаки

**Важные предупреждения:**
- Маленькие монеты (низкий market cap) могут показывать STRONG SIGNAL но быть очень рискованными
- Высокий скор = хорошие цифры сейчас, не гарантия роста
- Всегда проверяй BTC Dominance и Fear & Greed перед решением

**Fear & Greed Index:**
- 0–24 😱 Extreme Fear — исторически хорошее время для накопления
- 25–44 😰 Fear — рынок осторожен
- 45–55 😐 Neutral — нет сигнала
- 56–74 😏 Greed — импульс есть, но осторожно
- 75–100 🤑 Extreme Greed — думай о фиксации прибыли

**BTC Dominance:**
- >55% → BTC сезон, альты проигрывают
- 48–55% → смешанные сигналы
- <48% → альткоин сезон

---

### 🇬🇧 For beginners

**What is this tool?**
A scanner that looks at crypto price movements and scores coins by short-term technical signals. This is NOT a prediction of the future.

**Signals:**
- 🟢 **STRONG SIGNAL** — coin shows good short-term signs. Does NOT mean "buy"!
- 🟡 **NEUTRAL** — interesting but unconfirmed
- 🔴 **HIGH RISK** — weak or dangerous signs

**Important warnings:**
- Small coins (low market cap) can show STRONG SIGNAL but be very risky
- High score = good numbers right now, not a guarantee of growth
- Always check BTC Dominance and Fear & Greed before deciding

**This app does not use real RSI** — it uses a transparent Momentum Proxy based on 1h/24h/7d price movement.

Educational only. Not financial advice.
""")

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

# ---------- MACRO SECTION ----------
fg = load_fear_greed()
btc_global = load_btc_dominance()

st.subheader("🌐 Macro Market Context / Макро контекст рынка")

m1, m2, m3 = st.columns(3)

with m1:
    if fg:
        val = fg["value"]
        label = fg["label"]

        if val <= 24:
            fg_class = "fg-extreme-fear"
            fg_advice_en = "Extreme Fear — historically good time to accumulate"
            fg_advice_ru = "Крайний страх — исторически хорошее время для накопления"
            fg_emoji = "😱"
        elif val <= 44:
            fg_class = "fg-fear"
            fg_advice_en = "Fear — market cautious, watch for reversals"
            fg_advice_ru = "Страх — рынок осторожен, смотри на развороты"
            fg_emoji = "😰"
        elif val <= 55:
            fg_class = "fg-neutral"
            fg_advice_en = "Neutral — no strong macro signal"
            fg_advice_ru = "Нейтрально — нет сильного макро-сигнала"
            fg_emoji = "😐"
        elif val <= 74:
            fg_class = "fg-greed"
            fg_advice_en = "Greed — momentum strong, but stay alert"
            fg_advice_ru = "Жадность — импульс есть, но будь осторожен"
            fg_emoji = "😏"
        else:
            fg_class = "fg-extreme-greed"
            fg_advice_en = "Extreme Greed — consider taking profits"
            fg_advice_ru = "Крайняя жадность — подумай о фиксации прибыли"
            fg_emoji = "🤑"

        html(f"""
        <div class="macro-box">
            <div class="macro-label">{fg_emoji} Fear & Greed Index</div>
            <div class="macro-value {fg_class}">{val}</div>
            <div class="macro-desc {fg_class}">{label}</div>
            <br>
            <div class="small-muted">
                🇷🇺 {fg_advice_ru}<br><br>
                🇬🇧 {fg_advice_en}
            </div>
        </div>
        """)
    else:
        html("""
        <div class="macro-box">
            <div class="macro-label">😱 Fear & Greed Index</div>
            <div class="small-muted">Unavailable / Недоступно</div>
        </div>
        """)

with m2:
    if btc_global and btc_global["btc_dominance"]:
        dom = btc_global["btc_dominance"]

        if dom >= 55:
            dom_class = "fg-fear"
            dom_advice_en = "BTC season — altcoins underperforming Bitcoin"
            dom_advice_ru = "BTC сезон — альткоины проигрывают биткоину"
            dom_emoji = "🟠"
        elif dom >= 48:
            dom_class = "fg-neutral"
            dom_advice_en = "Mixed signals — no clear alt or BTC season"
            dom_advice_ru = "Смешанные сигналы — нет явного сезона"
            dom_emoji = "⚖️"
        else:
            dom_class = "fg-greed"
            dom_advice_en = "Altcoin season — money flowing from BTC to alts"
            dom_advice_ru = "Альт-сезон — деньги перетекают из BTC в альты"
            dom_emoji = "🚀"

        html(f"""
        <div class="macro-box">
            <div class="macro-label">{dom_emoji} BTC Dominance / Доминация BTC</div>
            <div class="macro-value {dom_class}">{dom}%</div>
            <br>
            <div class="small-muted">
                🇷🇺 {dom_advice_ru}<br><br>
                🇬🇧 {dom_advice_en}
            </div>
        </div>
        """)
    else:
        html("""
        <div class="macro-box">
            <div class="macro-label">🟠 BTC Dominance</div>
            <div class="small-muted">Unavailable / Недоступно</div>
        </div>
        """)

with m3:
    if btc_global and btc_global["total_mcap"]:
        mcap = btc_global["total_mcap"]

        if mcap >= 1_000_000_000_000:
            mcap_str = f"${mcap / 1_000_000_000_000:.2f}T"
        else:
            mcap_str = f"${mcap / 1_000_000_000:.0f}B"

        html(f"""
        <div class="macro-box">
            <div class="macro-label">💰 Total Crypto Market Cap / Общий рынок</div>
            <div class="macro-value">{mcap_str}</div>
            <br>
            <div class="small-muted">
                🇷🇺 Общий размер всего крипто рынка<br><br>
                🇬🇧 Total size of the entire crypto market
            </div>
        </div>
        """)
    else:
        html("""
        <div class="macro-box">
            <div class="macro-label">💰 Total Market Cap</div>
            <div class="small-muted">Unavailable / Недоступно</div>
        </div>
        """)

# ---------- COMBINED MACRO SUMMARY ----------
if fg and btc_global and btc_global["btc_dominance"]:
    val = fg["value"]
    dom = btc_global["btc_dominance"]

    if val <= 44 and dom >= 55:
        summary_ru = "😰🟠 Страх + BTC доминация высокая → BTC сейчас безопаснее альтов. Не лучшее время для мелких монет."
        summary_en = "Fear + high BTC dominance → BTC is safer than alts right now. Not a great time for small coins."
    elif val >= 75 and dom < 48:
        summary_ru = "🤑🚀 Крайняя жадность + альт-сезон → высокий риск, рынок перегрет. Осторожно с новыми позициями."
        summary_en = "Extreme greed + altcoin season → high risk, market overheated. Be careful with new positions."
    elif val <= 44 and dom < 48:
        summary_ru = "😰🚀 Страх + альт-сезон начинается → потенциально интересный момент для осторожного входа в альты."
        summary_en = "Fear + altcoin season starting → potentially interesting moment for careful alt entries."
    elif val >= 56 and dom >= 55:
        summary_ru = "😏🟠 Жадность + BTC доминация высокая → BTC лидирует. Альты отстают."
        summary_en = "Greed + high BTC dominance → BTC is leading. Alts are lagging."
    else:
        summary_ru = "😐 Смешанные сигналы — нет явного направления. Наблюдай, не торопись."
        summary_en = "Mixed signals — no clear direction. Watch and wait."

    html(f"""
    <div class="macro-summary-box">
        <b>🔍 Macro Summary / Макро вывод:</b><br><br>
        🇷🇺 {summary_ru}<br><br>
        🇬🇧 {summary_en}
    </div>
    """)

st.divider()

# ---------- MARKET API ----------
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

    try:
        value = float(value)
    except Exception:
        return "N/A"

    if value < 0:
        return f"-{fmt(abs(value))}"

    if value >= 1000:
        return f"{value:,.0f}"

    if value >= 1:
        return f"{value:,.2f}"

    return f"{value:.6f}"

def change(coin, key):
    return coin.get(key) or 0

def momentum_proxy(ch1, ch24, ch7):

    score = 50
    score += ch1 * 3
    score += ch24 * 1.5
    score += ch7 * 0.35

    return round(max(0, min(score, 100)), 1)

def coin_health_score(coin, risk_mode):

    score = 0
    reasons = []

    ch1 = coin["1h"]
    ch24 = coin["24h"]
    ch7 = coin["7d"]
    volume = coin["volume"]
    market_cap = coin["market_cap"]
    proxy = coin["momentum_proxy"]

    if risk_mode == "Conservative":
        max_24h = 6
        max_7d = 25

    elif risk_mode == "Aggressive":
        max_24h = 12
        max_7d = 40

    else:
        max_24h = 8
        max_7d = 30

    if 0.3 <= ch1 <= 3:
        score += 15
        reasons.append("early 1h momentum")

    if 1 <= ch24 <= max_24h:
        score += 25
        reasons.append("healthy 24h move")

    if 45 <= proxy <= 70:
        score += 20
        reasons.append("healthy momentum")

    elif proxy > 80:
        score -= 20
        reasons.append("momentum overheated")

    elif proxy < 35:
        score -= 10
        reasons.append("weak momentum")

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

    if market_cap > 500_000_000:
        score += 10
        reasons.append("good liquidity")

    if ch24 > 12:
        score -= 30
        reasons.append("already pumped too much")

    elif ch24 > max_24h:
        score -= 15
        reasons.append("24h move overextended")

    if ch7 > max_7d:
        score -= 20
        reasons.append("7d overheated")

    if ch24 < -6:
        score -= 20
        reasons.append("falling momentum")

    if risk_mode == "Aggressive":
        score += 8

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

# ---------- SIGNALS ----------
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

    signal["momentum_proxy"] = momentum_proxy(ch1, ch24, ch7)

    signal["score"], signal["reasons"] = coin_health_score(
        signal,
        risk_mode
    )

    signals.append(signal)

signals = sorted(signals, key=lambda x: x["score"], reverse=True)

best = signals[0]
top5 = signals[:5]

# ---------- SELECTED COIN ----------
html("""
<div class="card">
    <div style="font-size:34px; font-weight:900; color:white;">
        🧠 Choose Coin For Analysis / Выбери монету для анализа
    </div>
    <div class="small-muted" style="margin-top:10px;">
        🇷🇺 Выбери любую криптовалюту чтобы увидеть её моментум, ликвидность и сигнал.<br>
        🇬🇧 Select any cryptocurrency to view its momentum, liquidity and market signal.
    </div>
</div>
""")

coin_options = {s["id"]: s for s in signals}

coin_ids = list(coin_options.keys())

default_coin_id = "bitcoin" if "bitcoin" in coin_ids else coin_ids[0]

selected_coin_id = st.selectbox(
    "Choose coin / Выбери монету",
    coin_ids,
    index=coin_ids.index(default_coin_id),
    format_func=lambda coin_id:
        f"{coin_options[coin_id]['symbol']} — {coin_options[coin_id]['coin']}",
    key="coin_selector"
)

selected = coin_options[selected_coin_id]

decision_text, badge_color = signal_decision(selected["score"])

metric_class = (
    "metric-positive"
    if selected["24h"] >= 0
    else "metric-negative"
)

# Small coin warning
is_small_cap = selected["market_cap"] < 500_000_000
small_cap_warning = ""
if is_small_cap and selected["score"] >= 75:
    small_cap_warning = """
    <div class="warning-box">
        ⚠️ <b>Новичок — обрати внимание! / Beginner notice!</b><br><br>
        🇷🇺 Это маленькая монета (низкий market cap). Даже при высоком скоре — риск значительно выше чем у BTC или ETH. Маленькие монеты могут быстро расти и быстро падать.<br><br>
        🇬🇧 This is a small coin (low market cap). Even with a high score — risk is much higher than BTC or ETH. Small coins can rise fast and fall just as fast.
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
            Momentum Proxy: {selected["momentum_proxy"]}/100
        </div>
        {small_cap_warning}
    </div>
    """)

with right:
    reasons_html = explain_reasons(selected["reasons"])

    html(f"""
    <div class="card">
        <span class="badge {badge_color}">{decision_text}</span>
        <h1>Coin Health Score</h1>
        <h3>Score: {selected["score"]}/100</h3>
        <div class="info-box">
            🇷🇺 Этот скор показывает текущие технические признаки — не предсказание.<br>
            🇬🇧 This score shows current technical signals — not a prediction.
        </div>
        <br>
        <div class="small-muted"><b>Reasons / Причины:</b></div>
        <br>
        {reasons_html}
    </div>
    """)

# ---------- PRICE MOVEMENT ----------
st.subheader("📈 Price Movement / Движение цены")

p1, p2, p3, p4 = st.columns(4)

p1.metric("1 Hour / 1 час", f"{selected['1h']:.2f}%")
p2.metric("24 Hours / 24 часа", f"{selected['24h']:.2f}%")
p3.metric("7 Days / 7 дней", f"{selected['7d']:.2f}%")
p4.metric("Momentum Proxy", f"{selected['momentum_proxy']}/100")

# ---------- BEST SETUP ----------
st.subheader("🔥 Strongest Coin Setup / Лучший сетап прямо сейчас")

best_decision_text, best_color = signal_decision(best["score"])

best_metric = (
    "metric-positive"
    if best["24h"] >= 0
    else "metric-negative"
)

b1, b2 = st.columns([3, 1])

with b1:
    best_reasons_html = explain_reasons(best["reasons"])

    html(f"""
    <div class="card">
        <span class="badge {best_color}">{best_decision_text}</span>
        <h1>{best["symbol"]} — {best["coin"]}</h1>
        <div class="price">{fmt(best["price"])} {currency.upper()}</div>
        <div class="{best_metric}">24h: {best["24h"]:.2f}%</div>
        <br>
        <div class="small-muted">
            Momentum Proxy: {best["momentum_proxy"]}/100
            &nbsp;&nbsp;|&nbsp;&nbsp;
            Score: {best["score"]}/100
        </div>
        <br>
        <div class="small-muted"><b>Why / Почему:</b></div>
        <br>
        {best_reasons_html}
    </div>
    """)

with b2:
    if cat_orange.exists():
        st.image(str(cat_orange), width=220)

# ---------- TOP 5 ----------
st.subheader("🌍 Top 5 Coin Setups / Топ 5 монет")

rows = []

for s in top5:

    d, _ = signal_decision(s["score"])

    rows.append({
        "Coin": f"{s['symbol']} — {s['coin']}",
        "Price": f"{fmt(s['price'])} {currency.upper()}",
        "1h %": round(s["1h"], 2),
        "24h %": round(s["24h"], 2),
        "7d %": round(s["7d"], 2),
        "Momentum Proxy": s["momentum_proxy"],
        "Score": s["score"],
        "Signal": d
    })

st.dataframe(
    pd.DataFrame(rows),
    use_container_width=True,
    hide_index=True
)

# ---------- REFRESH ----------
st.divider()

if st.button("🔄 Refresh Market Data / Обновить данные"):
    st.cache_data.clear()
    st.rerun()