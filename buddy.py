import streamlit as st
import pandas as pd

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="Indian Budget Calculator",
    layout="centered"
)

# ---------------------------------------
# LOAD DATA (SAFE)
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Budget_Finalone.xlsx")
    df.columns = df.columns.str.strip()   # removes extra spaces
    return df

df = load_data()

# ---------------------------------------
# TITLE
# ---------------------------------------
st.title("🇮🇳 Indian Budget Calculator")
st.caption("Simple year-wise and theme-wise Union Budget calculator")

# ---------------------------------------
# THEME CONFIG (SAFE & VERIFIED)
# ---------------------------------------
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
            "Ministry of Home Affairs",
            "Police",
            "Cabinet",
            "Andaman & Nicobar Islands",
            "Chandigarh",
            "Dadra & Nagar Haveli & Daman & Diu",
            "Ladakh",
            "Lakshadweep",
            "Transfers to Delhi",
            "Transfers to Jammu & Kashmir",
            "Transfers to Puducherry"
        ]
    }
}

# ---------------------------------------
# INPUTS
# ---------------------------------------
st.subheader("🔢 Select Inputs")

year = st.selectbox(
    "Select Year",
    sorted(df["Year"].unique())
)

theme = st.selectbox(
    "Select Theme",
    list(themes.keys())
)

ta_col = themes[theme]["TA"]
sub_cols = themes[theme]["Subs"]

# ---------------------------------------
# TOTAL ALLOCATION (SAFE)
# ---------------------------------------
st.subheader("💰 Budget Calculation")

try:
    total_value = df.loc[df["Year"] == year, ta_col].values[0]
    st.metric(
        label=f"{theme} Total Allocation ({year})",
        value=f"₹ {total_value:,.0f} Crore"
    )
except:
    st.error("Total allocation data not available.")

# ---------------------------------------
# SUB-SECTION ALLOCATION (SAFE)
# ---------------------------------------
st.subheader("📊 Sub-Section Allocation")

available_subs = [c for c in sub_cols if c in df.columns]

if len(available_subs) == 0:
    st.warning("No sub-section data available for this theme.")
else:
    sub_df = (
        df[df["Year"] == year][available_subs]
        .T.reset_index()
    )
    sub_df.columns = ["Sub-Section", "Allocation (₹ Crore)"]

    st.dataframe(sub_df, use_container_width=True)

# ---------------------------------------
# FOOTER
# ---------------------------------------
st.markdown("---")
st.caption("Indian Union Budget Calculator | Python & Streamlit 🇮🇳")
