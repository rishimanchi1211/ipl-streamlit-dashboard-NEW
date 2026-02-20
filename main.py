import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IPL Match Analysis Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TEAM LOGOS DICTIONARY ---
TEAM_LOGOS = {
    "Chennai Super Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Chennai_Super_Kings_Logo.svg/1200px-Chennai_Super_Kings_Logo.svg.png",
    "Mumbai Indians": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Mumbai_Indians_Logo.svg/1200px-Mumbai_Indians_Logo.svg.png",
    "Royal Challengers Bangalore": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/Royal_Challengers_Bangalore_2020.svg/1200px-Royal_Challengers_Bangalore_2020.svg.png",
    "Kolkata Knight Riders": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/1200px-Kolkata_Knight_Riders_Logo.svg.png",
    "Sunrisers Hyderabad": "https://upload.wikimedia.org/wikipedia/en/thumb/8/81/Sunrisers_Hyderabad.svg/1200px-Sunrisers_Hyderabad.svg.png",
    "Rajasthan Royals": "https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Rajasthan_Royals_Logo.svg/1200px-Rajasthan_Royals_Logo.svg.png",
    "Delhi Capitals": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Delhi_Capitals.svg/1200px-Delhi_Capitals.svg.png",
    "Punjab Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/1200px-Punjab_Kings_Logo.svg.png",
    "Gujarat Titans": "https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Gujarat_Titans_Logo.svg/1200px-Gujarat_Titans_Logo.svg.png",
    "Lucknow Super Giants": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/Lucknow_Super_Giants_IPL_Logo.svg/1200px-Lucknow_Super_Giants_IPL_Logo.svg.png"
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

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")

years = sorted(df['year'].dropna().unique(), reverse=True)
selected_years = st.sidebar.multiselect("Select Year(s)", options=years, default=years[:5] if len(years) >= 5 else years)

all_teams = sorted(set(df['team1'].unique().tolist() + df['team2'].unique().tolist()))
selected_teams = st.sidebar.multiselect("Select Team(s)", options=all_teams, default=all_teams)

all_venues = sorted(df['venue'].dropna().unique())
selected_venues = st.sidebar.multiselect("Select Venue(s)", options=all_venues, default=all_venues)

all_cities = sorted(df['city'].dropna().unique())
selected_cities = st.sidebar.multiselect("Select City/Cities", options=all_cities, default=all_cities)

# Apply filters
filtered_df = df[
    (df['year'].isin(selected_years) if selected_years else True) &
    ((df['team1'].isin(selected_teams)) | (df['team2'].isin(selected_teams)) if selected_teams else True) &
    (df['venue'].isin(selected_venues) if selected_venues else True) &
    (df['city'].isin(selected_cities) if selected_cities else True)
].copy()

# --- MAIN DASHBOARD HEADER & LOGO BANNER ---
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🏏 IPL Match Analysis Dashboard</h2>", unsafe_allow_html=True)

# Generate HTML for the banner with the 10 active teams
active_teams = [
    "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Sunrisers Hyderabad", "Rajasthan Royals",
    "Delhi Capitals", "Punjab Kings", "Gujarat Titans", "Lucknow Super Giants"
]

banner_html = "<div style='display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 30px; padding-top: 10px; padding-bottom: 20px;'>"
for team in active_teams:
    if team in TEAM_LOGOS:
        banner_html += f"<img src='{TEAM_LOGOS[team]}' width='70' title='{team}' style='border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>"
banner_html += "</div><hr>"

st.markdown(banner_html, unsafe_allow_html=True)

# --- KPI METRICS ---
st.header("📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Matches", len(filtered_df))
with col2:
    st.metric("Teams", len(set(filtered_df['team1'].unique().tolist() + filtered_df['team2'].unique().tolist())))
with col3:
    st.metric("Venues", filtered_df['venue'].nunique())
with col4:
    st.metric("Cities", filtered_df['city'].nunique())
st.markdown("---")

# --- TEAM PERFORMANCE ---
st.header("🏆 Team Performance Analysis")
col1, col2 = st.columns(2)

with col1:
    team_wins = filtered_df['winner'].value_counts().head(10)
    fig_wins = px.bar(x=team_wins.values, y=team_wins.index, orientation='h', title="Top 10 Teams by Wins", labels={'x': 'Number of Wins', 'y': 'Team'}, color=team_wins.values, color_continuous_scale='viridis')
    fig_wins.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_wins, use_container_width=True)

