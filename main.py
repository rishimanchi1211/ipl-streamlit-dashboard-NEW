import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

st.set_page_config(
    page_title="IPL Analytics Hub",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #f4f7f9;
    }

    .glow-header-container {
        background: linear-gradient(135deg, #0A1A3C 0%, #1B3A6B 100%);
        padding: 25px 35px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        gap: 25px;
        box-shadow: 0 0 25px rgba(66, 153, 225, 0.5), inset 0 0 10px rgba(255,255,255,0.1);
        margin-bottom: 30px;
        margin-top: -20px;
        border: 1px solid #2c4a7c;
    }

    .ipl-logo-glow {
        width: 75px;
        filter: brightness(0) invert(1) drop-shadow(0 0 5px rgba(255,255,255,0.6));
    }

    .glow-text {
        color: #FFFFFF !important;
        margin: 0;
        font-size: 36px;
        font-weight: 800;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(255,255,255,0.7);
    }

    .logo-banner {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 30px;
    }

    .logo-card {
        background: white;
        border-radius: 12px;
        padding: 12px 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .logo-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }

    .logo-card img {
        height: 55px;
        object-fit: contain;
    }

    div[data-testid="metric-container"], [data-testid="stPlotlyChart"], .stDataFrame {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; background-color: #fff; border: 1px solid #e2e8f0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #ebf8ff; border-color: #3b82f6; color: #1e40af; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

def get_image_base64(path_or_url):
    if not path_or_url:
        return ""
    if path_or_url.startswith("http"):
        return path_or_url
    if os.path.isfile(path_or_url):
        with open(path_or_url, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            ext = path_or_url.split('.')[-1].lower()
            mime_type = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
            return f"data:{mime_type};base64,{encoded}"
    return "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="

TEAM_LOGOS = {
    "Chennai Super Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Chennai_Super_Kings_Logo.svg/200px-Chennai_Super_Kings_Logo.svg.png",
    "Mumbai Indians": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Mumbai_Indians_Logo.svg/200px-Mumbai_Indians_Logo.svg.png",
    "Royal Challengers Bangalore": "image_e791fc.jpg.png",
    "Royal Challengers Bengaluru": "image_e791fc.jpg.png",
    "Kolkata Knight Riders": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/200px-Kolkata_Knight_Riders_Logo.svg.png",
    "Sunrisers Hyderabad": "image_e79254.png",
    "Rajasthan Royals": "image_e7953e.png",
    "Delhi Capitals": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Delhi_Capitals.svg/200px-Delhi_Capitals.svg.png",
    "Delhi Daredevils": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Delhi_Capitals.svg/200px-Delhi_Capitals.svg.png",
    "Punjab Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/200px-Punjab_Kings_Logo.svg.png",
    "Kings XI Punjab": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/200px-Punjab_Kings_Logo.svg.png",
    "Gujarat Titans": "https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Gujarat_Titans_Logo.svg/200px-Gujarat_Titans_Logo.svg.png",
    "Lucknow Super Giants": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/Lucknow_Super_Giants_IPL_Logo.svg/200px-Lucknow_Super_Giants_IPL_Logo.svg.png"
}

@st.cache_data
def load_data():
    df = pd.read_csv("Match_Info.csv")
    df['match_date'] = pd.to_datetime(df['match_date'], errors='coerce')
    df['year'] = df['match_date'].dt.year
    df['team1'] = df['team1'].str.strip()
    df['team2'] = df['team2'].str.strip()
    df['winner'] = df['winner'].str.strip()
    df = df[df['result'] == 'Win'].copy()
    return df

df = load_data()

st.markdown('''
    <div class="glow-header-container">
        <img src="https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Indian_Premier_League_Official_Logo.svg/200px-Indian_Premier_League_Official_Logo.svg.png" class="ipl-logo-glow" alt="IPL Logo">
        <h1 class="glow-text">IPL Analytics Hub</h1>
    </div>
''', unsafe_allow_html=True)

active_teams = [
    "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Sunrisers Hyderabad", "Rajasthan Royals",
    "Delhi Capitals", "Punjab Kings", "Gujarat Titans", "Lucknow Super Giants"
]

banner_html = '<div class="logo-
