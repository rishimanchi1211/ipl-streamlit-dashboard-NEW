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

    /* Top Dark Blue Header matching the reference image */
    .custom-header {
        background-color: #1e3a8a;
        padding: 20px 30px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        margin-top: -30px;
    }
    .custom-header h1 {
        color: white !important;
        margin: 0;
        font-size: 26px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Style the Metrics like the image (White cards with borders) */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 15px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="metric-container"] label {
        color: #64748b !important;
        font-weight: 500;
        font-size: 14px;
    }
    div[data-testid="metric-container"] div {
        color: #0f172a !important;
        font-weight: 700;
    }

    /* Style Chart Containers to look like white cards */
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
        height: 60px;
        margin: 0 25px;
        vertical-align: middle;
        object-fit: contain;
    }
    @keyframes scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    </style>
""", unsafe_allow_html=True)

# --- MASTER SVG LOGOS (THESE WILL NOT BREAK) ---
TEAM_LOGOS = {
    "Chennai Super Kings": "https://upload.wikimedia.org/wikipedia/en/2/2b/Chennai_Super_Kings_Logo.svg",
    "Mumbai Indians": "https://upload.wikimedia.org/wikipedia/en/c/cd/Mumbai_Indians_Logo.svg",
    "Royal Challengers Bangalore": "https://upload.wikimedia.org/wikipedia/en/f/f0/Royal_Challengers_Bengaluru_logo.svg",
    "Royal Challengers Bengaluru": "https://upload.wikimedia.org/wikipedia/en/f/f0/Royal_Challengers_Bengaluru_logo.svg",
    "Kolkata Knight Riders": "https://upload.wikimedia.org/wikipedia/en/4/4c/Kolkata_Knight_Riders_Logo.svg",
    "Sunrisers Hyderabad": "https://upload.wikimedia.org/wikipedia/en/8/81/Sunrisers_Hyderabad.svg",
    "Rajasthan Royals": "https://upload.wikimedia.org/wikipedia/en/6/60/Rajasthan_Royals_Logo.svg",
    "Delhi Capitals": "https://upload.wikimedia.org/wikipedia/en/2/2f/Delhi_Capitals.svg",
    "Delhi Daredevils": "https://upload.wikimedia.org/wikipedia/en/2/2f/Delhi_Capitals.svg",
    "Punjab Kings": "https://upload.wikimedia.org/wikipedia/en/d/d4/Punjab_Kings_Logo.svg",
    "Kings XI Punjab": "https://upload.wikimedia.org/wikipedia/en/d/d4/Punjab_Kings_Logo.svg",
    "Gujarat Titans": "https://upload.wikimedia.org/wikipedia/en/0/09/Gujarat_Titans_Logo.svg",
    "Lucknow Super Giants": "https://upload.wikimedia.org/wikipedia/en/a/a9/Lucknow_Super_Giants_IPL_Logo.svg",
    "Pune Warriors": "https://upload.wikimedia.org/wikipedia/en/1/18/Pune_Warriors_India_logo.svg",
    "Deccan Chargers": "https://upload.wikimedia.org/wikipedia/en/b/bf/Deccan_Chargers_Logo.svg",
    "Gujarat Lions": "https://upload.wikimedia.org/wikipedia/en/3/30/Gujarat_Lions_Logo.svg",
    "Rising Pune Supergiant": "https://upload.wikimedia.org/wikipedia/en/0/02/Rising_Pune_Supergiants_Logo.svg",
    "Rising Pune Supergiants": "https://upload.wikimedia.org/wikipedia/en/0/02/Rising_Pune_Supergiants_Logo.svg",
    "Kochi Tuskers Kerala": "https://upload.wikimedia.org/wikipedia/en/d/d4/Kochi_Tuskers_Kerala_Logo.svg"
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
    <img src="https://upload.wikimedia.org/wikipedia/en/8/84/Indian_Premier_League_Official_Logo.svg" width="60" style="background: white; border-radius: 8px; padding: 2px;">
    <h1>IPL Analytical Dashboard</h1>
</div>
""", unsafe_allow_html=True)

# --- SCROLLING LOGO BANNER ---
logos_html = "".join([f"<img src='{url}' title='{team}'>" for team, url in TEAM_LOGOS.items()])
marquee_html = f"""
<div class="marquee-container">
    <div class="marquee-content">
        {logos_html}
        {logos_html}
    </div>
</div>
"""
st.markdown(marquee_html, unsafe_allow_html=True)

# --- FILTER SECTION (Matched to Image Style) ---
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
    st.markdown("#### Matches Won by Team")
    team_wins = filtered_df['winner'].value_counts().head(8).reset_index()
    team_wins.columns = ['Team', 'Wins']
    # Theme blue bar chart
    fig_wins = px.bar(team_wins, x='Team', y='Wins', color_discrete_sequence=['#0275d8'])
    fig_wins.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Inter", color="#333"))
    st.plotly_chart(fig_wins, use_container_width=True)

with row1_col2:
    st.markdown("#### Toss Decisions")
    toss_decision = filtered_df['toss_decision'].value_counts().reset_index()
    toss_decision.columns = ['Decision', 'Count']
    # Donut chart matching the image
    fig_toss = px.pie(toss_decision, names='Decision', values='Count', hole=0.5, color_discrete_sequence=['#0dcaf0', '#6f42c1'])
    fig_toss.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Inter", color="#333"), legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_toss, use_container_width=True)

# --- CHARTS ROW 2 ---
row2_col1, row2_col2 = st.columns([1, 1.5])

with row2_col1:
    st.markdown("#### Toss Strategy Impact")
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
    st.markdown("#### Recent Match Performance Data")
    # Clean up the table to look professional
    display_df = filtered_df[['match_date', 'team1', 'team2', 'winner', 'player_of_match']].copy()
    display_df['match_date'] = display_df['match_date'].dt.strftime('%Y-%m-%d')
    display_df = display_df.sort_values('match_date', ascending=False).head(10)
    display_df.columns = ['Date', 'Team 1', 'Team 2', 'Winner', 'Player of Match']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# --- HEAD-TO-HEAD ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### Head-to-Head Comparison")
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
            st.markdown(f"<div style='text-align: center;'><img src='{TEAM_LOGOS.get(team1_select, '')}' width='100'></div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #1e3a8a;'>{team1_wins} Wins</h3>", unsafe_allow_html=True)
            
        with logo_col2:
            st.markdown("<h4 style='text-align: center; color: #64748b; margin-top: 15px;'>Matches</h4>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; font-size: 3rem; color: #0f172a;'>{len(h2h_matches)}</h1>", unsafe_allow_html=True)
            
        with logo_col3:
            st.markdown(f"<div style='text-align: center;'><img src='{TEAM_LOGOS.get(team2_select, '')}' width='100'></div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #1e3a8a;'>{team2_wins} Wins</h3>", unsafe_allow_html=True)
    else:
        st.info("No matches found between these teams in the selected filter range.")
