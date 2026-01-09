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
# 2. UI: TICKERS & BACKGROUND VIDEO
# ----------------------------------
def apply_terminal_ui():
    # Cinematic financial background
    video_url = "https://assets.mixkit.co/videos/preview/mixkit-abstract-financial-data-movement-in-blue-23258-large.mp4"
    st.markdown(f"""
    <style>
    #myVideo {{
        position: fixed; right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -2; opacity: 0.12; filter: saturate(1.8);
    }}
    .stApp {{ background: transparent; }}

    /* Ticker System */
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
    @keyframes scroll-h {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-150%); }} }}

    /* Layout & Glassmorphism Metrics */
    .main-content {{ padding: 60px 40px; }}
    .metric-card {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(12px);
        padding: 25px; border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4); 
        text-align: center; color: white;
    }}
    .metric-card h2 {{ color: #FFFFFF !important; font-size: 2.3rem; font-weight: 800; text-shadow: 2px 2px 4px #000; }}
    .metric-card h3 {{ color: #FF9933 !important; font-size: 1rem; margin-bottom: 5px; text-transform: uppercase; }}
    
    h1, h2, h3 {{ color: white !important; text-shadow: 2px 2px 4px #000; }}
    
    /* Chart Container Styling */
    .chart-container {{
        background: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    </style>

    <video autoplay muted loop id="myVideo"><source src="{video_url}" type="video/mp4"></video>

    <div class="ticker-common top-ticker">
        <div class="moving-text">
            🚀 SENSEX UP 1.2% | UNION BUDGET 2026: INFRASTRUCTURE PUSH | DEFENCE EXPORTS TARGET: ₹35,000 CR | GST COLLECTIONS HIT RECORD HIGH 🚀
        </div>
    </div>

    <div class="ticker-common bottom-ticker">
        <div class="moving-text" style="animation-duration: 55s; color: #138808;">
            📈 FISCAL DEFICIT TARGET 4.5% | NEW TAX REGIME UPDATES | AI MISSIONS ALLOCATION: ₹10,000 CR | RAILWAY CAPITAL OUTLAY RECORD HIGH 📈
        </div>
    </div>
    """, unsafe_allow_html=True)

apply_terminal_ui()

# ----------------------------------
# 3. DATA LOADING
# ----------------------------------
@st.cache_data
def load_data():
    try:
        # Load from CSV if you have converted it, or Excel directly
        # For this script, we assume the Excel file is provided
        df = pd.read_excel("Budget_Finalone.xlsx")
        df.columns = df.columns.str.strip()
        # Clean numeric data (replace '-' with 0 and convert strings to float)
        df = df.replace('-', 0)
        # Ensure 'Year' is an integer
        df['Year'] = df['Year'].astype(int)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

df = load_data()

# ----------------------------------
# 4. MINISTRY THEMES (MATCHED TO DATASET)
# ----------------------------------
themes = {
    "Home Affairs": {
        "TA": "HomeAffairs TA", 
        "Subs": ["Ministry of Home Affairs", "Police", "Cabinet", "Ladakh", "Transfers to Jammu & Kashmir", "Chandigarh", "Lakshadweep", "Andaman & Nicobar Islands", "Dadra & Nagar Haveli & Daman & Diu", "Transfers to Delhi", "Transfers to Puducherry"]
    },
    "Defence": {
        "TA": "Defence TA", 
        "Subs": ["Revenue", "Capital Outlay ", "Pensions", "Civil"]
    },
    "Agriculture": {
        "TA": "Agriculture TA", 
        "Subs": ["Dept. of Agriculture & Farmers’ Welfare", "Dept. of Agricultural Research & Education"]
    },
    "Health": {
        "TA": "Health TA", 
        "Subs": ["Dept. of Health & Family Welfare", "Dept. of Health Research"]
    },
    "Education": {
        "TA": "Education TA", 
        "Subs": ["School Education & Literacy", "Higher Education"]
    }
}

# ----------------------------------
# 5. SIDEBAR CONTROLS
# ----------------------------------
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=100)

st.sidebar.subheader("📺 Live Broadcast")
st.sidebar.video("https://www.youtube.com/watch?v=u_EKL_CfY5k") # Official Sansad TV

