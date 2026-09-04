import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
import concurrent.futures

# =========================
# AUTO REFRESH
# =========================
REFRESH_SECONDS = 10

st_autorefresh(interval=REFRESH_SECONDS * 1000, key="refresh")

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Invesco India Midcap Fund NAV Tracker",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #050816;
    color: white;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #111827, #1f2937);
    border: 1px solid #374151;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.35);
}

div[data-testid="metric-container"] label {
    color: #cbd5e1 !important;
    font-size: 15px !important;
}

.big-title {
    font-size: 42px;
    font-weight: bold;
    color: white;
}

.timestamp {
    color: #bbbbbb;
    font-size: 15px;
}

.screenshot-box {
    background: linear-gradient(135deg, #0f172a, #111827);
    padding: 25px;
    border-radius: 25px;
    border: 1px solid #334155;
    margin-bottom: 20px;
}

.gainer-box {
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.35);
    padding: 12px;
    border-radius: 14px;
    margin-bottom: 10px;
}

.loser-box {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.35);
    padding: 12px;
    border-radius: 14px;
    margin-bottom: 10px;
}

.message-box {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #475569;
    margin-top: 20px;
}

.stButton>button {
    border-radius: 12px;
    height: 50px;
    font-weight: bold;
}

.stale-badge {
    background: rgba(239,68,68,0.15);
    border: 1px solid rgba(239,68,68,0.4);
    color: #fca5a5;
    padding: 8px 14px;
    border-radius: 10px;
    font-size: 13px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# INDIAN TIME
# =========================

now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
india_time = now_ist.strftime("%d %b %Y | %I:%M:%S %p")
today_ist_date = now_ist.date()

# =========================
# LOGO + TITLE
# =========================

col_logo, col_title = st.columns([1, 8])

with col_logo:
    st.image("logo.png", width=90)

with col_title:

    st.markdown(
        '<div class="big-title"> Invesco India Midcap Fund NAV Tracker</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="font-size:18px; color:#60a5fa; font-weight:bold; margin-top:-8px;">© Debrup Bera</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="timestamp">Last Updated: {india_time}</div>',
        unsafe_allow_html=True
    )

# =========================
# MANUAL NAV UPDATE
# =========================

previous_nav = 243.23
weekly_start_nav = 245.07

# =========================
# INVESTMENT DETAILS
# =========================

avg_nav = 217.10

total_units = 990.14

total_investment = (
    total_units * avg_nav
)

investment_date = datetime(
    2025,
    9,
    3
)

today_date = datetime.now()

total_days = (
    today_date - investment_date
).days

years = total_days // 365

remaining_days = total_days % 365

months = remaining_days // 30

days = remaining_days % 30

investment_duration = (
    f"{years}Y {months}M {days}D"
)

# =========================
# PORTFOLIO HOLDINGS
# =========================
# Updated to Invesco Mutual Fund's Monthly Portfolio Statement as on
# July 31, 2026 (equity holdings only; weights are "% to Net Assets").
# Excludes TREPS/Reverse Repo and Net Receivables/(Payables) lines
# (cash-equivalents, not equities).
# "Manipal Health Enterprises Ltd" (0.51%) is omitted - it is an
# unlisted company and has no resolvable NSE ticker.
# "Chola Financial Holdings", "Apar Industries" and "Sobha Ltd" from
# the prior statement have dropped out of this month's portfolio.

stocks = [

    ("PRESTIGE", 7.16),        # Prestige Estates Projects Limited
    ("FEDERALBNK", 6.42),      # The Federal Bank Limited
    ("MAXHEALTH", 6.21),       # Max Healthcare Institute Limited
    ("MEESHO", 4.64),          # Meesho Ltd
    ("MEDANTA", 4.37),         # Global Health Limited
    ("AUBANK", 4.22),          # AU Small Finance Bank Limited
    ("ETERNAL", 4.18),         # Eternal Limited
    ("INDUSINDBK", 4.06),      # IndusInd Bank Limited
    ("BSE", 3.86),             # BSE Limited
    ("LTF", 3.81),             # L&T Finance Limited
    ("INDIGO", 3.76),          # InterGlobe Aviation Limited
    ("MFSL", 3.16),            # Max Financial Services Limited
    ("SAILIFE", 3.05),         # Sai Life Sciences Limited
    ("JKCEMENT", 2.93),        # JK Cement Limited
    ("GLENMARK", 2.83),        # Glenmark Pharmaceuticals Limited
    ("ABB", 2.55),             # ABB India Limited
    ("SRF", 2.51),             # SRF Limited
    ("CPPLUS", 2.33),          # Aditya Infotech Limited
    ("NYKAA", 2.28),           # FSN E-Commerce Ventures Limited
    ("TORNTPOWER", 2.23),      # Torrent Power Limited
    ("TRENT", 2.11),           # Trent Limited
    ("SWIGGY", 2.08),          # Swiggy Limited
    ("AMBER", 2.07),           # Amber Enterprises India Limited
    ("DIXON", 1.48),           # Dixon Technologies (India) Limited
    ("ICICIGI", 1.47),         # ICICI Lombard General Insurance Company Limited
    ("BHARATFORG", 1.27),      # Bharat Forge Limited
    ("PHOENIXLTD", 1.24),      # The Phoenix Mills Limited
    ("KIMS", 1.06),            # Krishna Institute Of Medical Sciences Limited
    ("CORONA", 1.00),          # Corona Remedies Limited
    ("CRAFTSMAN", 0.97),       # Craftsman Automation Limited
    ("ETHOSLTD", 0.92),        # Ethos Ltd.
    ("AGARWALEYE", 0.73),      # Dr Agarwals Health Care Limited
    ("TIINDIA", 0.68),         # Tube Investments Of India Limited
    ("TIMKEN", 0.58),          # Timken India Limited
    ("MANIPALHOS", 0.51),      # Manipal Health Enterprises Limited
    ("BANSALWIRE", 0.50),      # Bansal Wire Industries Limited
    ("CARBORUNIV", 0.45),      # Carborundum Universal Limited
    ("WEWORK", 0.44),          # Wework India Management Limited
    ("MAXESTATES", 0.36),      # Max Estates Limited
    ("SONATSOFTW", 0.33),      # Sonata Software Limited
    ("VMM", 0.19),             # Vishal Mega Mart Limited

]


# =========================
# FETCH LIVE DATA (single batched, threaded, timed-out download)
# =========================
#
# WHY PREVIOUS CLOSES WERE SHOWING AS 3 DAYS OLD:
# Inside one batched yf.download() call for 40 tickers, if Yahoo
# throttles/fails a SUBSET of those tickers (common under sustained
# load), yfinance doesn't raise an error for the whole batch -- it just
# fills that ticker's recent rows with NaN. The old code did
# `.dropna()` per ticker and then blindly grabbed iloc[-2] / iloc[-1].
# If a ticker's last 2-3 days came back NaN, dropna() silently removed
# them, and iloc[-2]/iloc[-1] landed on genuinely old data -- which was
# then displayed and used in NAV math as if it were live/previous-day
# data. The existing "reuse last known good value" fallback never
# triggered for this case because a value (just a stale one) was always
# returned.
#
# FIX: after extracting the per-ticker Close series, check the ACTUAL
# DATE of the most recent row. If it's older than STALE_DATA_MAX_DAYS,
# treat that ticker's fetch as failed for this cycle (return None, None)
# so it falls through to the existing last-known-good-value cache
# instead of being displayed as current.

FETCH_TIMEOUT_SECONDS = 15

# Generous enough to cover a long weekend / one-day exchange holiday,
# tight enough to catch "stuck for days" staleness.
STALE_DATA_MAX_DAYS = 4

if "last_good_data" not in st.session_state:
    st.session_state["last_good_data"] = {}

if "last_good_asof" not in st.session_state:
    st.session_state["last_good_asof"] = {}

symbol_list = [s for s, _ in stocks]
ticker_list = [s + ".NS" for s in symbol_list]


def _download_batch(tickers):
    """Runs in a worker thread; wrapped with a timeout by the caller."""
    return yf.download(
        tickers=tickers,
        period="10d",
        interval="1d",
        group_by="ticker",
        threads=True,
        progress=False,
        auto_adjust=False,
    )


@st.cache_data(ttl=REFRESH_SECONDS, show_spinner=False)
def fetch_all_prices(tickers):
    """One batched, threaded call for ALL tickers, with a hard timeout.
    Returns a DataFrame (possibly empty if the fetch failed/timed out)."""
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            future = ex.submit(_download_batch, tickers)
            return future.result(timeout=FETCH_TIMEOUT_SECONDS)
    except concurrent.futures.TimeoutError:
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def get_prices_from_batch(ticker, batch_data, as_of_today):
    """Pull (previous_close, live_price, as_of_date) for one ticker out of
    the already-fetched batch DataFrame.

    Returns (None, None, None) if there's no data OR the freshest data
    point available is older than STALE_DATA_MAX_DAYS -- callers should
    treat that the same as a failed fetch and fall back to cached values.
    """
    try:
        if isinstance(batch_data.columns, pd.MultiIndex):
            hist = batch_data[ticker]["Close"].dropna()
        else:
            hist = batch_data["Close"].dropna()

        if len(hist) == 0:
            return None, None, None

        latest_date = hist.index[-1].date()
        age_days = (as_of_today - latest_date).days

        if age_days > STALE_DATA_MAX_DAYS:
            # Data exists but it's too old to trust -- treat as a
            # failed fetch for this cycle.
            return None, None, None

        if len(hist) >= 2:
            prev = round(float(hist.iloc[-2]), 2)
            live = round(float(hist.iloc[-1]), 2)
        else:
            prev = live = round(float(hist.iloc[-1]), 2)

        return prev, live, latest_date

    except Exception:
        return None, None, None


batch_data = fetch_all_prices(ticker_list)

fetch_failed = batch_data is None or batch_data.empty

rows = []
total_weighted_return = 0
stale_symbols = []       # fell back to cache this cycle
never_fetched_symbols = []  # no cache to fall back to at all

for symbol, weight in stocks:

    ticker = symbol + ".NS"

    prev_close, live_price, as_of_date = (None, None, None)
    if not fetch_failed:
        prev_close, live_price, as_of_date = get_prices_from_batch(
            ticker, batch_data, today_ist_date
        )

    if prev_close is not None and live_price is not None:
        # Good, fresh data this refresh -> compute and remember it
        change_pct = ((live_price - prev_close) / prev_close) * 100 if prev_close else 0
        weighted_return = (change_pct * weight) / 100
        total_weighted_return += weighted_return

        row = [
            symbol,
            round(weight, 2),
            prev_close,
            live_price,
            round(change_pct, 2),
        ]

        st.session_state["last_good_data"][symbol] = row
        st.session_state["last_good_asof"][symbol] = as_of_date

    else:
        # No fresh/trustworthy data this refresh -> reuse last known
        # good values instead of collapsing to 0 or showing stale data
        # as if it were current.
        cached_row = st.session_state["last_good_data"].get(symbol)

        if cached_row is not None:
            row = cached_row
            cached_change_pct = row[4]
            weighted_return = (cached_change_pct * weight) / 100
            total_weighted_return += weighted_return
            stale_symbols.append(symbol)
        else:
            row = [symbol, weight, 0, 0, 0]
            never_fetched_symbols.append(symbol)

    rows.append(row)

if fetch_failed:
    st.warning(
        "⚠️ Couldn't reach Yahoo Finance this refresh "
        f"(timed out after {FETCH_TIMEOUT_SECONDS}s or request failed). "
        "Showing last known values.",
        icon="⚠️",
    )
elif stale_symbols:
    preview = ", ".join(stale_symbols[:6])
    more = f" +{len(stale_symbols) - 6} more" if len(stale_symbols) > 6 else ""
    st.markdown(
        f'<div class="stale-badge">⚠️ {len(stale_symbols)} symbol(s) returned '
        f'data older than {STALE_DATA_MAX_DAYS} days this refresh — showing '
        f'their last known good values instead: {preview}{more}</div>',
        unsafe_allow_html=True,
    )

if never_fetched_symbols:
    st.info(
        "ℹ️ No data (fresh or cached) yet for: "
        + ", ".join(never_fetched_symbols)
        + ". These show as 0 until a successful fetch comes through."
    )

# =========================
# DATAFRAME
# =========================

df = pd.DataFrame(

    rows,

    columns=[

        "Stock",
        "Weight %",
        "Previous Close",
        "Live Price",
        "% Change"

    ]

)

# =========================
# NAV CALCULATIONS
# =========================

estimated_nav = previous_nav * (
    1 + total_weighted_return / 100
)

daily_nav_change = (
    estimated_nav - previous_nav
)

weekly_change = (
    (estimated_nav - weekly_start_nav)
    / weekly_start_nav
) * 100

weekly_nav_change = (
    estimated_nav - weekly_start_nav
)

# =========================
# UNREALISED PROFIT / LOSS
# =========================

unrealised_pl_pct = (
    (estimated_nav - avg_nav)
    / avg_nav
) * 100

# =========================
# AMOUNT CALCULATIONS
# =========================

daily_return_amount = daily_nav_change * total_units

weekly_return_amount = (
    total_investment
    * weekly_change
    / 100
)

unrealised_pl_amount = (
    total_investment
    * unrealised_pl_pct
    / 100
)

# =========================
# TOP 5 GAINERS & LOSERS
# =========================

top_gainers = df.sort_values(
    by="% Change",
    ascending=False
).head(5)

top_losers = df.sort_values(
    by="% Change",
    ascending=True
).head(5)

# =========================
# CONDITIONAL COLORS
# =========================

def color_change(val):

    if val > 0:
        return "color: lime"

    elif val < 0:
        return "color: red"

    return "color: white"

styled_df = df.style.format({

    "Weight %": "{:.2f}",
    "Previous Close": "{:.2f}",
    "Live Price": "{:.2f}",
    "% Change": "{:.2f}"

}).map(

    color_change,
    subset=["% Change"]

)

# =========================
# SCREENSHOT SECTION
# =========================

st.markdown('<div class="screenshot-box">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Previous NAV",
    f"{previous_nav:.2f}"
)

col2.metric(
    "Expected NAV",
    f"{estimated_nav:.2f}",
    f"{total_weighted_return:.2f}%"
)

col3.metric(
    "📅 Weekly Change",
    f"{weekly_change:.2f}%",
    f"{weekly_nav_change:.2f} NAV"
)

col4.metric(
    "📈 Daily Change",
    f"{total_weighted_return:.2f}%"
)

st.markdown("---")

col5, col6, col7 = st.columns(3)

col5.metric(
    "💰 Daily Return",
    f"₹{daily_return_amount:,.0f}"
)

col6.metric(
    "💵 Weekly Return",
    f"₹{weekly_return_amount:,.0f}"
)

col7.metric(
    "💼 Unrealised P/L",
    f"₹{unrealised_pl_amount:,.0f}",
    f"{unrealised_pl_pct:.2f}%"
)

st.markdown("---")

col8, col9 = st.columns(2)

col8.metric(
    "⏳ Investment Time",
    investment_duration
)

col9.metric(
    "🧾 Total Units",
    f"{total_units:,.3f}"
)

st.markdown("---")

# =========================
# TOP 5 GAINERS
# =========================

col10, col11 = st.columns(2)

with col10:

    st.subheader("🚀 Top 5 Gainers")

    for _, row in top_gainers.iterrows():

        st.markdown(f"""
        <div class="gainer-box">
        <b>{row['Stock']}</b> ({row['Weight %']:.2f}%)
        <br>
        {row['% Change']:.2f}%
        </div>
        """, unsafe_allow_html=True)

# =========================
# TOP 5 LOSERS
# =========================

with col11:

    st.subheader("🔻 Top 5 Losers")

    for _, row in top_losers.iterrows():

        st.markdown(f"""
        <div class="loser-box">
        <b>{row['Stock']}</b> ({row['Weight %']:.2f}%)
        <br>
        {row['% Change']:.2f}%
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# EMAIL & WHATSAPP SECTION
# =========================

st.markdown('<div class="message-box">', unsafe_allow_html=True)

st.subheader("📧 Share Today's Expected Returns")

# Prepare the message content
message_content = f"""
🔥 INVESCO India Midcap Fund - Daily Update

📅 Date: {india_time}

📊 NAV Details:
• Previous NAV: ₹{previous_nav:.2f}
• Expected NAV: ₹{estimated_nav:.2f}
• Daily Change: {total_weighted_return:.2f}%

💰 Returns:
• Daily Return: ₹{daily_return_amount:,.0f}
• Weekly Return: ₹{weekly_return_amount:,.0f}
• Unrealised P/L: ₹{unrealised_pl_amount:,.0f} ({unrealised_pl_pct:.2f}%)

📈 Portfolio Performance:
• Weekly Change: {weekly_change:.2f}%
• Investment Duration: {investment_duration}

🚀 Top 5 Gainers:
"""

for idx, (_, row) in enumerate(top_gainers.head(5).iterrows(), 1):
    message_content += f"{idx}. {row['Stock']} - {row['% Change']:.2f}%\n"

message_content += "\n🔻 Top 5 Losers:\n"

for idx, (_, row) in enumerate(top_losers.head(5).iterrows(), 1):
    message_content += f"{idx}. {row['Stock']} - {row['% Change']:.2f}%\n"

message_content += "\n© Debrup Bera | Invesco India Midcap Fund Tracker"

# Display the message preview
with st.expander("📝 Preview Message", expanded=False):
    st.text_area("Message Content", message_content, height=300, disabled=True)

# Create columns for input fields
col_email, col_phone = st.columns(2)

with col_email:
    st.markdown("#### 📧 Send via Email")
    recipient_email = st.text_input("Recipient Email", placeholder="example@gmail.com")

    # Email configuration (You need to set these in Streamlit secrets or environment variables)
    sender_email = st.text_input("Your Email (Gmail)", placeholder="your-email@gmail.com")
    sender_password = st.text_input("App Password", type="password",
                                   help="Use Gmail App Password, not your regular password")

with col_phone:
    st.markdown("#### 📱 Send via WhatsApp")
    phone_number = st.text_input("Phone Number (with country code)",
                                 placeholder="+911234567890",
                                 help="Format: +91XXXXXXXXXX (India)")

# Create buttons
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

with col_btn1:
    send_email_btn = st.button("📧 Send Email", use_container_width=True)

with col_btn2:
    send_whatsapp_btn = st.button("📱 Send WhatsApp", use_container_width=True)

# =========================
# EMAIL SENDING FUNCTION
# =========================

def send_email(sender, password, recipient, subject, body):
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)

        # Send email
        text = msg.as_string()
        server.sendmail(sender, recipient, text)
        server.quit()

        return True, "Email sent successfully! ✅"

    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

# =========================
# WHATSAPP LINK GENERATION
# =========================

def generate_whatsapp_link(phone, message):
    # Remove '+' and any spaces from phone number
    clean_phone = phone.replace('+', '').replace(' ', '').replace('-', '')

    # URL encode the message
    encoded_message = urllib.parse.quote(message)

    # Generate WhatsApp link
    whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_message}"

    return whatsapp_url

# =========================
# HANDLE BUTTON CLICKS
# =========================

if send_email_btn:
    if not recipient_email or not sender_email or not sender_password:
        st.error("⚠️ Please fill in all email fields!")
    else:
        with st.spinner("Sending email..."):
            subject = f"Invesco India Midcap Fund Update - {datetime.now().strftime('%d %b %Y')}"
            success, message = send_email(sender_email, sender_password, recipient_email,
                                         subject, message_content)

            if success:
                st.success(message)
            else:
                st.error(message)
                st.info("💡 Tip: For Gmail, you need to use an 'App Password', not your regular password. "
                       "Generate one at: https://myaccount.google.com/apppasswords")

if send_whatsapp_btn:
    if not phone_number:
        st.error("⚠️ Please enter a phone number!")
    else:
        whatsapp_url = generate_whatsapp_link(phone_number, message_content)
        st.success("✅ WhatsApp link generated!")
        st.markdown(f"[📱 Click here to open WhatsApp]({whatsapp_url})")
        st.info("💡 Clicking the link will open WhatsApp with the pre-filled message. "
               "You can review and send it from there.")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PORTFOLIO TABLE
# =========================

st.markdown("---")

st.subheader("📊 Portfolio Holdings")

st.dataframe(
    styled_df,
    use_container_width=True,
    height=850
)

# Small transparency footer so a data-freshness problem is visible
# immediately instead of showing up as silently wrong numbers.
if st.session_state["last_good_asof"]:
    oldest_symbol = min(
        st.session_state["last_good_asof"],
        key=lambda s: st.session_state["last_good_asof"][s]
    )
    oldest_date = st.session_state["last_good_asof"][oldest_symbol]
    st.caption(
        f"Oldest 'Previous Close' data point currently in use: "
        f"{oldest_symbol} as of {oldest_date.strftime('%d %b %Y')}"
    )

st.markdown("---")

st.caption(f"© Debrup Bera | Auto-refresh every {REFRESH_SECONDS} seconds")
