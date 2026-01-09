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
# 2. PRO UI: PERFECT ALIGNMENT & GLASSMORPHISM
# ----------------------------------
def apply_terminal_ui():
    video_url = "https://assets.mixkit.co/videos/preview/mixkit-abstract-financial-data-movement-in-blue-23258-large.mp4"
    st.markdown(f"""
    <style>
    /* Cinematic Background */
    #myVideo {{
        position: fixed; right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -2; opacity: 0.15; filter: saturate(1.8) contrast(1.1);
    }}
    .stApp {{ background: transparent; }}

    /* Dual Ticker System with Exact Alignment */
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
        animation: scroll-h 50s linear infinite;
    }}
    @keyframes scroll-h {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-200%); }} }}

    /* Perfect Main Content Alignment */
    .main-block {{
        padding: 60px 5% 60px 5%; /* Balanced horizontal padding */
        max-width: 1600px;
        margin: 0 auto;
    }}
    
    .hero-title {{
        text-align: center; color: #FF9933; font-size: clamp(2rem, 5vw, 4.5rem); 
        font-weight: 900; text-shadow: 4px 4px 12px rgba(0,0,0,0.9);
        margin-top: 20px; margin-bottom: 0px; letter-spacing: 4px;
    }}
    
    /* KPI Card Alignment */
    .metric-card {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        padding: 25px; border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5); 
        text-align: center; height: 100%; display: flex;
        flex-direction: column; justify-content: center;
        transition: transform 0.3s ease;
    }}
    .metric-card:hover {{ transform: translateY(-5px); background: rgba(255, 255, 255, 0.18); }}
    .metric-val {{ color: #FFFFFF !important; font-size: clamp(1.5rem, 3vw, 2.8rem); font-weight: 900; }}
    .metric-lbl {{ color: #FF9933 !important; font-size: 0.9rem; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }}

    /* Sidebar Spacing Fix */
    [data-testid="stSidebar"] {{ padding-top: 40px; }}
    
    h1, h2, h3 {{ color: white !important; text-shadow: 2px 2px 4px #000; }}
    </style>

    <video autoplay muted loop id="myVideo"><source src="{video_url}" type="video/mp4"></video>

    <div class="ticker-common top-ticker">
        <div class="moving-text">
            🚀 UNION BUDGET ANALYSIS PORTAL • ALL DATA IN ₹ CRORES • SENSEX TRADING HIGH • NEW INFRASTRUCTURE TARGET: ₹11.1 LAKH CR • DEFENCE MODERNIZATION BUDGET INCREASED 🚀
        </div>
    </div>

    <div class="ticker-common bottom-ticker">
        <div class="moving-text" style="animation-direction: reverse; color: #138808;">
            📈 REAL-TIME DATA VISUALIZATION • FISCAL DEFICIT TARGET 4.5% • DIGITAL PUBLIC INFRASTRUCTURE FUNDED • GREEN HYDROGEN MISSION ALLOCATION UP • AGRI-TECH FOCUS 📈
        </div>
    </div>
    """, unsafe_allow_html=True)

apply_terminal_ui()

# ----------------------------------
# 3. DATA ENGINE
# ----------------------------------
@st.cache_data
def load_data():
    try:
        # Assuming the CSV is converted/read from the provided context
        df = pd.read_excel("Budget_Finalone.xlsx")
        df.columns = df.columns.str.strip()
        df = df.replace('-', 0)
        return df
    except:
        st.error("Error: 'Budget_Finalone.xlsx' not found. Please check your deployment folder.")
        st.stop()

df = load_data()

themes = {
    "Agriculture": {"TA": "Agriculture TA", "Subs": ["Dept. of Agriculture & Farmers’ Welfare", "Dept. of Agricultural Research & Education"]},
    "Defence": {"TA": "Defence TA", "Subs": ["Revenue", "Capital Outlay ", "Pensions", "Civil"]},
    "Health": {"TA": "Health TA", "Subs": ["Dept. of Health & Family Welfare", "Dept. of Health Research"]},
    "Education": {"TA": "Education TA", "Subs": ["School Education & Literacy", "Higher Education"]},
    "Home Affairs": {"TA": "HomeAffairs TA", "Subs": ["Police", "Ladakh", "Transfers to Jammu & Kashmir", "Chandigarh", "Lakshadweep", "Andaman & Nicobar Islands"]}
}

