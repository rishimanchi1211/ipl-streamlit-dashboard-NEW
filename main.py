import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IPL Analytical Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED CSS FOR SaaS THEME ---
st.markdown("""
    <style>
    /* Import clean sans-serif font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Set app background to light grey/blue */
    .stApp {
        background-color: #f4f7f9;
    }

    /* Top Premium Gradient Header */
    .custom-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 25px 30px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        margin-top: -30px;
    }
    .custom-header h1 {
        color: white !important;
        margin: 0;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* Custom Footer */
    .custom-footer {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        font-weight: 500;
        margin-top: 40px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-size: 16px;
    }

    /* Style the Metrics (White cards with borders) */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 15px 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    div[data-testid="metric-container"] label {
        color: #64748b !important;
        font-weight: 600;
        font-size: 14px;
    }
    div[data-testid="metric-container"] div {
        color: #0f172a !important;
        font-weight: 700;
    }

    /* Style Chart Containers */
    [data-testid="stPlotlyChart"], .stDataFrame {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }

    /* Marquee styling for logos */
    .marquee-container {
        width: 100%;
        overflow: hidden;
        background: transparent;
        padding: 10px 0 20px 0;
        white-space: nowrap;
    }
    .marquee-content {
        display: inline-block;
        animation: scroll 35s linear infinite;
    }
    .marquee-content img {
        height: 65px;
        margin: 0 35px;
        vertical-align: middle;
        object-fit: contain;
    }
    @keyframes scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    </style>
""", unsafe_allow_html=True)

# --- OFFICIAL BCCI S3 LOGOS (100% RELIABLE, WILL NOT BREAK) ---
TEAM_LOGOS = {
    "Chennai Super Kings": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/CSK/Logos/Logooutline/CSK.png",
    "Mumbai Indians": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/MI/Logos/Logooutline/MI.png",
    "Royal Challengers Bangalore": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/RCB/Logos/Logooutline/RCB.png",
    "Royal Challengers Bengaluru": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/RCB/Logos/Logooutline/RCB.png",
    "Kolkata Knight Riders": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/KKR/Logos/Logooutline/KKR.png",
    "Sunrisers Hyderabad": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/SRH/Logos/Logooutline/SRH.png",
    "Rajasthan Royals": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/RR/Logos/Logooutline/RR.png",
    "Delhi Capitals": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/DC/Logos/Logooutline/DC.png",
    "Delhi Daredevils": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/DC/Logos/Logooutline/DC.png",
    "Punjab Kings": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/PBKS/Logos/Logooutline/PBKS.png",
    "Kings XI Punjab": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/PBKS/Logos/Logooutline/PBKS.png",
    "Gujarat Titans": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/GT/Logos/Logooutline/GT.png",
    "Lucknow Super Giants": "https://bcciplayerimages.s3.ap-south-1.amazonaws.com/ipl/LSG/Logos/Logooutline/LSG.png"
}

# --- LOAD DATA ---
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

# --- CUSTOM BLUE HEADER ---
st.markdown("""
<div class="custom-header">
    <img src="https://upload.wikimedia.org/wikipedia/en/8/84/Indian_Premier_League_Official_Logo.svg" width="60" style="background: white; border-radius: 8px; padding: 5px;">
    <h1>IPL Analytical Dashboard</h1>
</div>
""", unsafe_allow_html=True)

# --- SCROLLING LOGO BANNER (DEDUPLICATED) ---
# This guarantees each visual logo is only added to the banner once!
seen_urls = set()
unique_logos = []
for team, url in TEAM_LOGOS.items():
    if url not in seen_urls:
        seen_urls.add(url)
        unique_logos.append((team, url))

logos_html = "".join([f"<img src='{url}' title='{team}'>" for team, url in unique_logos])
marquee_html = f"""
<div class="marquee-container">
    <div class="marquee-content">
        {logos_html}
        {logos_html}
    </div>
</div>
"""
st.markdown(marquee_html, unsafe_allow_html=True)

# --- FILTER SECTION ---
with st.container():
    col_f1, col_f2, col_f3 = st.columns(3)
    years = sorted(df['year'].dropna().unique(), reverse=True)
    all_teams = sorted(set(df['team1'].unique().tolist() + df['team2'].unique().tolist()))
    all_venues = sorted(df['venue'].dropna().unique())
    
    with col_f1: selected_years = st.multiselect("Date Range", options=years, default=years[:5] if len(years) >= 5 else years)
    with col_f2: selected_teams = st.multiselect("Teams", options=all_teams, default=all_teams)
    with col_f3: selected_venues = st.multiselect("Venues", options=all_venues, default=all_venues)

filtered_df = df[
    (df['year'].isin(selected_years) if selected_years else True) &
    ((df['team1'].isin(selected_teams)) | (df['team2'].isin(selected_teams)) if selected_teams else True) &
    (df['venue'].isin(selected_venues) if selected_venues else True)
].copy()

# --- KPI METRICS ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Matches", f"{len(filtered_df):,}")
with col2: st.metric("Unique Teams", len(set(filtered_df['team1'].unique().tolist() + filtered_df['team2'].unique().tolist())))
with col3: st.metric("Stadiums Played", filtered_df['venue'].nunique())
with col4: st.metric("Total Cities", filtered_df['city'].nunique())
st.markdown("<br>", unsafe_allow_html=True)

