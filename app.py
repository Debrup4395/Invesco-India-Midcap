import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import concurrent.futures
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from zoneinfo import ZoneInfo
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse

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

.source-tag {
    font-size: 11px;
    color: #94a3b8;
    font-style: italic;
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

previous_nav = 241.46
weekly_start_nav = 240.16

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
# Invesco India Midcap Fund - Monthly Portfolio Statement as on
# AUGUST 31, 2026 (equity holdings only; TREPS/Reverse Repo and Net
# Receivables/(Payables) excluded, since they aren't tradable equity
# tickers). Same 41 tickers as the July 31 statement; only
# weights/ranking moved. MANIPALHOS jump (0.51% -> 4.74%) reflects
# its Aug 5, 2026 NSE listing, not a data error.

stocks = [

    ("PRESTIGE", 7.27),        # Prestige Estates Projects Limited
    ("MAXHEALTH", 6.50),       # Max Healthcare Institute Limited
    ("FEDERALBNK", 5.98),      # The Federal Bank Limited
    ("MEESHO", 4.84),          # Meesho Ltd
    ("MANIPALHOS", 4.74),      # Manipal Health Enterprises Limited
    ("MEDANTA", 4.26),         # Global Health Limited
    ("ETERNAL", 4.20),         # Eternal Limited
    ("AUBANK", 4.05),          # AU Small Finance Bank Limited
    ("LTF", 3.97),             # L&T Finance Limited
    ("INDUSINDBK", 3.92),      # IndusInd Bank Limited
    ("BSE", 3.22),             # BSE Limited
    ("SAILIFE", 3.14),         # Sai Life Sciences Limited
    ("MFSL", 3.07),            # Max Financial Services Limited
    ("INDIGO", 3.03),          # InterGlobe Aviation Limited
    ("GLENMARK", 2.91),        # Glenmark Pharmaceuticals Limited
    ("ABB", 2.86),             # ABB India Limited
    ("JKCEMENT", 2.56),        # JK Cement Limited
    ("SRF", 2.27),             # SRF Limited
    ("CPPLUS", 2.27),          # Aditya Infotech Limited
    ("NYKAA", 2.21),           # FSN E-Commerce Ventures Limited
    ("AMBER", 1.96),           # Amber Enterprises India Limited
    ("BHARATFORG", 1.85),      # Bharat Forge Limited
    ("TRENT", 1.77),           # Trent Limited
    ("TORNTPOWER", 1.77),      # Torrent Power Limited
    ("SWIGGY", 1.48),          # Swiggy Limited
    ("DIXON", 1.45),           # Dixon Technologies (India) Limited
    ("TIINDIA", 1.42),         # Tube Investments Of India Limited
    ("ICICIGI", 1.31),         # ICICI Lombard General Insurance Company Limited
    ("PHOENIXLTD", 1.15),      # The Phoenix Mills Limited
    ("CRAFTSMAN", 1.02),       # Craftsman Automation Limited
    ("ETHOSLTD", 0.96),        # Ethos Ltd.
    ("KIMS", 0.92),            # Krishna Institute Of Medical Sciences Limited
    ("CORONA", 0.90),          # Corona Remedies Limited
    ("AGARWALEYE", 0.73),      # Dr Agarwals Health Care Limited
    ("TIMKEN", 0.54),          # Timken India Limited
    ("BANSALWIRE", 0.47),      # Bansal Wire Industries Limited
    ("MAXESTATES", 0.43),      # Max Estates Limited
    ("WEWORK", 0.37),          # Wework India Management Limited
    ("VMM", 0.18),             # Vishal Mega Mart Limited
    ("CARBORUNIV", 0.09),      # Carborundum Universal Limited
    ("SONATSOFTW", 0.07),      # Sonata Software Limited

]

# =========================
# FETCH LIVE DATA
# =========================
#
# WHY PRICES WERE WRONG IN THE OLD VERSION:
#
# The old fetch did ONE batched yf.download(period="10d", interval="1d")
# call and nothing else. That only ever returns DAILY BARS. During
# market hours, "today's" daily bar for an NSE ticker frequently isn't
# updated intraday the way a live quote is -- so "Live Price" was
# regularly just showing yesterday's (or an even older) daily close,
# not the actual current traded price. There was no live/intraday
# source at all, unlike the sister Motilal Oswal tracker, which is why
# that one moves correctly and this one didn't.
#
# FIX -- adopt the same 3-tier fetch used by the Motilal Oswal tracker,
# which IS producing correct live movement:
#
#   Tier 1 (primary):   NSE's own quote API (previousClose + lastPrice,
#                        both authoritative, straight from the exchange)
#   Tier 2 (secondary):  Yahoo's chart-API meta block
#                        (chartPreviousClose / regularMarketPrice) --
#                        values Yahoo states directly, computed on
#                        their side. NOT yfinance's fast_info, whose
#                        previousClose is derived client-side from
#                        hourly bars and was returning the wrong
#                        session's close for NSE tickers.
#   Tier 3 (last resort): our own derivation from batched daily +
#                        intraday candle history, only used if both
#                        Tier 1 and Tier 2 fail for a symbol
#
# All three tiers are fetched CONCURRENTLY across all symbols, each
# bounded by its own hard timeout, and the per-symbol loop that builds
# the table does ZERO network I/O -- it only reads from the pre-fetched
# batches. This is the same pattern that fixed both the "frozen page"
# and "wrong price" bugs on the Motilal tracker.
#
# A staleness guard (keyed by symbol+date, so it resets every trading
# day) still protects ONLY the Tier 3 derived path, since Tier 1/2 are
# authoritative exchange/vendor quotes with nothing to validate them
# against.

STALE_GUARD_PCT = 3.0     # max allowed jump in previous_close vs last known-good, in % (Tier 3 only)
NSE_REQUEST_TIMEOUT = 5   # per-request timeout, seconds
NSE_BATCH_TIMEOUT = 20    # hard ceiling for ALL NSE requests combined
YF_BATCH_TIMEOUT = 15     # hard ceiling for each batched yfinance call

if "last_good_data" not in st.session_state:
    st.session_state["last_good_data"] = {}

if "last_good_prev_close" not in st.session_state:
    # {symbol: {"date": "YYYY-MM-DD", "value": float}} -- staleness
    # guard baseline, used only for the Tier 3 derived path.
    st.session_state["last_good_prev_close"] = {}

if "nse_session" not in st.session_state:
    st.session_state["nse_session"] = None

symbol_list = [s for s, _ in stocks]
tickers_list = [s + ".NS" for s in symbol_list]

NSE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/get-quotes/equity",
}


