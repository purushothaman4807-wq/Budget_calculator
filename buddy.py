import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(page_title="Union Budget Dashboard", layout="wide")

# ----------------------------------
# BACKGROUND VIDEO & THEME CSS
# ----------------------------------
def add_bg_video():
    # Replace the URL below with a direct MP4 link of the Indian Budget/Parliament
    # Using a placeholder cinematic Indian landscape for demonstration
    video_url = "https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4" 
    
    st.markdown(f"""
    <style>
    #myVideo {{
        position: fixed;
        right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1;
        opacity: 0.15; /* Makes text visible while video plays softly */
        filter: grayscale(50%);
    }}
    .stApp {{
        background: transparent;
    }}
    h1 {{ color: #FF9933 !important; text-shadow: 2px 2px 4px #000; }}
    h2, h3 {{ color: #138808 !important; }}
    .stMetric {{ background: rgba(255,255,255,0.8); padding: 10px; border-radius: 10px; }}
    </style>
    <video autoplay muted loop id="myVideo">
      <source src="{video_url}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

add_bg_video()

# ----------------------------------
# LOAD DATA (With dummy fallback)
# ----------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Budget_Finalone.xlsx")
    except:
        # Fallback data for preview
        data = {
            "Year": [2021, 2022, 2023, 2024, 2025],
            "Agriculture TA": [110000, 115000, 120000, 125000, 135000],
            "Defence TA": [480000, 510000, 550000, 580000, 620000],
            "Education TA": [90000, 95000, 105000, 110000, 120000],
            "Health TA": [70000, 75000, 85000, 90000, 100000]
        }
        df = pd.DataFrame(data)
    return df

df = load_data()

# ----------------------------------
# SIDEBAR
# ----------------------------------
st.sidebar.title("🇮🇳 Budget Controls")
theme = st.sidebar.selectbox("Choose Theme", ["Agriculture", "Defence", "Education", "Health"])
ta_col = f"{theme} TA"

# ----------------------------------
# MAIN DASHBOARD
# ----------------------------------
st.title(f"Detailed Analysis: {theme} Sector")

# ADVANCED CALCULATIONS
df['YoY Growth (%)'] = df[ta_col].pct_change() * 100

# ROW 1: CORE METRICS
col1, col2, col3 = st.columns(3)
latest_val = df[ta_col].iloc[-1]
prev_val = df[ta_col].iloc[-2]
growth = ((latest_val - prev_val) / prev_val) * 100

col1.metric("Current Allocation", f"₹{latest_val:,.0f} Cr", f"{growth:.1f}% YoY")
col2.metric("5-Year Average", f"₹{df[ta_col].mean():,.0f} Cr")
col3.metric("Projected Next Year", f"₹{latest_val * 1.08:,.0f} Cr", "Estimated 8%↑")

st.markdown("---")

# ROW 2: DYNAMIC GRAPHS
c1, c2 = st.columns(2)

with c1:
    # 1. THE TREND LINE (Area Chart)
    st.subheader("📈 Long-term Funding Trend")
    fig1 = px.area(df, x="Year", y=ta_col, color_discrete_sequence=['#FF9933'])
    st.plotly_chart(fig1, use_container_width=True)

    # 2. YoY GROWTH RATE (Bar Chart)
    st.subheader("🚀 Annual Growth Rate (%)")
    fig2 = px.bar(df, x="Year", y="YoY Growth (%)", color="YoY Growth (%)", 
                  color_continuous_scale='Greens')
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    # 3. DISTRIBUTION (Sunburst/Pie)
    st.subheader("🍰 Budget Proportions")
    # For demo, we split the TA into 2 segments
    df_melt = pd.DataFrame({
        "Category": ["Revenue Expenditure", "Capital Outlay"],
        "Value": [latest_val * 0.7, latest_val * 0.3]
    })
    fig3 = px.pie(df_melt, values="Value", names="Category", hole=0.4, 
                  color_discrete_sequence=['#000080', '#138808'])
    st.plotly_chart(fig3, use_container_width=True)

    # 4. CUMULATIVE ALLOCATION (Waterfall Chart)
    st.subheader("🌊 Cumulative Spending Impact")
    fig4 = px.line(df, x="Year", y=df[ta_col].cumsum(), markers=True)
    fig4.update_traces(line_color='#138808')
    st.plotly_chart(fig4, use_container_width=True)

# 5. HEATMAP (Bottom Full Width)
st.subheader("🌡️ Allocation Intensity Heatmap")
fig5 = px.density_heatmap(df, x="Year", y=ta_col, text_auto=True, color_continuous_scale='Oranges')
st.plotly_chart(fig5, use_container_width=True)
