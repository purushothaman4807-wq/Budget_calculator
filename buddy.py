import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# ----------------------------------
# 🎥 VIDEO BACKGROUND INJECTION
# ----------------------------------
def set_bg_video(video_file):
    with open(video_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    video_html = f'''
        <style>
        #myVideo {{
            position: fixed;
            right: 0; bottom: 0;
            min-width: 100%; min-height: 100%;
            z-index: -1;
            filter: brightness(0.4); /* Darkens video to make text pop */
        }}
        .stApp {{ background: transparent; }}
        
        /* 💎 GLASSMORPHISM KPI CARDS */
        .kpi-card {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        .kpi-label {{ color: #FF9933; font-size: 1.2rem; font-weight: bold; }}
        .kpi-value {{ color: #FFFFFF; font-size: 2.2rem; font-weight: 900; }}
        
        /* High-Visibility Headings */
        h1, h2, h3 {{ color: #FFFFFF !important; text-shadow: 2px 2px 4px #000000; }}
        </style>
        <video autoplay muted loop id="myVideo">
            <source src="data:video/mp4;base64,{b64}" type="video/mp4">
        </video>
    '''
    st.markdown(video_html, unsafe_allow_html=True)

# ----------------------------------
# APP SETUP
# ----------------------------------
st.set_page_config(page_title="🇮🇳 Budget Terminal", layout="wide")

# IMPORTANT: Replace 'budget_bg.mp4' with your actual video file name
try:
    set_bg_video("budget_bg.mp4")
except:
    st.warning("Video file not found. Place 'budget_bg.mp4' in the root folder.")

# ... (Previous Data Loading & Theme Logic here) ...

# ----------------------------------
# 📊 ENHANCED KPI DISPLAY
# ----------------------------------
st.title("🇮🇳 Indian Union Budget Explorer")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'''<div class="kpi-card">
        <div class="kpi-label">AGRICULTURE ALLOCATION</div>
        <div class="kpi-value">₹ 1,25,000 Cr</div>
    </div>''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''<div class="kpi-card">
        <div class="kpi-label">DEFENCE OUTLAY</div>
        <div class="kpi-value">₹ 6,21,540 Cr</div>
    </div>''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''<div class="kpi-card">
        <div class="kpi-label">HEALTHCARE FOCUS</div>
        <div class="kpi-value">₹ 89,287 Cr</div>
    </div>''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# (Rest of your charts and dataframes follow)