def get_nse_session():
    """Reuse one requests.Session across reruns so we don't re-negotiate
    NSE's anti-bot cookies on every refresh."""
    session = st.session_state.get("nse_session")
    if session is None:
        session = requests.Session()
        session.headers.update(NSE_HEADERS)
        try:
            session.get("https://www.nseindia.com", timeout=NSE_REQUEST_TIMEOUT)
        except Exception:
            pass
        st.session_state["nse_session"] = session
    return session


def _fetch_one_nse(symbol, session):
    """Single-symbol NSE fetch. Called from a thread pool, never
    directly from the main per-symbol loop."""
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    try:
        resp = session.get(url, timeout=NSE_REQUEST_TIMEOUT)
        if resp.status_code != 200:
            resp = session.get(url, timeout=NSE_REQUEST_TIMEOUT)
        if resp.status_code != 200:
            return symbol, None, None, f"HTTP {resp.status_code}"
        data = resp.json()
        price_info = data.get("priceInfo", {})
        live_price = price_info.get("lastPrice")
        prev_close = price_info.get("previousClose")
        if live_price and prev_close:
            return symbol, float(prev_close), float(live_price), None
        return symbol, None, None, "missing priceInfo fields (likely bot-blocked page)"
    except ValueError:
        return symbol, None, None, "non-JSON response (likely bot-block HTML page)"
    except requests.exceptions.Timeout:
        return symbol, None, None, "timeout"
    except Exception as e:
        return symbol, None, None, f"{type(e).__name__}"


