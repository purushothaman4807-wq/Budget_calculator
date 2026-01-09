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
# 2. THE 4-WAY TICKER CSS & BACKGROUND
# ----------------------------------
def apply_terminal_ui():
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
        position: fixed; background: rgba(0, 0, 128, 0.95);
        color: #FF9933; font-weight: bold; overflow: hidden; z-index: 1000;
        font-family: 'Courier New', Courier, monospace;
    }}
    
    /* Horizontal Tickers */
    .ticker-h {{ width: 100%; height: 35px; line-height: 35px; left: 0; }}
    .top-ticker {{ top: 0; border-bottom: 2px solid #FF9933; }}
    .bottom-ticker {{ bottom: 0; border-top: 2px solid #138808; }}
    
    /* Vertical Tickers */
    .ticker-v {{ width: 40px; height: 100%; top: 0; writing-mode: vertical-rl; }}
    .left-ticker {{ left: 0; border-right: 2px solid #FF9933; }}
    .right-ticker {{ right: 0; border-left: 2px solid #138808; }}

    .moving-text {{
        display: inline-block; white-space: nowrap; padding-left: 100%;
        animation: scroll-h 40s linear infinite;
    }}
    .moving-text-v {{
        display: inline-block; white-space: nowrap; padding-top: 100%;
        animation: scroll-v 30s linear infinite;
    }}

    @keyframes scroll-h {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-100%); }} }}
    @keyframes scroll-v {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(-100%); }} }}

    /* Main Content Adjustments */
    .main-content {{ padding: 50px 60px; }}
    .metric-card {{
        background: rgba(255, 255, 255, 0.9);
        padding: 20px; border-radius: 10px;
        border-top: 4px solid #FF9933; border-bottom: 4px solid #138808;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3); text-align: center;
    }}
    </style>

    <video autoplay muted loop id="myVideo"><source src="{video_url}" type="video/mp4"></video>

    <div class="ticker-common ticker-h top-ticker">
        <div class="moving-text">
            🚀 SENSEX UP 1.2% | UNION BUDGET 2026: INFRASTRUCTURE PUSH | RENEWABLE ENERGY SUBSIDIES INCREASED | DEFENCE EXPORTS TARGET: ₹35,000 CR | GST COLLECTIONS HIT RECORD HIGH 🚀
        </div>
    </div>

    <div class="ticker-common ticker-h bottom-ticker">
        <div class="moving-text" style="animation-direction: reverse; color: #138808;">
            📈 FISCAL DEFICIT TARGET 4.5% | NEW TAX REGIME UPDATES | AI MISSIONS ALLOCATION: ₹10,000 CR | RAILWAY CAPITAL OUTLAY RECORD HIGH | AGRI-TECH STARTUPS TAX HOLIDAY 📈
        </div>
    </div>

    <div class="ticker-common ticker-v left-ticker">
        <div class="moving-text-v"> BUDGET 2026 • DIGITAL INDIA • ATMANIRBHAR BHARAT • GREEN HYDROGEN • SEMICONDUCTOR MISSION </div>
    </div>

    <div class="ticker-common ticker-v right-ticker">
        <div class="moving-text-v" style="animation-direction: reverse; color: #138808;"> FINANCIAL DATA • REAL-TIME ANALYSIS • GDP GROWTH 7.2% • RBI REPO RATE UNCHANGED </div>
    </div>
    """, unsafe_allow_html=True)

apply_terminal_ui()

# ----------------------------------
# 3. DATA LOADING & THEMES
# ----------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Budget_Finalone.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except:
        st.error("Budget_Finalone.xlsx not found.")
        st.stop()

df = load_data()

themes = {
    "Home Affairs": {"TA": "HomeAffairs TA", "Subs": ["Ministry of Home Affairs", "Police", "Cabinet", "Ladakh", "Transfers to Jammu & Kashmir", "Chandigarh", "Lakshadweep", "Andaman & Nicobar Islands"]},
    "Defence": {"TA": "Defence TA", "Subs": ["Revenue", "Capital Outlay", "Pensions", "Civil"]},
    "Agriculture": {"TA": "Agriculture TA", "Subs": ["Dept. of Agriculture & Farmers’ Welfare", "Dept. of Agricultural Research & Education"]},
    "Education": {"TA": "Education TA", "Subs": ["School Education & Literacy", "Higher Education"]},
    "Health": {"TA": "Health TA", "Subs": ["Dept. of Health & Family Welfare", "Dept. of Health Research"]}
}

# ----------------------------------
# 4. SIDEBAR & NAVIGATION
# ----------------------------------
st.sidebar.markdown("<br><br>", unsafe_allow_html=True) # Space for top ticker
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=120)
st.sidebar.header("📊 Control Panel")

selected_year = st.sidebar.selectbox("Fiscal Year", sorted(df["Year"].unique(), reverse=True))
selected_theme = st.sidebar.selectbox("Ministry Select", list(themes.keys()))

ta_col = themes[selected_theme]["TA"]
sub_cols = [c for c in themes[selected_theme]["Subs"] if c in df.columns]

# ----------------------------------
# 5. MAIN DASHBOARD
# ----------------------------------
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.title(f"🇮🇳 {selected_theme.upper()} COMMAND CENTER")

# KPI Summary
current_val = df.loc[df["Year"] == selected_year, ta_col].values[0]
prev_year_data = df.loc[df["Year"] == (selected_year - 1), ta_col]
growth = ((current_val - prev_year_data.values[0]) / prev_year_data.values[0] * 100) if not prev_year_data.empty else 0

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"<div class='metric-card'><h3>Total Outlay</h3><h2>₹ {current_val:,.0f} Cr</h2></div>", unsafe_allow_html=True)
with m2:
    g_color = "#138808" if growth >= 0 else "#FF0000"
    st.markdown(f"<div class='metric-card'><h3>YoY Performance</h3><h2 style='color:{g_color}'>{growth:+.2f}%</h2></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='metric-card'><h3>Active Divisions</h3><h2>{len(sub_cols)} Nodes</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# Visual Suite
c1, c2 = st.columns(2)
with c1:
    st.subheader("📈 Allocation Timeline")
    fig1 = px.area(df, x="Year", y=ta_col, line_shape="spline", color_discrete_sequence=['#FF9933'])
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🚀 Spending Growth Rate")
    df_g = df.copy().sort_values("Year")
    df_g['Rate'] = df_g[ta_col].pct_change() * 100
    fig2 = px.bar(df_g, x="Year", y="Rate", color="Rate", color_continuous_scale='YlOrBr')
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    st.subheader("🗺️ Budget Distribution (Treemap)")
    
    if sub_cols:
        sub_vals = df[df["Year"] == selected_year][sub_cols].T.reset_index()
        sub_vals.columns = ["Dept", "Val"]
        fig3 = px.treemap(sub_vals, path=['Dept'], values='Val', color='Val', color_continuous_scale='Greens')
        st.plotly_chart(fig3, use_container_width=True)
    
    st.subheader("🌡️ Structural Heatmap")
    
    fig4 = px.imshow(df[sub_cols].T, aspect="auto", color_continuous_scale='YlOrBr')
    st.plotly_chart(fig4, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
