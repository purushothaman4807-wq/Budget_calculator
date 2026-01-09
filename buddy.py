import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Indian Budget Calculator",
    layout="wide"
)

# ----------------------------------
# INDIAN FLAG THEME
# ----------------------------------
st.markdown("""
<style>
h1 { color:#FF9933; }
h2, h3 { color:#138808; }
.metric {
    padding:20px;
    border-left:6px solid #FF9933;
    background:#FFFFFF;
    border-radius:10px;
    box-shadow:0 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# LOAD DATA (SAFE)
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Budget_Finalone.xlsx")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ----------------------------------
# TITLE
# ----------------------------------
st.title("🇮🇳 Indian Budget Calculator")
st.caption("Advanced Year-wise & Theme-wise Budget Analysis")

# ----------------------------------
# THEME CONFIG
# ----------------------------------
themes = {
    "Agriculture": {
        "TA": "Agriculture TA",
        "Subs": [
            "Dept. of Agriculture & Farmers’ Welfare",
            "Dept. of Agricultural Research & Education"
        ]
    },
    "Defence": {
        "TA": "Defence TA",
        "Subs": ["Revenue", "Capital Outlay", "Pensions", "Civil"]
    },
    "Education": {
        "TA": "Education TA",
        "Subs": ["School Education & Literacy", "Higher Education"]
    },
    "Health": {
        "TA": "Health TA",
        "Subs": [
            "Dept. of Health & Family Welfare",
            "Dept. of Health Research"
        ]
    },
    "Home Affairs": {
        "TA": "HomeAffairs TA",
        "Subs": [
            "Ministry of Home Affairs", "Police", "Cabinet",
            "Andaman & Nicobar Islands", "Chandigarh",
            "Dadra & Nagar Haveli & Daman & Diu",
            "Ladakh", "Lakshadweep",
            "Transfers to Delhi",
            "Transfers to Jammu & Kashmir",
            "Transfers to Puducherry"
        ]
    }
}

# ----------------------------------
# SIDEBAR INPUTS
# ----------------------------------
st.sidebar.header("🔢 Select Inputs")

year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
theme = st.sidebar.selectbox("Select Theme", list(themes.keys()))

ta_col = themes[theme]["TA"]
sub_cols = [c for c in themes[theme]["Subs"] if c in df.columns]

# ----------------------------------
# TABS
# ----------------------------------
tab1, tab2, tab3 = st.tabs(["🧮 Calculator", "📊 Visual Analysis", "🧠 Insights"])

# ========== TAB 1: CALCULATOR ==========
with tab1:
    st.subheader("💰 Budget Calculator")

    total_val = df.loc[df["Year"] == year, ta_col].values[0]

    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='metric'><h3>{theme} Allocation ({year})</h3><h2>₹ {total_val:,.0f} Cr</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric'><h3>Number of Sub-Sections</h3><h2>{len(sub_cols)}</h2></div>", unsafe_allow_html=True)

    st.subheader("📁 Sub-Section Breakdown")

    if sub_cols:
        sub_df = df[df["Year"] == year][sub_cols].T.reset_index()
        sub_df.columns = ["Sub-Section", "Allocation (₹ Cr)"]
        st.dataframe(sub_df, use_container_width=True)
    else:
        st.warning("No sub-section data available.")

# ========== TAB 2: VISUAL ANALYSIS ==========
with tab2:
    st.subheader("📈 Year-wise Trend")

    fig_line = px.line(
        df,
        x="Year",
        y=ta_col,
        markers=True,
        color_discrete_sequence=["#138808"]
    )
    fig_line.update_layout(height=450)
    st.plotly_chart(fig_line, use_container_width=True)

    if sub_cols:
        st.subheader("📊 Sub-Section Distribution")

        fig_bar = px.bar(
            sub_df,
            x="Sub-Section",
            y="Allocation (₹ Cr)",
            color="Sub-Section"
        )
        fig_bar.update_layout(height=450)
        st.plotly_chart(fig_bar, use_container_width=True)

        fig_donut = px.pie(
            sub_df,
            names="Sub-Section",
            values="Allocation (₹ Cr)",
            hole=0.45
        )
        fig_donut.update_layout(height=450)
        st.plotly_chart(fig_donut, use_container_width=True)

# ========== TAB 3: INSIGHTS ==========
with tab3:
    st.subheader("🧠 Auto Insights")

    if sub_cols:
        max_row = sub_df.loc[sub_df["Allocation (₹ Cr)"].idxmax()]
        min_row = sub_df.loc[sub_df["Allocation (₹ Cr)"].idxmin()]

        st.success(
            f"In {year}, **{max_row['Sub-Section']}** received the highest allocation "
            f"(₹ {max_row['Allocation (₹ Cr)']:,.0f} Cr), while "
            f"**{min_row['Sub-Section']}** received the lowest."
        )

    st.info(
        f"The **{theme}** budget in {year} reflects the government's priority "
        f"in this sector compared to previous years."
    )

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("---")
st.caption("Advanced Indian Budget Calculator | Python & Streamlit 🇮🇳")