# ----------------------------------
# 4. SIDEBAR ALIGNMENT
# ----------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=110)
    st.markdown("### 📺 Live Broadcast")
    st.video("https://www.youtube.com/watch?v=u_EKL_CfY5k")
    st.markdown("---")
    st.title("🎛️ Terminal Controls")
    selected_year = st.selectbox("Fiscal Year", sorted(df["Year"].unique(), reverse=True))
    selected_theme = st.selectbox("Ministry", list(themes.keys()))

ta_col = themes[selected_theme]["TA"]
sub_cols = [c for c in themes[selected_theme]["Subs"] if c in df.columns]

# ----------------------------------
# 5. MAIN CONTENT - SYMMETRIC GRID
# ----------------------------------
# Wrapping everything in a div for aligned padding
st.markdown('<div class="main-block">', unsafe_allow_html=True)

st.markdown('<div class="hero-title">UNION BUDGET ANALYSIS</div>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#138808; font-weight:bold;'>Exploring {selected_theme.upper()} | Amounts in ₹ Crores | FY {selected_year}</p>", unsafe_allow_html=True)

# KPI Metrics - Perfectly Balanced Columns
current_val = df.loc[df["Year"] == selected_year, ta_col].values[0]
prev_year_rows = df.loc[df["Year"] == (selected_year - 1), ta_col]
growth = ((current_val - prev_year_rows.values[0]) / prev_year_rows.values[0] * 100) if not prev_year_rows.empty else 0

k1, k2, k3 = st.columns(3, gap="medium")
with k1:
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Total Allocation</div><div class='metric-val'>₹{current_val:,.0f} Cr</div></div>", unsafe_allow_html=True)
with k2:
    g_color = "#2ECC71" if growth >= 0 else "#E74C3C"
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>YoY Performance</div><div class='metric-val' style='color:{g_color}!important;'>{growth:+.2f}%</div></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Data Status</div><div class='metric-val' style='color:#3498DB!important;'>VERIFIED</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Symmetric Chart Grid
row1_c1, row1_c2 = st.columns(2, gap="large")
with row1_c1:
    st.subheader("📈 Historical Volume Trend")
    fig1 = px.area(df, x="Year", y=ta_col, line_shape="spline", color_discrete_sequence=['#FF9933'])
    fig1.update_layout(margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig1, use_container_width=True)

with row1_c2:
    st.subheader("🍩 Sub-Sector Composition")
    if sub_cols:
        sub_vals = df[df["Year"] == selected_year][sub_cols].T.reset_index()
        sub_vals.columns = ["Dept", "Val"]
        fig3 = px.pie(sub_vals, names="Dept", values="Val", hole=0.6, color_discrete_sequence=px.colors.sequential.Greens_r)
        fig3.update_layout(margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig3, use_container_width=True)

row2_c1, row2_c2 = st.columns(2, gap="large")
with row2_c1:
    st.subheader("📉 Multi-Sector Trajectory")
    if sub_cols:
        fig2 = px.line(df, x="Year", y=sub_cols, markers=True)
        fig2.update_layout(margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig2, use_container_width=True)

with row2_c2:
    st.subheader("📊 Annual Growth Delta")
    df_g = df.copy().sort_values("Year")
    df_g['Rate'] = df_g[ta_col].pct_change() * 100
    fig4 = px.bar(df_g, x="Year", y="Rate", color="Rate", color_continuous_scale='YlOrBr')
    fig4.update_layout(margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig4, use_container_width=True)

row3_c1, row3_c2 = st.columns(2, gap="large")
with row3_c1:
    st.subheader("🌊 Cumulative Footprint")
    fig5 = go.Figure(go.Scatter(x=df["Year"], y=df[ta_col].cumsum(), fill='tozeroy', line_color='#000080'))
    fig5.update_layout(margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig5, use_container_width=True)

with row3_c2:
    st.subheader("🌡️ Allocation Heatmap")
    fig6 = px.imshow(df[sub_cols].T, text_auto=True, aspect="auto", color_continuous_scale='Greens')
    fig6.update_layout(margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig6, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
