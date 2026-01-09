import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ----------------------------------
# 1. PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="🇮🇳 Union Budget Analysis",
    page_icon="🇮🇳",
    layout="wide"
)

# ----------------------------------
# 2. UI ENHANCEMENTS: TICKERS & BACKGROUND
# ----------------------------------
def apply_pro_terminal_ui():
    video_url = "https://assets.mixkit.co/videos/preview/mixkit-abstract-financial-data-movement-in-blue-23258-large.mp4"
    st.markdown(f"""
    <style>
    /* Cinematic Background Video */
    #myVideo {{
        position: fixed; right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -2; opacity: 0.15; filter: saturate(1.8) contrast(1.2);
    }}
    .stApp {{ background: transparent; }}

    /* High-End News Tickers */
    .ticker-common {{
        position: fixed; left: 0; width: 100%; height: 45px; 
        line-height: 45px; background: rgba(0, 0, 128, 0.9);
        color: #FF9933; font-weight: bold; overflow: hidden; z-index: 1000;
        font-family: 'Courier New', Courier, monospace; font-size: 1.1rem;
    }}
    .top-ticker {{ top: 0; border-bottom: 2px solid #FF9933; }}
    .bottom-ticker {{ bottom: 0; border-top: 2px solid #138808; }}
    .moving-text {{
        display: inline-block; white-space: nowrap; padding-left: 100%;
        animation: scroll-h 50s linear infinite;
    }}
    @keyframes scroll-h {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-180%); }} }}

    /* Main Page Styling */
    .main-content {{ padding: 80px 40px; }}
    
    .hero-title {{
        text-align: center; color: #FF9933; font-size: 4rem; font-weight: 900;
        text-shadow: 4px 4px 10px rgba(0,0,0,0.8); margin-bottom: 10px;
        letter-spacing: 5px; animation: fadeIn 2s;
    }}
    
    .metric-card {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5); 
        text-align: center; transition: 0.3s;
    }}
    .metric-card:hover {{ transform: scale(1.03); background: rgba(255, 255, 255, 0.2); }}
    
    .metric-val {{ color: white !important; font-size: 2.8rem; font-weight: 900; text-shadow: 2px 2px 4px #000; }}
    .metric-lbl {{ color: #FF9933 !important; font-size: 1.2rem; font-weight: bold; text-transform: uppercase; }}

    h1, h2, h3 {{ color: white !important; text-shadow: 2px 2px 4px #000; }}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    </style>

    <video autoplay muted loop id="myVideo"><source src="{video_url}" type="video/mp4"></video>

    <div class="ticker-common top-ticker">
        <div class="moving-text">
            🚀 UNION BUDGET ANALYSIS 2026 • FISCAL DEFICIT TARGET: 4.5% • NEW INFRASTRUCTURE ALLOCATION: ₹11.11 LAKH CR • DEFENCE OUTLAY RECORD HIGH • RURAL DEVELOPMENT BOOSTED 🚀
        </div>
    </div>

    <div class="ticker-common bottom-ticker">
        <div class="moving-text" style="animation-duration: 60s; color: #138808;">
            📈 SENSEX UP 800 POINTS • GST COLLECTIONS HIT ₹1.8 LAKH CR • TAX SLABS REVISED • DIGITAL INDIA MISSION PHASE 3 • GREEN ENERGY SUBSIDY INCREASED 📈
        </div>
    </div>
    """, unsafe_allow_html=True)

apply_pro_terminal_ui()

# ----------------------------------
# 3. DATA ENGINE
# ----------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Budget_Finalone.xlsx")
        df.columns = df.columns.str.strip()
        df = df.replace('-', 0)
        return df
    except:
        st.error("Budget_Finalone.xlsx not found.")
        st.stop()

df = load_data()

# Ministry Themes
themes = {
    "Home Affairs": {"TA": "HomeAffairs TA", "Subs": ["Police", "Ladakh", "Transfers to Jammu & Kashmir", "Chandigarh", "Lakshadweep", "Andaman & Nicobar Islands"]},
    "Defence": {"TA": "Defence TA", "Subs": ["Revenue", "Capital Outlay ", "Pensions", "Civil"]},
    "Agriculture": {"TA": "Agriculture TA", "Subs": ["Dept. of Agriculture & Farmers’ Welfare", "Dept. of Agricultural Research & Education"]},
    "Health": {"TA": "Health TA", "Subs": ["Dept. of Health & Family Welfare", "Dept. of Health Research"]},
    "Education": {"TA": "Education TA", "Subs": ["School Education & Literacy", "Higher Education"]}
}

