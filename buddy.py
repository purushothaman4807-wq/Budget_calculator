import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------
# 1. PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="🇮🇳 Union Budget Analysis",
    page_icon="🇮🇳",
    layout="wide"
)

# ----------------------------------
# 2. PRO UI: DUAL TICKERS, VIDEO & GLASSMORPHISM
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

    /* Dual Ticker System */
    .ticker-common {{
        position: fixed; left: 0; width: 100%; height: 45px; 
        line-height: 45px; background: rgba(0, 0, 128, 0.9);
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

    /* Layout & Headings */
    .main-content {{ padding: 80px 40px; }}
    .hero-title {{
        text-align: center; color: #FF9933; font-size: 4.5rem; font-weight: 900;
        text-shadow: 4px 4px 12px rgba(0,0,0,0.9); margin-bottom: 5px;
        letter-spacing: 4px; animation: fadeIn 2s;
    }}
    
    /* Enhanced Glassmorphism KPI */
    .metric-card {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5); 
        text-align: center; transition: 0.3s transform ease;
    }}
    .metric-card:hover {{ transform: scale(1.05); background: rgba(255, 255, 255, 0.18); }}
    .metric-val {{ color: #FFFFFF !important; font-size: 2.8rem; font-weight: 900; text-shadow: 2px 2px 4px #000; }}
    .metric-lbl {{ color: #FF9933 !important; font-size: 1.1rem; font-weight: bold; text-transform: uppercase; }}

    h1, h2, h3 {{ color: white !important; text-shadow: 2px 2px 4px #000; }}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
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
        df = pd.read_excel("Budget_Finalone.xlsx")
        df.columns = df.columns.str.strip()
        df = df.replace('-', 0)
        return df
    except:
        st.error("Error: 'Budget_Finalone.xlsx' not found in current directory.")
        st.stop()

df = load_data()

# Ministry Mapping
themes = {
    "Agriculture": {"TA": "Agriculture TA", "Subs": ["Dept. of Agriculture & Farmers’ Welfare", "Dept. of Agricultural Research & Education"]},
    "Defence": {"TA": "Defence TA", "Subs": ["Revenue", "Capital Outlay", "Pensions", "Civil"]},
    "Health": {"TA": "Health TA", "Subs": ["Dept. of Health & Family Welfare", "Dept. of Health Research"]},
    "Education": {"TA": "Education TA", "Subs": ["School Education & Literacy", "Higher Education"]},
    "Home Affairs": {"TA": "HomeAffairs TA", "Subs": ["Police", "Ladakh", "Transfers to Jammu & Kashmir", "Chandigarh", "Lakshadweep", "Andaman & Nicobar Islands"]}
}

# ----------------------------------
# 4. SIDEBAR (LIVE STREAM & CONTROLS)
# ----------------------------------
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=110)

st.sidebar.header("📺 Live Coverage")
st.sidebar.video("https://www.youtube.com/watch?v=u_EKL_CfY5k") # Sansad TV

st.sidebar.title("🎛️ Terminal Settings")
selected_year = st.sidebar.selectbox("Select Fiscal Year", sorted(df["Year"].unique(), reverse=True))
selected_theme = st.sidebar.selectbox("Select Ministry", list(themes.keys()))

ta_col = themes[selected_theme]["TA"]
sub_cols = [c for c in themes[selected_theme]["Subs"] if c in df.columns]

# ----------------------------------
# 5. MAIN CONTENT (6 GRAPHS - ALL IN CRORES)
# ----------------------------------
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.markdown('<div class="hero-title">UNION BUDGET ANALYSIS</div>', unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center; color:#138808 !important; margin-bottom:50px;'>Exploring {selected_theme.upper()} | All values in ₹ Crores (FY {selected_year})</h3>", unsafe_allow_html=True)

# KPI Metrics
current_val = df.loc[df["Year"] == selected_year, ta_col].values[0]
prev_year_rows = df.loc[df["Year"] == (selected_year - 1), ta_col]
growth = ((current_val - prev_year_rows.values[0]) / prev_year_rows.values[0] * 100) if not prev_year_rows.empty else 0

k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Total Ministry Outlay</div><div class='metric-val'>₹{current_val:,.0f} Cr</div></div>", unsafe_allow_html=True)
with k2:
    g_color = "#2ECC71" if growth >= 0 else "#E74C3C"
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Annual Growth Rate</div><div class='metric-val' style='color:{g_color}!important;'>{growth:+.2f}%</div></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Sector Priority</div><div class='metric-val' style='color:#3498DB!important;'>HIGH</div></div>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Graph Grid
g1, g2 = st.columns(2)
with g1:
    st.subheader("📈 Total Funding Trend (₹ Crores)")
    fig1 = px.area(df, x="Year", y=ta_col, line_shape="spline", color_discrete_sequence=['#FF9933'])
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", yaxis_title="Amount (₹ Cr)")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📉 Sub-Sector Trajectory (₹ Crores)")
    if sub_cols:
        fig2 = px.line(df, x="Year", y=sub_cols, markers=True)
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", yaxis_title="Amount (₹ Cr)")
        st.plotly_chart(fig2, use_container_width=True)

with g2:
    st.subheader("🍩 Current Year Mix (₹ Crores)")
    if sub_cols:
        sub_vals = df[df["Year"] == selected_year][sub_cols].T.reset_index()
        sub_vals.columns = ["Dept", "Val"]
        fig3 = px.pie(sub_vals, names="Dept", values="Val", hole=0.6, color_discrete_sequence=px.colors.sequential.Greens_r)
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📊 Performance Delta (%)")
    df_g = df.copy().sort_values("Year")
    df_g['Rate'] = df_g[ta_col].pct_change() * 100
    fig4 = px.bar(df_g, x="Year", y="Rate", color="Rate", color_continuous_scale='YlOrBr', labels={'Rate': 'Growth %'})
    fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
g3, g4 = st.columns(2)
with g3:
    st.subheader("🌊 Cumulative Spending (₹ Crores)")
    fig5 = go.Figure(go.Scatter(x=df["Year"], y=df[ta_col].cumsum(), fill='tozeroy', line_color='#000080'))
    fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", yaxis_title="Cumulative (₹ Cr)")
    st.plotly_chart(fig5, use_container_width=True)

with g4:
    st.subheader("🌡️ Structural Intensity (Heatmap)")
    fig6 = px.imshow(df[sub_cols].T, text_auto=True, aspect="auto", color_continuous_scale='Greens', labels=dict(color="₹ Cr"))
    fig6.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig6, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