@st.cache_data(ttl=REFRESH_SECONDS, show_spinner=False)
def fetch_nse_batch(symbols):
    """PRIMARY source. Fetches ALL symbols concurrently via a thread
    pool, bounded by ONE overall timeout."""
    session = get_nse_session()
    results = {}
    errors = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(_fetch_one_nse, s, session): s for s in symbols}
        try:
            for fut in concurrent.futures.as_completed(futures, timeout=NSE_BATCH_TIMEOUT):
                s = futures[fut]
                try:
                    _, prev_close, live_price, err = fut.result()
                except Exception as e:
                    prev_close, live_price, err = None, None, str(e)
                results[s] = (prev_close, live_price)
                if err:
                    errors[s] = err
        except concurrent.futures.TimeoutError:
            for fut, s in futures.items():
                if s not in results:
                    results[s] = (None, None)
                    errors[s] = "timeout (overall NSE batch)"

    return results, errors


YF_CHART_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"

YF_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json,text/plain,*/*",
}


def _fetch_one_yf_quote(ticker):
    """TIER 2 -- Yahoo CHART API meta.

    THIS REPLACES THE OLD fast_info CALL, WHICH WAS THE ACTUAL CAUSE OF
    THE WRONG PREVIOUS CLOSES.

    `fast_info.previousClose` is NOT a raw field off Yahoo's servers.
    yfinance DERIVES it: it pulls a week of hourly bars (including
    pre/post-market), groups them by calendar date, and takes the
    second-to-last day's close. On .NS tickers that grouping regularly
    lands one session too far back -- which is why FEDERALBNK showed
    334.50 when the real previous close was 332.75 (live price 331.60
    was correct, because lastPrice IS a raw field). Every symbol was
    hitting this because NSE is blocked on Streamlit Cloud, so Tier 2
    was serving the whole table.

    The chart endpoint's `meta` block instead gives Yahoo's OWN STATED
    values, computed on their side, no client-side derivation:
      - chartPreviousClose  -> previous session's official close
      - regularMarketPrice  -> current live traded price
    One HTTP request per ticker, fetched concurrently, so it's no
    slower than fast_info (which also made its own request).
    """
    try:
        resp = requests.get(
            YF_CHART_URL.format(ticker=ticker),
            params={"range": "1d", "interval": "1m"},
            headers=YF_HEADERS,
            timeout=NSE_REQUEST_TIMEOUT,
        )
        if resp.status_code != 200:
            return ticker, None, None, f"HTTP {resp.status_code}"

        payload = resp.json()
        result = (payload.get("chart", {}).get("result") or [None])[0]
        if not result:
            err = payload.get("chart", {}).get("error")
            return ticker, None, None, f"no result ({err})"

        meta = result.get("meta", {})

        # chartPreviousClose is the previous SESSION's close for the
        # requested range -- the value we actually want. previousClose
        # is kept only as a secondary in case the former is absent.
        prev_close = meta.get("chartPreviousClose") or meta.get("previousClose")
        live_price = meta.get("regularMarketPrice")

        # If the market is closed / regularMarketPrice is missing, fall
        # back to the last non-null 1-minute close in the same payload
        # (same source, same session -- no cross-source reconciliation).
        if live_price is None:
            try:
                closes = result["indicators"]["quote"][0]["close"]
                for c in reversed(closes):
                    if c is not None:
                        live_price = c
                        break
            except Exception:
                pass

        if prev_close and live_price:
            return ticker, float(prev_close), float(live_price), None
        return ticker, None, None, "missing chart meta fields"

    except ValueError:
        return ticker, None, None, "non-JSON response"
    except requests.exceptions.Timeout:
        return ticker, None, None, "timeout"
    except Exception as e:
        return ticker, None, None, f"{type(e).__name__}"


@st.cache_data(ttl=REFRESH_SECONDS, show_spinner=False)
def fetch_yf_quote_batch(tickers):
    """TIER 2 (secondary) source, used when NSE fails -- which on
    Streamlit Cloud is effectively ALWAYS, since NSE blocks datacenter
    IPs. This tier therefore serves the whole table in practice, so it
    has to be right: it reads Yahoo's chart-API meta (stated previous
    close + stated live price), not yfinance's client-side fast_info
    derivation. Fetches ALL tickers CONCURRENTLY, bounded by ONE
    timeout."""
    results = {}
    errors = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(_fetch_one_yf_quote, t): t for t in tickers}
        try:
            for fut in concurrent.futures.as_completed(futures, timeout=YF_BATCH_TIMEOUT):
                t = futures[fut]
                try:
                    _, prev_close, live_price, err = fut.result()
                except Exception as e:
                    prev_close, live_price, err = None, None, str(e)
                results[t] = (prev_close, live_price)
                if err:
                    errors[t] = err
        except concurrent.futures.TimeoutError:
            for fut, t in futures.items():
                if t not in results:
                    results[t] = (None, None)
                    errors[t] = "timeout (overall yfinance quote batch)"

    return results, errors


def _download_with_timeout(kwargs, timeout_seconds):
    """Runs a yf.download() call in a worker thread with a hard
    timeout, since yfinance itself sets none."""
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            future = ex.submit(lambda: yf.download(**kwargs))
            return future.result(timeout=timeout_seconds)
    except concurrent.futures.TimeoutError:
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=REFRESH_SECONDS, show_spinner=False)
def fetch_daily_batch(tickers):
    """TIER 3 (last-resort) source for previous close: ONE batched,
    threaded call for ALL tickers' recent daily bars."""
    return _download_with_timeout(
        dict(
            tickers=tickers,
            period="10d",
            interval="1d",
            group_by="ticker",
            threads=True,
            progress=False,
            auto_adjust=False,
        ),
        YF_BATCH_TIMEOUT,
    )


@st.cache_data(ttl=REFRESH_SECONDS, show_spinner=False)
def fetch_intraday_batch(tickers):
    """Tier 3 live-price source: ONE batched, threaded call for ALL
    tickers' 1-minute intraday bars."""
    return _download_with_timeout(
        dict(
            tickers=tickers,
            period="1d",
            interval="1m",
            group_by="ticker",
            threads=True,
            progress=False,
            auto_adjust=False,
        ),
        YF_BATCH_TIMEOUT,
    )


def get_prev_close_from_daily(ticker, daily_batch, intraday_batch):
    """Previous close = last COMPLETE daily bar, pulled from the
    pre-fetched daily batch. No network I/O.

    Decides whether the last daily row is "today's still-forming bar"
    by comparing it against yfinance's OWN intraday bar dates (same
    source/normalization as the daily bars), rather than against a
    separately-computed Python-clock date -- avoids the two sources of
    "what day is it" disagreeing with each other.
    """
    try:
        if daily_batch is None or daily_batch.empty:
            return None
        if isinstance(daily_batch.columns, pd.MultiIndex):
            daily_hist = daily_batch[ticker]["Close"].dropna()
        else:
            daily_hist = daily_batch["Close"].dropna()

        if daily_hist.empty:
            return None

        last_daily_ts = daily_hist.index[-1]
        last_daily_date = pd.Timestamp(last_daily_ts).date()

        intraday_last_date = None
        try:
            if intraday_batch is not None and not intraday_batch.empty:
                if isinstance(intraday_batch.columns, pd.MultiIndex):
                    intraday_hist = intraday_batch[ticker]["Close"].dropna()
                else:
                    intraday_hist = intraday_batch["Close"].dropna()
                if len(intraday_hist) >= 1:
                    intraday_last_date = pd.Timestamp(intraday_hist.index[-1]).date()
        except Exception:
            intraday_last_date = None

        if intraday_last_date is not None and last_daily_date == intraday_last_date:
            # Last daily row is today's in-progress session -> drop it.
            if len(daily_hist) >= 2:
                return float(daily_hist.iloc[-2])
            return None

        return float(daily_hist.iloc[-1])
    except Exception:
        pass
    return None


def get_live_price_from_intraday(ticker, batch_data):
    """Live price = most recent 1-minute intraday close, pulled from
    the pre-fetched intraday batch. No network I/O. Falls back to the
    daily batch's last close if intraday data is unavailable (e.g.
    market closed)."""
    try:
        if batch_data is not None and not batch_data.empty:
            if isinstance(batch_data.columns, pd.MultiIndex):
                hist = batch_data[ticker]["Close"].dropna()
            else:
                hist = batch_data["Close"].dropna()
            if len(hist) >= 1:
                return float(hist.iloc[-1])
    except Exception:
        pass
    return None


def validate_prev_close(symbol, prev_close, source):
    """
    STALENESS GUARD -- keyed by (symbol, date) so the baseline resets
    every trading day instead of persisting indefinitely on a warm
    Streamlit Cloud instance.

    NSE's own previousClose and Yahoo's own quote previousClose
    (Tier 2, "yahoo-chart") are trusted outright and skip the
    guard entirely -- they're authoritative values straight from the
    exchange/vendor. The guard only protects the Tier 3
    "yfinance-daily-derived" path, which is the one that derives
    previous-close from historical candles ourselves and can
    occasionally land on a bad bar.
    """
    today_str = datetime.now(ZoneInfo("Asia/Kolkata")).date().isoformat()

    if source in ("NSE", "yahoo-chart"):
        st.session_state["last_good_prev_close"][symbol] = {
            "date": today_str,
            "value": prev_close,
        }
        return prev_close, True

    entry = st.session_state["last_good_prev_close"].get(symbol)

    if entry is None or entry.get("date") != today_str:
        st.session_state["last_good_prev_close"][symbol] = {
            "date": today_str,
            "value": prev_close,
        }
        return prev_close, True

    last_good = entry["value"]
    deviation_pct = abs(prev_close - last_good) / last_good * 100

    if deviation_pct > STALE_GUARD_PCT:
        return last_good, False

    st.session_state["last_good_prev_close"][symbol] = {
        "date": today_str,
        "value": prev_close,
    }
    return prev_close, True


# --- Fetch all sources ONCE, up front, each bounded by its own hard
# --- timeout. The per-symbol loop below does NO network I/O.

nse_results, nse_errors = fetch_nse_batch(tuple(symbol_list))

need_tier2 = any(
    nse_results.get(s, (None, None))[0] is None
    or nse_results.get(s, (None, None))[1] is None
    for s in symbol_list
)

yf_quote_results, yf_quote_errors = (
    fetch_yf_quote_batch(tuple(tickers_list)) if need_tier2 else ({}, {})
)

need_tier3 = any(
    (nse_results.get(s, (None, None))[0] is None or nse_results.get(s, (None, None))[1] is None)
    and (
        yf_quote_results.get(s + ".NS", (None, None))[0] is None
        or yf_quote_results.get(s + ".NS", (None, None))[1] is None
    )
    for s in symbol_list
)

daily_batch = fetch_daily_batch(tuple(tickers_list)) if need_tier3 else None
intraday_batch = fetch_intraday_batch(tuple(tickers_list)) if need_tier3 else None

rows = []
total_weighted_return = 0
stale_symbols = []          # Tier-3 staleness guard fired this cycle
never_fetched_symbols = []  # no data AND no cache to fall back to

for symbol, weight in stocks:

    ticker = symbol + ".NS"

    prev_close, live_price = nse_results.get(symbol, (None, None))
    source = "NSE"

    if prev_close is None or live_price is None:
        q_prev, q_live = yf_quote_results.get(ticker, (None, None))
        prev_close = prev_close if prev_close is not None else q_prev
        live_price = live_price if live_price is not None else q_live
        source = "yahoo-chart"

    if prev_close is None or live_price is None:
        fb_prev = get_prev_close_from_daily(ticker, daily_batch, intraday_batch)
        fb_live = get_live_price_from_intraday(ticker, intraday_batch)
        prev_close = prev_close if prev_close is not None else fb_prev
        live_price = live_price if live_price is not None else fb_live
        source = "yfinance-daily-derived"

    if prev_close is not None and live_price is not None:

        validated_prev_close, accepted = validate_prev_close(symbol, prev_close, source)
        if not accepted:
            source = f"{source} (rejected, using last-good)"
            stale_symbols.append(symbol)
        prev_close = validated_prev_close

        change_pct = (
            (live_price - prev_close)
            / prev_close
        ) * 100 if prev_close else 0

        weighted_return = (
            change_pct * weight
        ) / 100

        row = [
            symbol,
            round(weight, 2),
            round(prev_close, 2),
            round(live_price, 2),
            round(change_pct, 2),
            source,
        ]

        st.session_state["last_good_data"][symbol] = row
        total_weighted_return += weighted_return

    else:
        # No fresh data at all this refresh -> reuse last known good
        # values instead of showing 0.
        cached_row = st.session_state["last_good_data"].get(symbol)

        if cached_row is not None:
            row = cached_row
            cached_change_pct = row[4]
            weighted_return = (cached_change_pct * weight) / 100
            total_weighted_return += weighted_return
            stale_symbols.append(symbol)
        else:
            row = [symbol, weight, 0, 0, 0, "no data"]
            never_fetched_symbols.append(symbol)

    rows.append(row)

if never_fetched_symbols:
    st.info(
        "ℹ️ No data (fresh or cached) yet for: "
        + ", ".join(never_fetched_symbols)
        + ". These show as 0 until a successful fetch comes through."
    )
elif stale_symbols:
    preview = ", ".join(stale_symbols[:6])
    more = f" +{len(stale_symbols) - 6} more" if len(stale_symbols) > 6 else ""
    st.markdown(
        f'<div class="stale-badge">⚠️ {len(stale_symbols)} symbol(s) fell back to '
        f'cached/last-known-good values this refresh: {preview}{more}</div>',
        unsafe_allow_html=True,
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
        "% Change",
        "Source",

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
# DEBUG: DATA SOURCE PER STOCK
# =========================

with st.expander("🛠️ Debug: Data source per stock", expanded=False):
    st.dataframe(
        df[["Stock", "Previous Close", "Live Price", "Source"]],
        use_container_width=True
    )

    if nse_errors:
        st.markdown("**NSE fetch failures this cycle:**")
        nse_error_df = pd.DataFrame(
            [{"Stock": s, "NSE Error": e} for s, e in nse_errors.items()]
        )
        st.dataframe(nse_error_df, use_container_width=True)
        st.caption(
            "If every symbol shows an error here (especially "
            "'non-JSON response' or 'HTTP 403'), NSE is very likely "
            "blocking requests from this host's IP address -- common on "
            "Streamlit Community Cloud. In that case the app runs on "
            "Yahoo's own quote fields instead (Source column shows "
            "'yahoo-chart'). 'yfinance-daily-derived' means even "
            "Yahoo's quote fields failed for that symbol and it fell "
            "back to candle-derived data, the least reliable tier."
        )
    else:
        st.caption("NSE responded successfully for all symbols this cycle.")

    if 'yf_quote_errors' in dir() and yf_quote_errors:
        st.markdown("**Yahoo quote (Tier 2) failures this cycle:**")
        yf_error_df = pd.DataFrame(
            [{"Ticker": t, "Error": e} for t, e in yf_quote_errors.items()]
        )
        st.dataframe(yf_error_df, use_container_width=True)

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

st.subheader("📊 Portfolio Holdings (with live pricing)")

st.dataframe(
    styled_df,
    use_container_width=True,
    height=850
)

st.markdown("---")

st.caption(f"© Debrup Bera | Auto-refresh every {REFRESH_SECONDS} seconds")
