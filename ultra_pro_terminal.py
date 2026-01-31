import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. CONFIG & DARK THEME ---
st.set_page_config(page_title="GALAXY HQ | DARK", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #ffffff !important; }
    header, footer { visibility: hidden !important; }
    .stButton > button { 
        background: #1e1e1e !important; color: #00ff00 !important; 
        border: 1px solid #00ff00 !important; border-radius: 5px; width: 100%;
    }
    .chat-card { 
        background: #111111; padding: 15px; border-radius: 10px; 
        border: 1px solid #333; margin-bottom: 10px; color: #eee;
    }
    input, textarea { background-color: #111 !important; color: white !important; border: 1px solid #444 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE BAĞLANTISI ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def get_data():
    try:
        response = supabase.table("messages").select("*").order("id", desc=True).limit(20).execute()
        return pd.DataFrame(response.data)
    except:
        return pd.DataFrame(columns=["user", "message", "timestamp"])

def send_data(u, m):
    try:
        data = {"user": u, "message": m, "timestamp": datetime.now().strftime("%H:%M")}
        supabase.table("messages").insert(data).execute()
        return True
    except:
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
        components.html('<div style="height:800px;"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>{"colorTheme":"dark","isTransparent":false,"width":"100%","height":"100%","locale":"tr","importanceFilter":"-1,0,1"}</script></div>', height=800)

    elif st.session_state.page == "💬 SQUAD":
        l, r = st.columns([1, 2])
        with l:
            msg = st.text_area("Mesajını buraya bırak...")
            if st.button("SİSTEME GÖNDER"):
                if msg:
                    if send_data(st.session_state.user, msg):
                        st.success("İletildi!"); st.rerun()
                    else: st.error("Bağlantı hatası!")
        with r:
            st.write("### SQUAD MESSAGES")
            df = get_data()
            if not df.empty:
                for i, row in df.iterrows():
                    st.markdown(f'<div class="chat-card"><b style="color:#00ff00;">@{row["user"]}</b><br>{row["message"]} <br><small style="color:#666;">{row["timestamp"]}</small></div>', unsafe_allow_html=True)
