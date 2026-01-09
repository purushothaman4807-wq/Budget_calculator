import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------
# 1. PAGE CONFIG & ENHANCED THEME
# ----------------------------------
st.set_page_config(
    page_title="🇮🇳 Budget Terminal Live",
    page_icon="🇮🇳",
    layout="wide"
)

def apply_pro_ui():
    # Cinematic financial background video
    video_url = "https://assets.mixkit.co/videos/preview/mixkit-abstract-financial-data-movement-in-blue-23258-large.mp4"
    st.markdown(f"""
    <style>
    #myVideo {{
        position: fixed; right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -2; opacity: 0.15; filter: saturate(1.5);
    }}
    .stApp {{ background: transparent; }}
    
    /* GLASSMORPHISM KPI CARDS */
    .kpi-card {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 30px; border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }}
    .kpi-label {{ color: #FF9933; font-size: 1.3rem; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }}
    .kpi-value {{ color: #FFFFFF; font-size: 2.8rem; font-weight: 900; text-shadow: 2px 2px 10px rgba(0,0,0,0.5); }}
    
    /* News Tickers */
    .ticker-wrap {{
        position: fixed; left: 0; width: 100%; height: 40px; 
        background: rgba(0, 0, 128, 0.95); color: #FF9933;
        line-height: 40px; z-index: 1000; font-family: monospace;
    }}
    .top-ticker {{ top: 0; border-bottom: 2px solid #FF9933; }}
    .bottom-ticker {{ bottom: 0; border-top: 2px solid #138808; }}
    .moving-text {{ display: inline-block; white-space: nowrap; animation: scroll 40s linear infinite; }}
    @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-150%); }} }}
    
    h1, h2, h3 {{ color: #FFFFFF !important; text-shadow: 2px 2px 5px #000; }}
    </style>
    <video autoplay muted loop id="myVideo"><source src="{video_url}" type="video/mp4"></video>
    
    <div class="ticker-wrap top-ticker">
        <div class="moving-text">🚨 SANSAD TV LIVE: UNION BUDGET PRESENTATION IN PROGRESS • 📈 SENSEX TRADING AT 74,000 • 🚜 AGRI-TECH SUBSIDIES INCREASED BY 15% 🚨</div>
    </div>
    """, unsafe_allow_html=True)

apply_pro_ui()

# ----------------------------------
# 2. DATA LOADING & CONFIG
# ----------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Budget_Finalone.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except:
        st.error("Excel file not found!")
        st.stop()

df = load_data()

themes = {
    "Home Affairs": {"TA": "HomeAffairs TA", "Subs": ["Police", "Ladakh", "Transfers to Jammu & Kashmir", "Chandigarh"]},
    "Defence": {"TA": "Defence TA", "Subs": ["Revenue", "Capital Outlay", "Pensions"]},
    "Agriculture": {"TA": "Agriculture TA", "Subs": ["Dept. of Agriculture & Farmers’ Welfare", "Dept. of Agricultural Research & Education"]}
}

# ----------------------------------
# 3. SIDEBAR & LIVE VIDEO
# ----------------------------------
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=120)

st.sidebar.header("📺 Live Broadcast")
# Official Sansad TV Live Stream Link
st.sidebar.video("https://www.youtube.com/watch?v=u_EKL_CfY5k")

st.sidebar.header("🎛️ Data Controls")
selected_year = st.sidebar.selectbox("Fiscal Year", sorted(df["Year"].unique(), reverse=True))
selected_theme = st.sidebar.selectbox("Ministry", list(themes.keys()))

# ----------------------------------
# 4. MAIN DASHBOARD CONTENT
# ----------------
