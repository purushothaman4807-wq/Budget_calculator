import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------
# 1. PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Union Budget Analysis",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------
# 2. TERMINAL UI + ALIGNMENT FIX
# ----------------------------------
def apply_terminal_ui():
    video_url = "https://assets.mixkit.co/videos/preview/mixkit-abstract-financial-data-movement-in-blue-23258-large.mp4"
    st.markdown(f"""
    <style>

    /* Background Video */
    #myVideo {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -2;
        opacity: 0.15;
    }}

    .stApp {{
        background: transparent;
        padding-top: 40px; /* ONLY ticker offset */
    }}

    /* Top & Bottom Ticker */
    .ticker-common {{
        position: fixed;
        left: 0;
        width: 100%;
        height: 40px;
        line-height: 40px;
        background: rgba(0,0,128,0.95);
        color: #FF9933;
        font-weight: bold;
        overflow: hidden;
        z-index: 1000;
        font-family: 'Courier New', monospace;
    }}

    .top-ticker {{
        top: 0;
        border-bottom: 2px solid #FF9933;
    }}

    .bottom-ticker {{
        bottom: 0;
        border-top: 2px solid #138808;
    }}

    .moving-text {{
        display: inline-block;
        white-space: nowrap;
        padding-left: 100%;
        animation: scroll-h 45s linear infinite;
    }}

    @keyframes scroll-h {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-200%); }}
    }}

    /* MAIN CONTENT ALIGNMENT FIX */
    .main-block {{
        padding: 20px 5% 60px 5%;  /* TOP GAP FIXED */
        max-width: 1600px;
        margin: 0 auto;
    }}

    .hero-title {{
        text-align: center;
        color: #FF9933;
        font-size: clamp(2rem, 5vw, 4.5rem);
        font-weight: 900;
        text-shadow: 4px 4px 12px rgba(0,0,0,0.9);
        margin-top: 0px;   /* FIX */
        margin-bottom: 5px;
        letter-spacing: 4px;
    }}

    /* KPI CARDS */
    .metric-card {{
        background: rgba(255,255,255,0.12);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        text-align: center;
        height: 100%;
    }}

    .metric-val {{
        color: white;
        font-size: 2.4rem;
        font-weight: 900;
    }}

    .metric-lbl {{
        color: #FF9933;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
    }}

    h1, h2, h3 {{
        color: white !important;
    }}

    </style>

    <video autoplay muted loop id="myVideo">
        <source src="{video_url}" type="video/mp4">
    </video>

    <div class="ticker-common top-ticker">
        <div class="moving-text">
        🚀 UNION BUDGET ANALYSIS • ALL VALUES IN ₹ CRORES • INFRA PUSH • DEFENCE MODERNISATION • DIGITAL INDIA 🚀
        </div>
    </div>

    <div class="ticker-common bottom-ticker">
        <div class="moving-text" style="animation-direction:reverse;color:#138808;">
        📊 REAL-TIME VISUALIZATION • FISCAL DEFICIT 4.5% • GREEN HYDROGEN • AGRI-TECH 📊
        </div>
    </div>
    """, unsafe_allow_html=True)

apply_terminal_ui()

# ----------------------------------
# 3. LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Budget_Finalone.xlsx")
    df.columns = df.columns.str.strip()
    df = df.replace('-', 0)
    return df

df = load_data()

themes = {
    "Agriculture": {
        "TA": "Agriculture TA",
        "Subs": ["Dept. of Agriculture & Farmers’ Welfare", "Dept. of Agricultural Research & Education"]
    },
    "Defence": {
        "TA": "Defence TA",
        "Subs": ["Revenue", "Capital Outlay ", "Pensions", "Civil"]
    },
    "Health": {
        "TA": "Health TA",
        "Subs": ["Dept. of Health & Family Welfare", "Dept. of Health Research"]
    },
    "Education": {
        "TA": "Education TA",
        "Subs": ["School Education & Literacy", "Higher Education"]
    },
    "Home Affairs": {
        "TA": "HomeAffairs TA",
        "Subs": ["Police", "Ladakh", "Transfers to Jammu & Kashmir",
                 "Chandigarh", "Lakshadweep", "Andaman & Nicobar Islands"]
    }
}

# ----------------------------------
# 4. SIDEBAR
# ----------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=110)
    st.title("🎛️ Terminal Controls")
    selected_year = st.selectbox("Fiscal Year", sorted(df["Year"].unique(), reverse=True))
    selected_theme = st.selectbox("Ministry", list(themes.keys()))

ta_col = themes[selected_theme]["TA"]
sub_cols = [c for c in themes[selected_theme]["Subs"] if c in df.columns]

# ----------------------------------
# 5. MAIN CONTENT
# ----------------------------------
st.markdown('<div class="main-block">', unsafe_allow_html=True)

st.markdown('<div class="hero-title">UNION BUDGET ANALYSIS</div>', unsafe_allow_html=True)
st.markdown(
    f"<p style='text-align:center;color:#138808;font-weight:bold;margin-top:0;'>"
    f"Exploring {selected_theme.upper()} | ₹ Crores | FY {selected_year}</p>",
    unsafe_allow_html=True
)

current_val = df.loc[df["Year"] == selected_year, ta_col].values[0]
prev = df.loc[df["Year"] == selected_year - 1, ta_col]
growth = ((current_val - prev.values[0]) / prev.values[0] * 100) if not prev.empty else 0

c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='metric-card'><div class='metric-lbl'>Total Allocation</div><div class='metric-val'>₹{current_val:,.0f}</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><div class='metric-lbl'>YoY Growth</div><div class='metric-val'>{growth:+.2f}%</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><div class='metric-lbl'>Status</div><div class='metric-val'>VERIFIED</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    fig1 = px.area(df, x="Year", y=ta_col)
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    if sub_cols:
        sub = df[df["Year"] == selected_year][sub_cols].T.reset_index()
        sub.columns = ["Dept", "Value"]
        fig2 = px.pie(sub, names="Dept", values="Value", hole=0.6)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