with col2:
    team_matches = {}
    for team in all_teams:
        matches = len(filtered_df[(filtered_df['team1'] == team) | (filtered_df['team2'] == team)])
        wins = len(filtered_df[filtered_df['winner'] == team])
        if matches > 0:
            team_matches[team] = {'matches': matches, 'wins': wins, 'win_percentage': (wins / matches) * 100}
    
    win_pct_df = pd.DataFrame(team_matches).T.sort_values('win_percentage', ascending=False).head(10)
    fig_pct = px.bar(x=win_pct_df.index, y=win_pct_df['win_percentage'], title="Top 10 Teams by Win Percentage", labels={'x': 'Team', 'y': 'Win Percentage (%)'}, color=win_pct_df['win_percentage'], color_continuous_scale='plasma')
    fig_pct.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_pct, use_container_width=True)

# --- TOSS ANALYSIS ---
st.header("🎲 Toss Analysis")
col1, col2 = st.columns(2)

with col1:
    toss_decision = filtered_df['toss_decision'].value_counts()
    fig_toss = px.pie(values=toss_decision.values, names=toss_decision.index, title="Toss Decision Distribution", color_discrete_sequence=px.colors.qualitative.Set3)
    fig_toss.update_layout(height=400)
    st.plotly_chart(fig_toss, use_container_width=True)

with col2:
    toss_winner_match_winner = filtered_df[filtered_df['toss_winner'] == filtered_df['winner']]
    toss_impact = {'Toss Winner Won': len(toss_winner_match_winner), 'Toss Winner Lost': len(filtered_df) - len(toss_winner_match_winner)}
    fig_impact = px.pie(values=list(toss_impact.values()), names=list(toss_impact.keys()), title="Toss Winner Impact on Match Result", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_impact.update_layout(height=400)
    st.plotly_chart(fig_impact, use_container_width=True)

st.subheader("🏆 Match Wins by Toss Decision")
wins_by_decision = {'bat': 0, 'field': 0}
for _, row in filtered_df.iterrows():
    if row['toss_winner'] == row['winner']:
        decision = str(row['toss_decision']).lower()
        if decision in wins_by_decision: wins_by_decision[decision] += 1
    else:
        opposite_decision = 'field' if str(row['toss_decision']).lower() == 'bat' else 'bat'
        if opposite_decision in wins_by_decision: wins_by_decision[opposite_decision] += 1

col1, col2, col3 = st.columns(3)
with col1: st.metric("Wins Choosing to Bat", wins_by_decision['bat'])
with col2: st.metric("Wins Choosing to Field", wins_by_decision['field'])
with col3: st.metric("Total Matches", wins_by_decision['bat'] + wins_by_decision['field'])

# --- VENUE ANALYSIS ---
st.header("📍 Venue Analysis")
col1, col2 = st.columns(2)

with col1:
    venue_counts = filtered_df['venue'].value_counts().head(10)
    fig_venue = px.bar(x=venue_counts.index, y=venue_counts.values, title="Top 10 Venues by Matches", labels={'x': 'Venue', 'y': 'Matches'}, color=venue_counts.values, color_continuous_scale='blues')
    fig_venue.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_venue, use_container_width=True)

with col2:
    city_counts = filtered_df['city'].value_counts().head(10)
    fig_city = px.bar(x=city_counts.index, y=city_counts.values, title="Top 10 Cities by Matches", labels={'x': 'City', 'y': 'Matches'}, color=city_counts.values, color_continuous_scale='greens')
    fig_city.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_city, use_container_width=True)

# --- TIME SERIES ANALYSIS ---
st.header("📈 Matches Over Time")
matches_by_year = filtered_df.groupby('year').size().reset_index(name='matches')
fig_timeline = px.line(matches_by_year, x='year', y='matches', title="Number of Matches by Year", markers=True, labels={'year': 'Year', 'matches': 'Number of Matches'})
fig_timeline.update_traces(line_color='#1f77b4', line_width=3, marker_size=10)
st.plotly_chart(fig_timeline, use_container_width=True)

