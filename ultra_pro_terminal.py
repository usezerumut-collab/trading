import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. CONFIG ---
st.set_page_config(page_title="GALAXY HQ | PRO", layout="wide", initial_sidebar_state="collapsed")

# Kendi Sheets linkini buraya yapıştır kanka
SHEET_URL = "https://docs.google.com/spreadsheets/d/1HbSdgHwC-56zUtsLku8Vq4eQbGg3qrH1dUdjB8-nBzg/edit?usp=sharing"

# BAĞLANTIYI KONTROL ETMEK İÇİN ÖZEL FONKSİYON
def get_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Eğer Sheet1 ismi yanlışsa veya tablo boşsa hata almamak için
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)
        return df
    except Exception as e:
        # Eğer tablo boşsa veya ulaşılamıyorsa boş bir yapı oluştur
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

# Session State Ayarları
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = ""
if 'page' not in st.session_state: st.session_state.page = "📈 TERMINAL"

# --- 2. CSS (NET SİYAH BEYAZ) ---
st.markdown("""
    <style>
    .stApp { background: #f8f9fa !important; color: #000; }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: #000 !important; font-weight: 800 !important; font-size: 18px !important;
    }
    .stButton > button { background: #000 !important; color: #fff !important; border-radius: 10px; }
    .chat-card { background: white; padding: 15px; border-radius: 12px; border: 1px solid #ddd; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.auth:
    _, cent, _ = st.columns([1, 1, 1])
    with cent:
        st.title("GALAXY HQ")
        u_id = st.text_input("Commander ID")
        if st.button("AUTHENTICATE"):
            if u_id:
                st.session_state.user = u_id
                st.session_state.auth = True
                st.rerun()
else:
    # MENÜ
    cols = st.columns(4)
    if cols[0].button("📈 TERMINAL"): st.session_state.page = "📈 TERMINAL"; st.rerun()
    if cols[1].button("🔥 NEWS"): st.session_state.page = "🔥 NEWS"; st.rerun()
    if cols[2].button("💬 SQUAD HUB"): st.session_state.page = "💬 SQUAD HUB"; st.rerun()
    if cols[3].button("🔴 EXIT"): st.session_state.auth = False; st.rerun()

    st.divider()

    if st.session_state.page == "📈 TERMINAL":
        c1, c2 = st.columns([3, 1])
        with c1:
            t1, t2, t3 = st.tabs(["EUR/USD", "GOLD", "SILVER"])
            with t1: components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=FX:EURUSD&interval=15&theme=light" width="100%" height="500"></iframe>', height=510)
            with t2: components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=15&theme=light" width="100%" height="500"></iframe>', height=510)
            with t3: components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAGUSD&interval=15&theme=light" width="100%" height="500"></iframe>', height=510)
        with c2:
            st.write("### LIVE")
            components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=D&theme=light" width="100%" height="200"></iframe>', height=210)

    elif st.session_state.page == "💬 SQUAD HUB":
        l, r = st.columns([1, 2])
        with l:
            msg = st.text_area("Mesaj yaz...")
            if st.button("GÖNDER"):
                if msg:
                    if send_data(st.session_state.user, msg):
                        st.success("İşlendi!")
                        st.rerun()
                    else: st.error("Bağlantı hatası!")
        with r:
            st.write("### MESAJLAR")
            data = get_data()
            if not data.empty:
                for i, row in data.iloc[::-1].iterrows():
                    st.markdown(f'<div class="chat-card"><b>@{row["user"]}</b>: {row["message"]} <br><small>{row["timestamp"]}</small></div>', unsafe_allow_html=True)
            else:
                st.info("Henüz mesaj yok.")