# ----------------------------------
# 4. SIDEBAR (LIVE STREAM)
# ----------------------------------
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=120)

st.sidebar.header("📺 Live Budget Stream")
st.sidebar.video("https://www.youtube.com/watch?v=u_EKL_CfY5k") # Sansad TV

st.sidebar.title("🎛️ Terminal Settings")
selected_year = st.sidebar.selectbox("Fiscal Year", sorted(df["Year"].unique(), reverse=True))
selected_theme = st.sidebar.selectbox("Ministry Select", list(themes.keys()))

ta_col = themes[selected_theme]["TA"]
sub_cols = [c for c in themes[selected_theme]["Subs"] if c in df.columns]

# ----------------------------------
# 5. MAIN CONTENT (6 GRAPHS)
# ----------------------------------
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.markdown(f'<div class="hero-title">UNION BUDGET ANALYSIS</div>', unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center; margin-bottom:50px;'>Exploring the {selected_theme.upper()} Framework (FY {selected_year})</h3>", unsafe_allow_html=True)

# KPI Row
current_val = df.loc[df["Year"] == selected_year, ta_col].values[0]
prev_year_rows = df.loc[df["Year"] == (selected_year - 1), ta_col]
growth = ((current_val - prev_year_rows.values[0]) / prev_year_rows.values[0] * 100) if not prev_year_rows.empty else 0

k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Total Allocation</div><div class='metric-val'>₹{current_val:,.0f}Cr</div></div>", unsafe_allow_html=True)
with k2:
    g_color = "#2ECC71" if growth >= 0 else "#E74C3C"
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>YoY Growth</div><div class='metric-val' style='color:{g_color}!important;'>{growth:+.2f}%</div></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Fiscal Status</div><div class='metric-val' style='color:#3498DB!important;'>VERIFIED</div></div>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Graph Row 1
r1c1, r1c2 = st.columns(2)
with r1c1:
    st.subheader("📈 Historical Funding Volume")
    fig1 = px.area(df, x="Year", y=ta_col, line_shape="spline", color_discrete_sequence=['#FF9933'])
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig1, use_container_width=True)

with r1c2:
    st.subheader("🍩 Sub-Sector Mix (Donut)")
    if sub_cols:
        sub_vals = df[df["Year"] == selected_year][sub_cols].T.reset_index()
        sub_vals.columns = ["Dept", "Val"]
        fig2 = px.pie(sub_vals, names="Dept", values="Val", hole=0.6, color_discrete_sequence=px.colors.sequential.Greens_r)
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

# Graph Row 2
r2c1, r2c2 = st.columns(2)
with r2c1:
    st.subheader("📉 Sub-Sector Trajectory (Line)")
    
    if sub_cols:
        fig3 = px.line(df, x="Year", y=sub_cols, markers=True)
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig3, use_container_width=True)

with r2c2:
    st.subheader("📊 Annual Performance Delta")
    df_growth = df.copy().sort_values("Year")
    df_growth['Rate'] = df_growth[ta_col].pct_change() * 100
    fig4 = px.bar(df_growth, x="Year", y="Rate", color="Rate", color_continuous_scale='YlOrBr')
    fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig4, use_container_width=True)

# Graph Row 3
r3c1, r3c2 = st.columns(2)
with r3c1:
    st.subheader("🌊 Cumulative Spending Footprint")
    fig5 = go.Figure(go.Scatter(x=df["Year"], y=df[ta_col].cumsum(), fill='tozeroy', line_color='#000080'))
    fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig5, use_container_width=True)

with r3c2:
    st.subheader("🌡️ Allocation Intensity (Heatmap)")
    
    fig6 = px.imshow(df[sub_cols].T, text_auto=True, aspect="auto", color_continuous_scale='Greens')
    fig6.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig6, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
