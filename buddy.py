import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------
# 1. PAGE CONFIG & BACKGROUND VIDEO
# ----------------------------------
st.set_page_config(page_title="🇮🇳 Indian Budget Analytics", layout="wide")

def add_bg_video():
    # Using a professional cinematic background (replace with your own MP4 link if needed)
    video_url = "https://assets.mixkit.co/videos/preview/mixkit-abstract-financial-data-movement-in-blue-23258-large.mp4"
    st.markdown(f"""
    <style>
    #myVideo {{
        position: fixed; right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1; opacity: 0.12; filter: saturate(1.5);
    }}
    .stApp {{ background: transparent; }}
    /* Indian Flag Themed Headers */
    h1 {{ color: #FF9933 !important; text-shadow: 1px 1px 2px #000; font-weight: 800; }}
    h2, h3 {{ color: #138808 !important; font-weight: 700; }}
    .metric-container {{
        background: rgba(255, 255, 255, 0.85);
        padding: 20px; border-radius: 15px;
        border-top: 5px solid #FF9933; border-bottom: 5px solid #138808;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    </style>
    <video autoplay muted loop id="myVideo"><source src="{video_url}" type="video/mp4"></video>
    """, unsafe_allow_html=True)

add_bg_video()

# ----------------------------------
# 2. DATA LOADING & THEME MAPPING
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Budget_Finalone.xlsx")
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Please ensure 'Budget_Finalone.xlsx' is in the folder. Error: {e}")
    st.stop()

# Configuration based on your previous input
themes = {
    "Agriculture": {"TA": "Agriculture TA", "Subs": ["Dept. of Agriculture & Farmers’ Welfare", "Dept. of Agricultural Research & Education"]},
    "Defence": {"TA": "Defence TA", "Subs": ["Revenue", "Capital Outlay", "Pensions", "Civil"]},
    "Education": {"TA": "Education TA", "Subs": ["School Education & Literacy", "Higher Education"]},
    "Health": {"TA": "Health TA", "Subs": ["Dept. of Health & Family Welfare", "Dept. of Health Research"]},
    "Home Affairs": {"TA": "HomeAffairs TA", "Subs": ["Ministry of Home Affairs", "Police", "Cabinet", "Ladakh", "Transfers to Jammu & Kashmir"]}
}

# ----------------------------------
# 3. SIDEBAR CONTROLS
# ----------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=100)
st.sidebar.title("Budget Controls")
selected_year = st.sidebar.selectbox("Select Financial Year", sorted(df["Year"].unique(), reverse=True))
selected_theme = st.sidebar.selectbox("Select Theme", list(themes.keys()))

ta_col = themes[selected_theme]["TA"]
sub_cols = [c for c in themes[selected_theme]["Subs"] if c in df.columns]

# ----------------------------------
# 4. DASHBOARD HEADER & KPI
# ----------------------------------
st.title(f"🇮🇳 {selected_theme} Budget Analysis")

# Calculations
current_val = df.loc[df["Year"] == selected_year, ta_col].values[0]
prev_year_data = df.loc[df["Year"] == (selected_year - 1), ta_col]
growth = ((current_val - prev_year_data.values[0]) / prev_year_data.values[0] * 100) if not prev_year_data.empty else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-container'><h3>Total Allocation</h3><h2>₹ {current_val:,.0f} Cr</h2></div>", unsafe_allow_html=True)
with col2:
    color = "green" if growth >= 0 else "red"
    st.markdown(f"<div class='metric-container'><h3>YoY Growth</h3><h2 style='color:{color}'>{growth:+.2f}%</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-container'><h3>Sub-Departments</h3><h2>{len(sub_cols)} Units</h2></div>", unsafe_allow_html=True)

# ----------------------------------
# 5. THE 5-GRAPH SUITE
# ----------------------------------
st.markdown("---")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    # CHART 1: Area Trend (Historical Context)
    st.subheader("📈 Allocation Trend (Time Series)")
    fig1 = px.area(df, x="Year", y=ta_col, line_shape="spline", color_discrete_sequence=['#FF9933'])
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with row1_col2:
    # CHART 2: Donut Chart (Sub-sector Breakdown)
    st.subheader("🥧 Sub-Sector Composition")
    if sub_cols:
        sub_vals = df[df["Year"] == selected_year][sub_cols].T.reset_index()
        sub_vals.columns = ["Department", "Value"]
        fig2 = px.pie(sub_vals, values="Value", names="Department", hole=0.5, color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No sub-section data available for this theme.")

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    # CHART 3: Bar Chart (Annual Growth Comparison)
    st.subheader("🚀 Annual Growth Rate (%)")
    df_growth = df.copy()
    df_growth['Growth'] = df_growth[ta_col].pct_change() * 100
    fig3 = px.bar(df_growth, x="Year", y="Growth", color="Growth", color_continuous_scale='RdYlGn')
    st.plotly_chart(fig3, use_container_width=True)

with row2_col2:
    # CHART 4: Waterfall Chart (Cumulative Budget Build-up)
    st.subheader("🌊 Cumulative Spending Impact")
    fig4 = go.Figure(go.Scatter(x=df["Year"], y=df[ta_col].cumsum(), fill='tozeroy', line_color='#000080'))
    fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig4, use_container_width=True)

# CHART 5: Heatmap (Sector Intensity)
st.subheader("🌡️ Budget Intensity Heatmap (All Sectors)")
heatmap_cols = ["Year"] + [themes[t]["TA"] for t in themes]
fig5 = px.imshow(df[heatmap_cols].set_index("Year").T, text_auto=True, aspect="auto", color_continuous_scale='Oranges')
st.plotly_chart(fig5, use_container_width=True)

st.caption("Data Source: Budget_Finalone.xlsx | Created for Indian Budget Analysis 🇮🇳")