st.sidebar.title("🎛️ Terminal Controls")
selected_year = st.sidebar.selectbox("Fiscal Year", sorted(df["Year"].unique(), reverse=True))
selected_theme = st.sidebar.selectbox("Ministry Select", list(themes.keys()))

ta_col = themes[selected_theme]["TA"]
sub_cols = [c for c in themes[selected_theme]["Subs"] if c in df.columns]

# ----------------------------------
# 6. MAIN CONTENT
# ----------------------------------
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.title(f"🇮🇳 {selected_theme.upper()} COMMAND CENTER")

# Calculations
curr_val = df.loc[df["Year"] == selected_year, ta_col].values[0]
prev_year_rows = df.loc[df["Year"] == (selected_year - 1), ta_col]
growth = ((curr_val - prev_year_rows.values[0]) / prev_year_rows.values[0] * 100) if not prev_year_rows.empty else 0

# KPI Row
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"<div class='metric-card'><h3>Ministry Outlay</h3><h2>₹ {curr_val:,.0f} Cr</h2></div>", unsafe_allow_html=True)
with k2:
    g_color = "#2ECC71" if growth >= 0 else "#E74C3C"
    st.markdown(f"<div class='metric-card'><h3>YoY Performance</h3><h2 style='color:{g_color} !important;'>{growth:+.2f}%</h2></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='metric-card'><h3>Status</h3><h2 style='color:#3498DB !important;'>VERIFIED</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------
# 7. ENHANCED VISUAL SUITE (6 GRAPHS)
# ----------------------------------

# Row 1: Area Trend & Donut Chart
r1c1, r1c2 = st.columns(2)

with r1c1:
    st.subheader("📈 Total Allocation Trend")
    fig_area = px.area(df, x="Year", y=ta_col, line_shape="spline", color_discrete_sequence=['#FF9933'])
    fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_area, use_container_width=True)

with r1c2:
    st.subheader("🍩 Sub-Sector Composition (Donut)")
    if sub_cols:
        sub_vals = df[df["Year"] == selected_year][sub_cols].T.reset_index()
        sub_vals.columns = ["Department", "Allocation"]
        sub_vals["Allocation"] = pd.to_numeric(sub_vals["Allocation"], errors='coerce').fillna(0)
        fig_donut = px.pie(sub_vals, names="Department", values="Allocation", hole=0.5, color_discrete_sequence=px.colors.sequential.Greens_r)
        fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

# Row 2: Multi-line Sub-sector Trend & Treemap
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.subheader("📉 Sub-Sector Historical Trends (Line)")
    if sub_cols:
        fig_line = px.line(df, x="Year", y=sub_cols, markers=True)
        fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", legend_title="Sub-Sectors")
        st.plotly_chart(fig_line, use_container_width=True)

with r2c2:
    st.subheader("🗺️ Allocation Hierarchy (Treemap)")
    if sub_cols:
        fig_tree = px.treemap(sub_vals, path=['Department'], values='Allocation', color='Allocation', color_continuous_scale='YlOrBr')
        fig_tree.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_tree, use_container_width=True)

# Row 3: Stacked Bar & Growth Comparison
r3c1, r3c2 = st.columns(2)

with r3c1:
    st.subheader("📊 Stacked Expenditure Growth")
    if sub_cols:
        # Melt data for stacked bar
        df_melt = df.melt(id_vars=["Year"], value_vars=sub_cols, var_name="Sub-Sector", value_name="Budget")
        df_melt["Budget"] = pd.to_numeric(df_melt["Budget"], errors='coerce').fillna(0)
        fig_stack = px.bar(df_melt, x="Year", y="Budget", color="Sub-Sector", barmode="stack")
        fig_stack.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_stack, use_container_width=True)

with r3c2:
    st.subheader("🚀 Annual Growth Rate (%)")
    df_growth = df.copy().sort_values("Year")
    df_growth['Rate'] = df_growth[ta_col].pct_change() * 100
    fig_growth = px.bar(df_growth, x="Year", y="Rate", color="Rate", color_continuous_scale='RdYlGn')
    fig_growth.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_growth, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
