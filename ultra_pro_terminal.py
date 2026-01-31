import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. AYARLAR ---
st.set_page_config(page_title="GALAXY HQ | PRO", layout="wide", initial_sidebar_state="collapsed")

# Bağlantıyı her seferinde temizle (Beyaz ekran ve bağlantı hatasını önlemek için)
st.cache_data.clear()

# SENİN LINKIN
SHEET_URL = "https://docs.google.com/spreadsheets/d/1HbSdgHwC-56zUtsLku8Vq4eQbGg3qrH1dUdjB8-nBzg/edit?usp=sharing"

def get_data():
    try:
        # ttl=0 bağlantının bayatlamasını engeller
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)
        return df
    except:
        return pd.DataFrame(columns=["user", "message", "timestamp"])

def send_data(u, m):
    try:
        df = get_data()
        new_row = pd.DataFrame([{"user": u, "message": m, "timestamp": datetime.now().strftime("%H:%M")}])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        return True
    except:
        return False

# Session State
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = ""
if 'page' not in st.session_state: st.session_state.page = "📈 TERMINAL"

# --- 2. TASARIM ---
st.markdown("""
    <style>
    .stApp { background: #f8f9fa !important; color: #000; }
    .stButton > button { background: #000 !important; color: #fff !important; border-radius: 10px; }
    .chat-card { background: white; padding: 15px; border-radius: 12px; border: 1px solid #ddd; margin-bottom: 10px; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AKIŞ ---
if not st.session_state.auth:
    _, cent, _ = st.columns([1, 1, 1])
    with cent:
        st.title("GALAXY HQ")
        u_id = st.text_input("Commander ID", key="login_box")
        if st.button("AUTHENTICATE"):
            if u_id:
                st.session_state.user = u_id
                st.session_state.auth = True
                st.rerun()
else:
    # MENÜ
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("📈 TERMINAL"): st.session_state.page = "📈 TERMINAL"; st.rerun()
    if c2.button("🔥 NEWS"): st.session_state.page = "🔥 NEWS"; st.rerun()
    if c3.button("💬 SQUAD HUB"): st.session_state.page = "💬 SQUAD HUB"; st.rerun()
    if c4.button("🔴 EXIT"): st.session_state.auth = False; st.rerun()

    st.divider()

    if st.session_state.page == "📈 TERMINAL":
        main, side = st.columns([3, 1])
        with main:
            t1, t2, t3 = st.tabs(["EUR/USD", "GOLD", "SILVER"])
            with t1: components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=FX:EURUSD&interval=15&theme=light" width="100%" height="500"></iframe>', height=510)
            with t2: components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=15&theme=light" width="100%" height="500"></iframe>', height=510)
            with t3: components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAGUSD&interval=15&theme=light" width="100%" height="500"></iframe>', height=510)
        with side:
            st.write("### MARKET")
            components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=D&theme=light" width="100%" height="200"></iframe>', height=210)

    elif st.session_state.page == "💬 SQUAD HUB":
        l, r = st.columns([1, 2])
        with l:
            st.write("### MESAJ GÖNDER")
            msg = st.text_area("Notun...", key="msg_area")
            if st.button("SİSTEME YÜKLE"):
                if msg:
                    if send_data(st.session_state.user, msg):
                        st.success("Mesaj Tabloya Çakıldı!")
                        st.rerun()
                    else:
                        st.error("Bağlantı Hatası! Lütfen Google Sheet 'Düzenleyici' iznini kontrol et.")
        with r:
            st.write("### SQUAD FEED")
            data = get_data()
            if not data.empty:
                # Sadece son 20 mesajı göster ki sayfa kasmasın
                for i, row in data.iloc[::-1].head(20).iterrows():
                    st.markdown(f'<div class="chat-card"><b>@{row["user"]}</b>: {row["message"]} <br><small style="color:gray;">{row["timestamp"]}</small></div>', unsafe_allow_html=True)
            else:
                st.info("Henüz mesaj yok veya bağlantı kuruluyor...")
