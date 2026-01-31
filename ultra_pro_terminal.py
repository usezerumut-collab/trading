import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. CONFIG & DARK THEME ---
st.set_page_config(page_title="GALAXY HQ | DARK", layout="wide", initial_sidebar_state="collapsed")

# Arka planı simsiyah, yazıları bembeyaz yapan CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&display=swap');
    
    .stApp { background-color: #000000 !important; color: #ffffff !important; }
    header, footer { visibility: hidden !important; }
    
    /* Sekme ve Buton Tasarımları */
    .stTabs [data-baseweb="tab-list"] button { color: #ffffff !important; font-family: 'Space Grotesk'; }
    .stButton > button { 
        background: #1e1e1e !important; color: #00ff00 !important; 
        border: 1px solid #00ff00 !important; border-radius: 5px;
        font-weight: bold; width: 100%;
    }
    .stButton > button:hover { background: #00ff00 !important; color: #000 !important; }
    
    /* Mesaj Kartları */
    .chat-card { 
        background: #111111; padding: 15px; border-radius: 10px; 
        border: 1px solid #333; margin-bottom: 10px; color: #eee;
    }
    
    /* Input Alanları */
    input, textarea { background-color: #111 !important; color: white !important; border: 1px solid #444 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BAĞLANTI AYARLARI ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1HbSdgHwC-56zUtsLku8Vq4eQbGg3qrH1dUdjB8-nBzg/edit?usp=sharing"

def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # ttl=0 yaparak her seferinde taze veri çekiyoruz
        return conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)
    except Exception as e:
        return pd.DataFrame(columns=["user", "message", "timestamp"])

def send_data(u, m):
    try:
        df = get_data()
        new_row = pd.DataFrame([{"user": u, "message": m, "timestamp": datetime.now().strftime("%H:%M")}])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        return True
    except Exception as e:
        st.error(f"Detaylı Hata: {e}") # Hatayı buraya yazdırıyoruz ki anlayalım
        return False

# Session States
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = ""
if 'page' not in st.session_state: st.session_state.page = "📈 TERMINAL"

# --- 3. AKIŞ ---
if not st.session_state.auth:
    _, cent, _ = st.columns([1, 1, 1])
    with cent:
        st.markdown("<h1 style='text-align:center; color:#00ff00;'>GALAXY HQ</h1>", unsafe_allow_html=True)
        u_id = st.text_input("COMMANDER ID")
        if st.button("LOGIN"):
            if u_id:
                st.session_state.user = u_id; st.session_state.auth = True; st.rerun()
else:
    # MENÜ
    m1, m2, m3, m4 = st.columns(4)
    if m1.button("📈 CHART"): st.session_state.page = "📈 TERMINAL"; st.rerun()
    if m2.button("🔥 NEWS"): st.session_state.page = "🔥 NEWS"; st.rerun()
    if m3.button("💬 SQUAD"): st.session_state.page = "💬 SQUAD"; st.rerun()
    if m4.button("🔴 EXIT"): st.session_state.auth = False; st.rerun()

    st.markdown("<hr style='border: 1px solid #333'>", unsafe_allow_html=True)

    if st.session_state.page == "📈 TERMINAL":
        c1, c2 = st.columns([3, 1])
        with c1:
            t1, t2 = st.tabs(["GOLD (XAUUSD)", "EURUSD"])
            with t1: components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=15&theme=dark" width="100%" height="600"></iframe>', height=610)
            with t2: components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=FX:EURUSD&interval=15&theme=dark" width="100%" height="600"></iframe>', height=610)
        with c2:
            st.markdown("### DATA FEED")
            components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=D&theme=dark" width="100%" height="300"></iframe>', height=310)

    elif st.session_state.page == "🔥 NEWS":
        st.markdown("### EKONOMİK TAKVİM")
        # Haberler kısmını düzelten güncel widget
        components.html('<div style="height:800px;"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>{"colorTheme":"dark","isTransparent":false,"width":"100%","height":"100%","locale":"tr","importanceFilter":"-1,0,1"}</script></div>', height=800)

    elif st.session_state.page == "💬 SQUAD":
        l, r = st.columns([1, 2])
        with l:
            msg = st.text_area("Mesajını buraya bırak...")
            if st.button("SİSTEME GÖNDER"):
                if msg:
                    if send_data(st.session_state.user, msg):
                        st.success("İletildi!"); st.rerun()
        with r:
            st.write("### SQUAD MESSAGES")
            data = get_data()
            if not data.empty:
                for i, row in data.iloc[::-1].head(15).iterrows():
                    st.markdown(f'<div class="chat-card"><b style="color:#00ff00;">@{row["user"]}</b><br>{row["message"]} <br><small style="color:#666;">{row["timestamp"]}</small></div>', unsafe_allow_html=True)
