import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. AYARLAR & BAĞLANTI ---
st.set_page_config(page_title="GALAXY HQ | PRO", layout="wide", initial_sidebar_state="collapsed")

# BURAYA O ATTIĞIN LINKI TIRNAKLARIN İÇİNE YAPIŞTIR
SHEET_URL = "https://docs.google.com/spreadsheets/d/1HbSdgHwC-56zUtsLku8Vq4eQbGg3qrH1dUdjB8-nBzg/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        # Sheet1 yazan yer e-tablonun altındaki sekme ismidir, orası aynı kalmalı
        return conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1")
    except:
        return pd.DataFrame(columns=["user", "message", "timestamp"])

def send_data(u, m):
    df = get_data()
    new_row = pd.DataFrame([{"user": u, "message": m, "timestamp": datetime.now().strftime("%H:%M")}])
    updated_df = pd.concat([df, new_row], ignore_index=True)
    conn.update(spreadsheet=SHEET_URL, data=updated_df)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = ""
if 'page' not in st.session_state: st.session_state.page = "📈 TERMINAL"

# --- 2. TASARIM (SİYAH BEYAZ VE NET) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;600&display=swap');
    header, footer { visibility: hidden !important; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%) !important; color: #000; font-family: 'Inter', sans-serif; }
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: #000000 !important; font-weight: 800 !important; font-size: 18px !important;
    }
    
    .stButton > button {
        width: 100%; background: #000 !important; color: #fff !important;
        border: none !important; border-radius: 10px !important; padding: 12px !important;
        font-family: 'Space Grotesk' !important; font-weight: 600 !important;
    }
    
    .chat-card {
        background: white; padding: 15px; border-radius: 15px; border: 1px solid #eee;
        margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GİRİŞ PANELİ ---
if not st.session_state.auth:
    st.write("<br><br><br>", unsafe_allow_html=True)
    _, cent, _ = st.columns([1, 1.2, 1])
    with cent:
        st.markdown('<div style="text-align:center; background:#000; color:#fff; padding:10px; border-radius:50px; font-weight:700; letter-spacing:5px; margin-bottom:10px;">DİSİPLİN & SABIR</div>', unsafe_allow_html=True)
        st.markdown('<div style="background:white; padding:50px; border-radius:30px; border:1px solid #eee; text-align:center;"><h1 style="color:#000; font-family:Space Grotesk;">GALAXY HQ</h1><p style="color:#888; letter-spacing:2px;">WELCOME COMMANDER</p></div>', unsafe_allow_html=True)
        u_id = st.text_input("ID", placeholder="İsmin...", key="login_id")
        if st.button("WELCOME"):
            if u_id:
                st.session_state.user = u_id
                st.session_state.auth = True
                st.rerun()
else:
    # --- MENÜ ---
    n1, n2, n3, n4 = st.columns(4)
    if n1.button("📈 TERMINAL"): st.session_state.page = "📈 TERMINAL"; st.rerun()
    if n2.button("🔥 FOREX NEWS"): st.session_state.page = "🔥 NEWS"; st.rerun()
    if n3.button("💬 SQUAD HUB"): st.session_state.page = "💬 SQUAD"; st.rerun()
    if n4.button("🔴 EXIT"): st.session_state.auth = False; st.rerun()

    st.divider()

    # --- SAYFALAR ---
    if st.session_state.page == "📈 TERMINAL":
        c_main, c_side = st.columns([3, 1])
        with c_main:
            t1, t2, t3 = st.tabs(["EUR / USD", "XAU / USD (GOLD)", "XAG / USD (SILVER)"])
            with t1: components.html('<div style="height:550px;"><div id="c1" style="height:100%;"></div><script src="https://s3.tradingview.com/tv.js"></script><script>new TradingView.widget({"autosize":true,"symbol":"FX:EURUSD","interval":"15","theme":"light","style":"1","locale":"tr","container_id":"c1"});</script></div>', height=560)
            with t2: components.html('<div style="height:550px;"><div id="c2" style="height:100%;"></div><script src="https://s3.tradingview.com/tv.js"></script><script>new TradingView.widget({"autosize":true,"symbol":"OANDA:XAUUSD","interval":"15","theme":"light","style":"1","locale":"tr","container_id":"c2"});</script></div>', height=560)
            with t3: components.html('<div style="height:550px;"><div id="c3" style="height:100%;"></div><script src="https://s3.tradingview.com/tv.js"></script><script>new TradingView.widget({"autosize":true,"symbol":"OANDA:XAGUSD","interval":"15","theme":"light","style":"1","locale":"tr","container_id":"c3"});</script></div>', height=560)
        with c_side:
            st.markdown("### 📊 LIVE DATA")
            components.html('<script src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>{"symbol":"OANDA:XAUUSD","width":"100%","height":200,"locale":"tr","colorTheme":"light"}</script>', height=210)
            components.html('<script src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>{"symbol":"OANDA:XAGUSD","width":"100%","height":200,"locale":"tr","colorTheme":"light"}</script>', height=210)

    elif st.session_state.page == "🔥 NEWS":
        components.html('<div style="height:800px;"><script src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>{"colorTheme":"light","width":"100%","height":"100%","locale":"tr","importanceFilter":"0,1"}</script></div>', height=800)

    elif st.session_state.page == "💬 SQUAD HUB":
        s_l, s_r = st.columns([1, 2])
        with s_l:
            st.markdown("### MESAJ GÖNDER")
            msg = st.text_area("Notun:", key="squad_msg")
            if st.button("SİSTEME YÜKLE"):
                if msg:
                    send_data(st.session_state.user, msg)
                    st.success("Gönderildi!")
                    st.rerun()
        with s_r:
            st.markdown("### SQUAD FEED")
            data = get_data()
            if not data.empty:
                for index, row in data.iloc[::-1].iterrows():
                    st.markdown(f'<div class="chat-card"><b>@{row["user"]}</b> <small style="color:#999">{row["timestamp"]}</small><br>{row["message"]}</div>', unsafe_allow_html=True)

    # FOOTER
    st.markdown('<div style="position:fixed; bottom:0; left:0; width:100%; background:white; border-top:1px solid #eee; z-index:99;">', unsafe_allow_html=True)
    components.html('<script src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>{"symbols": [{"proName": "FX_IDC:EURUSD", "title": "EUR/USD"}, {"proName": "OANDA:XAUUSD", "title": "GOLD"}, {"proName": "OANDA:XAGUSD", "title": "SILVER"}], "colorTheme": "light"}</script>', height=50)
    st.markdown('</div>', unsafe_allow_html=True)