# --- CHARTS ROW 1 ---
row1_col1, row1_col2 = st.columns([1.5, 1])

with row1_col1:
    st.markdown("<h4 style='color: #1e3a8a;'>Matches Won by Team</h4>", unsafe_allow_html=True)
    team_wins = filtered_df['winner'].value_counts().head(8).reset_index()
    team_wins.columns = ['Team', 'Wins']
    fig_wins = px.bar(team_wins, x='Team', y='Wins', color_discrete_sequence=['#3b82f6'])
    fig_wins.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Inter", color="#333"))
    st.plotly_chart(fig_wins, use_container_width=True)

with row1_col2:
    st.markdown("<h4 style='color: #1e3a8a;'>Toss Decisions</h4>", unsafe_allow_html=True)
    toss_decision = filtered_df['toss_decision'].value_counts().reset_index()
    toss_decision.columns = ['Decision', 'Count']
    fig_toss = px.pie(toss_decision, names='Decision', values='Count', hole=0.5, color_discrete_sequence=['#0dcaf0', '#1e3a8a'])
    fig_toss.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Inter", color="#333"), legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_toss, use_container_width=True)

# --- CHARTS ROW 2 ---
row2_col1, row2_col2 = st.columns([1, 1.5])

with row2_col1:
    st.markdown("<h4 style='color: #1e3a8a;'>Toss Strategy Impact</h4>", unsafe_allow_html=True)
    wins_by_decision = {'Bat First': 0, 'Field First': 0}
    for _, row in filtered_df.iterrows():
        if row['toss_winner'] == row['winner']:
            decision = 'Bat First' if str(row['toss_decision']).lower() == 'bat' else 'Field First'
            wins_by_decision[decision] += 1
        else:
            opposite = 'Field First' if str(row['toss_decision']).lower() == 'bat' else 'Bat First'
            wins_by_decision[opposite] += 1
            
    decision_df = pd.DataFrame({'Strategy': list(wins_by_decision.keys()), 'Matches Won': list(wins_by_decision.values())})
    fig_toss_win = px.bar(decision_df, x='Strategy', y='Matches Won', color_discrete_sequence=['#1e3a8a'])
    fig_toss_win.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Inter", color="#333"))
    st.plotly_chart(fig_toss_win, use_container_width=True)

with row2_col2:
    st.markdown("<h4 style='color: #1e3a8a;'>Recent Match Performance</h4>", unsafe_allow_html=True)
    display_df = filtered_df[['match_date', 'team1', 'team2', 'winner', 'player_of_match']].copy()
    display_df['match_date'] = display_df['match_date'].dt.strftime('%Y-%m-%d')
    display_df = display_df.sort_values('match_date', ascending=False).head(10)
    display_df.columns = ['Date', 'Team 1', 'Team 2', 'Winner', 'Player of Match']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# --- HEAD-TO-HEAD ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #1e3a8a;'>Head-to-Head Comparison</h4>", unsafe_allow_html=True)
h2h_col1, h2h_col2 = st.columns(2)

team1_select = h2h_col1.selectbox("Select Team 1", options=all_teams, index=all_teams.index('Chennai Super Kings') if 'Chennai Super Kings' in all_teams else 0)
team2_select = h2h_col2.selectbox("Select Team 2", options=all_teams, index=all_teams.index('Mumbai Indians') if 'Mumbai Indians' in all_teams else 1)

if team1_select and team2_select and team1_select != team2_select:
    h2h_matches = filtered_df[
        ((filtered_df['team1'] == team1_select) & (filtered_df['team2'] == team2_select)) |
        ((filtered_df['team1'] == team2_select) & (filtered_df['team2'] == team1_select))
    ]
    
    if len(h2h_matches) > 0:
        team1_wins = len(h2h_matches[h2h_matches['winner'] == team1_select])
        team2_wins = len(h2h_matches[h2h_matches['winner'] == team2_select])
        
        logo_col1, logo_col2, logo_col3 = st.columns([1, 1, 1])
        with logo_col1:
            st.markdown(f"<div style='text-align: center;'><img src='{TEAM_LOGOS.get(team1_select, '')}' width='120'></div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #1e3a8a;'>{team1_wins} Wins</h3>", unsafe_allow_html=True)
            
        with logo_col2:
            st.markdown("<h4 style='text-align: center; color: #64748b; margin-top: 25px;'>Total Matches</h4>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; font-size: 3.5rem; color: #0f172a;'>{len(h2h_matches)}</h1>", unsafe_allow_html=True)
            
        with logo_col3:
            st.markdown(f"<div style='text-align: center;'><img src='{TEAM_LOGOS.get(team2_select, '')}' width='120'></div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #1e3a8a;'>{team2_wins} Wins</h3>", unsafe_allow_html=True)
    else:
        st.info("No matches found between these teams in the selected filter range.")

# --- CUSTOM FOOTER ---
st.markdown("""
<div class="custom-footer">
    🏏 IPL Analytics Engine | Powered by Streamlit & Python
</div>
""", unsafe_allow_html=True)