# --- PLAYER OF THE MATCH ---
st.header("⭐ Player of the Match Analysis")
col1, col2 = st.columns(2)

with col1:
    potm_counts = filtered_df['player_of_match'].value_counts().head(15)
    fig_potm = px.bar(x=potm_counts.values, y=potm_counts.index, orientation='h', title="Top 15 Players by POTM Awards", labels={'x': 'Awards', 'y': 'Player'}, color=potm_counts.values, color_continuous_scale='sunset')
    fig_potm.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig_potm, use_container_width=True)

with col2:
    potm_by_team = filtered_df.groupby('winner')['player_of_match'].count().sort_values(ascending=False).head(10)
    fig_potm_team = px.bar(x=potm_by_team.index, y=potm_by_team.values, title="Top 10 Teams by POTM Awards", labels={'x': 'Team', 'y': 'Awards'}, color=potm_by_team.values, color_continuous_scale='reds')
    fig_potm_team.update_layout(showlegend=False, height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig_potm_team, use_container_width=True)

# --- HEAD-TO-HEAD WITH LOGOS ---
st.header("⚔️ Team Head-to-Head Analysis")
col1, col2 = st.columns(2)

team1_select = col1.selectbox("Select Team 1", options=all_teams, key='team1_h2h', index=all_teams.index('Chennai Super Kings') if 'Chennai Super Kings' in all_teams else 0)
team2_select = col2.selectbox("Select Team 2", options=all_teams, key='team2_h2h', index=all_teams.index('Mumbai Indians') if 'Mumbai Indians' in all_teams else 1)

if team1_select and team2_select and team1_select != team2_select:
    h2h_matches = filtered_df[
        ((filtered_df['team1'] == team1_select) & (filtered_df['team2'] == team2_select)) |
        ((filtered_df['team1'] == team2_select) & (filtered_df['team2'] == team1_select))
    ]
    
    if len(h2h_matches) > 0:
        team1_wins = len(h2h_matches[h2h_matches['winner'] == team1_select])
        team2_wins = len(h2h_matches[h2h_matches['winner'] == team2_select])
        
        # Display Logos and Metrics
        logo_col1, logo_col2, logo_col3 = st.columns([1, 1, 1])
        with logo_col1:
            if team1_select in TEAM_LOGOS: st.image(TEAM_LOGOS[team1_select], width=120)
            st.metric(f"{team1_select} Wins", team1_wins)
            
        with logo_col2:
            st.markdown("<h4 style='text-align: center;'>Total Encounters</h4>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center;'>{len(h2h_matches)}</h1>", unsafe_allow_html=True)
            
        with logo_col3:
            if team2_select in TEAM_LOGOS: st.image(TEAM_LOGOS[team2_select], width=120)
            st.metric(f"{team2_select} Wins", team2_wins)
            
        # H2H Pie Chart
        h2h_data = {team1_select: team1_wins, team2_select: team2_wins}
        fig_h2h = px.pie(values=list(h2h_data.values()), names=list(h2h_data.keys()), title=f"Win Ratio: {team1_select} vs {team2_select}", color_discrete_sequence=px.colors.qualitative.Bold)
        fig_h2h.update_layout(height=400)
        st.plotly_chart(fig_h2h, use_container_width=True)
    else:
        st.info(f"No matches found between {team1_select} and {team2_select}.")

# --- DATA TABLE ---
st.header("📋 Match Data")
st.dataframe(filtered_df[['match_number', 'team1', 'team2', 'match_date', 'venue', 'city', 'winner', 'player_of_match']].sort_values('match_date', ascending=False), use_container_width=True, height=400)

csv = filtered_df.to_csv(index=False)
st.download_button(label="📥 Download Filtered Data as CSV", data=csv, file_name=f"ipl_matches_filtered_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

st.markdown("---")
st.markdown("**IPL Match Analysis Dashboard** | Data sourced from Match_Info.csv")
