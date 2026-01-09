import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Indian Budget Explorer",
    page_icon="🇮🇳",
    layout="wide"
)

# ----------------------------------
# ENHANCED INDIAN FLAG THEME (UI/UX)
# ----------------------------------
st.markdown("""
<style>
    /* Background and Main Text */
    .stApp {
        background-color: #F4F7F6;
    }
    
    /* Header Colors */
    h1 { color: #FF9933 !important; font-weight: 800; }
    h2, h3 { color: #138808 !important; font-weight: 600; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 2px solid #000080; /* Ashoka Chakra Blue */
    }

    /* Metric Cards - Glassmorphism */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-top: 5px solid #FF9933;
        border-bottom: 5px solid #138808;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }
    
    .metric-title { color: #666666; font-size: 18px; margin-bottom: 10px; }
    .metric-value { color: #000080; font-size: 32px; font-weight: bold; }

    /* Fix for Visibility in Dataframes */
    .stDataFrame {
        background-color: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Budget_Finalone.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        # Creating dummy data for demonstration if file is missing
        return pd.DataFrame({
            "Year": [2023, 2024],
            "Agriculture TA": [120000, 130000],
            "Defence TA": [550000, 600000],
            "Education TA": [100000, 115000],
            "Health TA": [80000, 90000],
            "HomeAffairs TA": [190000, 200000]
        })

df = load_data()

# ----------------------------------
# SIDEBAR & VIDEO SECTION
# ----------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=100)
    st.header("⚙️ Configuration")
    
    year = st.selectbox("Select Financial Year", sorted(df["Year"].unique(), reverse=True))
    
    themes = {
        "Agriculture": {"TA": "Agriculture TA", "Subs": ["Dept. of Agriculture & Farmers’ Welfare", "Dept. of Agricultural Research & Education"]},
        "Defence": {"TA": "Defence TA", "Subs": ["Revenue", "Capital Outlay", "Pensions", "Civil"]},
        "Education": {"TA": "Education TA", "Subs": ["School Education & Literacy", "Higher Education"]},
        "Health": {"TA": "Health TA", "Subs": ["Dept. of Health & Family Welfare", "Dept. of Health Research"]},
        "Home Affairs": {"TA": "HomeAffairs TA", "Subs": ["Ministry of Home Affairs", "Police", "Cabinet"]}
    }
    
    theme_choice = st.selectbox("Select Budget Theme", list(themes.keys()))
    
    st.markdown("---")
    st.subheader("📺 Live Budget Coverage")
    # Link to Sansad TV or Budget Live Stream
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Replace with actual Budget Live Link
    st.caption("Live stream from Sansad TV / PIB")

# ----------------------------------
# MAIN CONTENT
# ----------------------------------
st.title("🇮🇳 Union Budget Analysis Portal")
st.markdown(f"### Exploring: {theme_choice} Sector | FY {year}")

ta_col = themes[theme_choice]["TA"]
sub_cols = [c for c in themes[theme_choice]["Subs"] if c in df.columns]

tab1, tab2, tab3 = st.tabs(["🎯 Key Summary", "📊 Interactive Charts", "📝 Detailed Data"])

# ========== TAB 1: SUMMARY ==========
with tab1:
    total_val = df.loc[df["Year"] == year, ta_col].values[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-title">Total {theme_choice} Allocation</div>
            <div class="metric-value">₹ {total_val:,.2f} Cr</div>
        </div>""", unsafe_allow_html=True)
        
    with col2:
        # Simple growth calculation
        prev_year_data = df[df["Year"] == (year - 1)]
        if not prev_year_data.empty:
            prev_val = prev_year_data[ta_col].values[0]
            growth = ((total_val - prev_val) / prev_val) * 100
            st.markdown(f"""<div class="metric-card">
                <div class="metric-title">Annual Growth</div>
                <div class="metric-value">{growth:+.1f}%</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-title">Annual Growth</div>
                <div class="metric-value">N/A</div>
            </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-title">Status</div>
            <div class="metric-value" style="color:#138808;">Active</div>
        </div>""", unsafe_allow_html=True)

# ========== TAB 2: VISUALS ==========
with tab2:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📈 Historical Trend")
        fig_line = px.area(df, x="Year", y=ta_col, line_shape="spline",
                           color_discrete_sequence=["#FF9933"])
        fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        st.subheader("🥧 Allocation Mix")
        if sub_cols:
            sub_vals = df[df["Year"] == year][sub_cols].T.reset_index()
            sub_vals.columns = ["Sector", "Value"]
            fig_pie = px.pie(sub_vals, values="Value", names="Sector", hole=0.5,
                             color_discrete_sequence=px.colors.sequential.Greens_r)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Sub-sector visualization not available for this theme.")

# ========== TAB 3: DATA ==========
with tab3:
    st.subheader("📄 Raw Allocation Breakdown")
    if sub_cols:
        final_table = df[df["Year"] == year][["Year", ta_col] + sub_cols]
        st.dataframe(final_table.style.format(precision=2), use_container_width=True)
    else:
        st.dataframe(df[df["Year"] == year][["Year", ta_col]], use_container_width=True)

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("---")
st.markdown("<center>Data Source: Union Budget of India | Government of India</center>", unsafe_allow_html=True)
