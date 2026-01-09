import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ----------------------------------
# 1. PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="🇮🇳 Budget Terminal Pro",
    page_icon="🇮🇳",
    layout="wide"
)

# ----------------------------------
# 2. TOP & BOTTOM TICKER CSS
# ----------------------------------
def apply_dual_ticker_ui():
    video_url = "https://assets.mixkit.co/videos/preview/mixkit-abstract-financial-data-movement-in-blue-23258-large.mp4"
    st.markdown(f"""
    <style>
    /* Video Background */
    #myVideo {{
        position: fixed; right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -2; opacity: 0.10; filter: saturate(1.8);
    }}
    .stApp {{ background: transparent; }}

    /* --- TICKER SYSTEM --- */
    .ticker-common {{
        position: fixed; left: 0; width: 100%; height: 40px; 
        line-height: 40px; background: rgba(0, 0, 128, 0.95);
        color: #FF9933; font-weight: bold; overflow: hidden; z-index: 1000;
        font-family: 'Courier New', Courier, monospace;
    }}
    
    .top-ticker {{ top: 0; border-bottom: 2px solid #FF9933; }}
    .bottom-ticker {{ bottom: 0; border-top: 2px solid #138808; }}

    .moving-text {{
        display: inline-block; white-space: nowrap; padding-left: 100%;
        animation: scroll-h 45s linear infinite;
    }}

    @keyframes scroll-h {{ 
        0% {{ transform: translateX(0); }} 
        100% {{ transform: translateX(-150%); }} 
    }}

    /* Layout Spacing */
    .main-content {{ padding: 60px 40px; }}
    .metric-card {{
        background: rgba(255, 255, 255, 0.95);
        padding: 20px; border-radius: 12px;
        border-top: 5px solid #FF9933; border-bottom: 5px solid #138808;
        box-shadow: 0 5px 20px rgba(0,0,0,0.25); text-align: center;
    }}
    </style>

    <video autoplay muted loop id="myVideo"><source src="{video_url}" type="video/mp4"></video>

    <div class="ticker-common top-ticker">
        <div class="moving-text">
            🚀 SENSEX UP 1.2% | UNION BUDGET 2026: INFRASTRUCTURE PUSH | RENEWABLE ENERGY SUBSIDIES INCREASED | DEFENCE EXPORTS TARGET: ₹35,000 CR | GST COLLECTIONS HIT RECORD HIGH 🚀
        </div>
    </div>

    <div class="ticker-common bottom-ticker">
        <div class="moving-text" style="animation-duration: 55s; color: #138808;">
            📈 FISCAL DEFICIT TARGET 4.5% | NEW TAX REGIME UPDATES | AI MISSIONS ALLOCATION: ₹10,000 CR | RAILWAY CAPITAL OUTLAY RECORD HIGH | AGRI-TECH STARTUPS TAX HOLIDAY 📈
        </div>
    </div>
    """, unsafe_allow_html=True)

apply_dual_ticker_ui()

# ----------------------------------
# 3. DATA LOADING
# ----------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Budget_Finalone.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except:
        # Fallback to demo data if file missing
        data = {"Year": [2023, 2024, 2025], "HomeAffairs TA": [100, 110, 120], "Police": [40, 45, 50]}
        return pd.DataFrame(data)

df = load_data()

# ----------------------------------
# 4. MINISTRY CONFIG
# ----------------------------------
themes = {
    "Home Affairs": {"TA": "HomeAffairs TA", "Subs": ["Ministry of Home Affairs", "Police", "Cabinet", "Ladakh", "Transfers to Jammu & Kashmir", "Chandigarh", "Lakshadweep", "Andaman & Nicobar Islands"]},
    "Defence": {"TA": "Defence TA", "Subs": ["Revenue", "Capital Outlay", "Pensions", "Civil"]},
    "Agriculture": {"TA": "Agriculture TA", "Subs": ["Dept. of Agriculture & Farmers’ Welfare", "Dept. of Agricultural Research & Education"]},
    "Education": {"TA": "Education TA", "Subs": ["School Education & Literacy", "Higher Education"]}
}

# ----------------------------------
# 5. SIDEBAR CONTROLS
# ----------------------------------
st.sidebar.markdown("<br><br>", unsafe_allow_html=True) # Prevent overlap with top ticker
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=100)
st.sidebar.title("🎛️ Terminal Controls")

selected_year = st.sidebar.selectbox("Fiscal Year", sorted(df["Year"].unique(), reverse=True))
selected_theme = st.sidebar.selectbox("Ministry Select", list(themes.keys()))

ta_col = themes[selected_theme]["TA"]
sub_cols = [c for c in themes[selected_theme]["Subs"] if c in df.columns]

# ----------------------------------
# 6. DASHBOARD DISPLAY
# ----------------------------------
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.title(f"🇮🇳 {selected_theme.upper()} BUDGET OVERVIEW")

# KPI Summary
current_val = df.loc[df["Year"] == selected_year, ta_col].values[0]
prev_year_data = df.loc[df["Year"] == (selected_year - 1), ta_col]
growth = ((current_val - prev_year_data.values[0]) / prev_year_data.values[0] * 100) if not prev_year_data.empty else 0

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"<div class='metric-card'><h3>Ministry Outlay</h3><h2>₹ {current_val:,.0f} Cr</h2></div>", unsafe_allow_html=True)
with m2:
    g_color = "#138808" if growth >= 0 else "#FF0000"
    st.markdown(f"<div class='metric-card'><h3>YoY Growth</h3><h2 style='color:{g_color}'>{growth:+.2f}%</h2></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='metric-card'><h3>Status</h3><h2 style='color:#000080'>VERIFIED</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# Visual Suite
c1, c2 = st.columns(2)
with c1:
    st.subheader("📈 Allocation Timeline")
    fig1 = px.area(df, x="Year", y=ta_col, line_shape="spline", color_discrete_sequence=['#FF9933'])
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("🗺️ Budget Distribution (Treemap)")
    if sub_cols:
        sub_vals = df[df["Year"] == selected_year][sub_cols].T.reset_index()
        sub_vals.columns = ["Dept", "Val"]
        fig3 = px.treemap(sub_vals, path=['Dept'], values='Val', color='Val', color_continuous_scale='Greens')
        st.plotly_chart(fig3, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
