import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IPL Analytics Hub",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar by default
)

# --- CUSTOM CSS FOR FONTS & STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Title Gradient */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298, #ff4b2b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 20px;
    }
    
    /* KPI Card Styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 5px solid #ff4b2b;
        transition: transform 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- TEAM LOGOS DICTIONARY (Updated URLs) ---
TEAM_LOGOS = {
    "Chennai Super Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Chennai_Super_Kings_Logo.svg/200px-Chennai_Super_Kings_Logo.svg.png",
    "Mumbai Indians": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Mumbai_Indians_Logo.svg/200px-Mumbai_Indians_Logo.svg.png",
    "Royal Challengers Bangalore": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f0/Royal_Challengers_Bengaluru_logo.svg/200px-Royal_Challengers_Bengaluru_logo.svg.png",
    "Kolkata Knight Riders": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/200px-Kolkata_Knight_Riders_Logo.svg.png",
    "Sunrisers Hyderabad": "https://upload.wikimedia.org/wikipedia/en/thumb/8/81/Sunrisers_Hyderabad.svg/200px-Sunrisers_Hyderabad.svg.png",
    "Rajasthan Royals": "https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Rajasthan_Royals_Logo.svg/200px-Rajasthan_Royals_Logo.svg.png",
    "Delhi Capitals": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Delhi_Capitals.svg/200px-Delhi_Capitals.svg.png",
    "Punjab Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/200px-Punjab_Kings_Logo.svg.png",
    "Gujarat Titans": "https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Gujarat_Titans_Logo.svg/200px-Gujarat_Titans_Logo.svg.png",
    "Lucknow Super Giants": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/Lucknow_Super_Giants_IPL_Logo.svg/200px-Lucknow_Super_Giants_IPL_Logo.svg.png"
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

# --- MAIN TITLE & LOGO BANNER ---
st.markdown('<div class="main-title">🏏 IPL Analytics Hub</div>', unsafe_allow_html=True)

# Generate Banner using native Streamlit columns (Much more reliable than HTML img tags)
active_teams = list(TEAM_LOGOS.keys())
cols = st.columns(10)
for i, team in enumerate(active_teams):
    with cols[i]:
        st.image(TEAM_LOGOS[team], use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- HORIZONTAL FILTER PANEL (Replacing Sidebar) ---
with st.expander("⚙️ **Dashboard Controls & Filters**", expanded=True):
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        years = sorted(df['year'].dropna().unique(), reverse=True)
        selected_years = st.multiselect("📅 Select Year(s)", options=years, default=years[:5] if len(years) >= 5 else years)
    
    with filter_col2:
        all_teams = sorted(set(df['team1'].unique().tolist() + df['team2'].unique().tolist()))
        selected_teams = st.multiselect("🏏 Select Team(s)", options=all_teams, default=all_teams)
        
    with filter_col3:
        all_venues = sorted(df['venue'].dropna().unique())
        selected_venues = st.multiselect("🏟️ Select Venue(s)", options=all_venues, default=all_venues)
        
    with filter_col4:
        all_cities = sorted(df['city'].dropna().unique())
        selected_cities = st.multiselect("🏙️ Select City", options=all_cities, default=all_cities)

# Apply filters
filtered_df = df[
    (df['year'].isin(selected_years) if selected_years else True) &
    ((df['team1'].isin(selected_teams)) | (df['team2'].isin(selected_teams)) if selected_teams else True) &
    (df['venue'].isin(selected_venues) if selected_venues else True) &
    (df['city'].isin(selected_cities) if selected_cities else True)
].copy()

st.markdown("---")

# --- KPI METRICS ---
st.header("📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Matches", len(filtered_df))
with col2: st.metric("Active Teams", len(set(filtered_df['team1'].unique().tolist() + filtered_df['team2'].unique().tolist())))
with col3: st.metric("Venues Played", filtered_df['venue'].nunique())
with col4: st.metric("Cities Visited", filtered_df['city'].nunique())
st.markdown("<br>", unsafe_allow_html=True)

# --- TEAM PERFORMANCE & TOSS STRATEGY (No Pie Charts) ---
st.header("🏆 Performance & Strategy")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    # Replaced Pie Chart with Horizontal Bar
    team_wins = filtered_df['winner'].value_counts().head(10).reset_index()
    team_wins.columns = ['Team', 'Wins']
    fig_wins = px.bar(team_wins, x='Wins', y='Team', orientation='h', title="Top 10 Teams by Total Wins", color='Wins', color_continuous_scale='Magma')
    fig_wins.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_wins, use_container_width=True)

with row1_col2:
    # Replaced Pie Chart with a clear Bar Chart showing Toss Decision Impact
    wins_by_decision = {'Bat First': 0, 'Field First': 0}
    for _, row in filtered_df.iterrows():
        if row['toss_winner'] == row['winner']:
            decision = 'Bat First' if str(row['toss_decision']).lower() == 'bat' else 'Field First'
            wins_by_decision[decision] += 1
        else:
            opposite = 'Field First' if str(row['toss_decision']).lower() == 'bat' else 'Bat First'
            wins_by_decision[opposite] += 1
            
    decision_df = pd.DataFrame({'Strategy': list(wins_by_decision.keys()), 'Matches Won': list(wins_by_decision.values())})
    fig_toss = px.bar(decision_df, x='Strategy', y='Matches Won', title="Which Toss Strategy Wins More Matches?", color='Strategy', color_discrete_sequence=['#2a5298', '#ff4b2b'])
    fig_toss.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_toss, use_container_width=True)

# --- HEAD-TO-HEAD WITH LOGOS ---
st.header("⚔️ Ultimate Head-to-Head")
h2h_filter_col1, h2h_filter_col2 = st.columns(2)

team1_select = h2h_filter_col1.selectbox("Choose Team 1", options=all_teams, key='team1_h2h', index=all_teams.index('Chennai Super Kings') if 'Chennai Super Kings' in all_teams else 0)
team2_select = h2h_filter_col2.selectbox("Choose Team 2", options=all_teams, key='team2_h2h', index=all_teams.index('Mumbai Indians') if 'Mumbai Indians' in all_teams else 1)

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
            if team1_select in TEAM_LOGOS: st.image(TEAM_LOGOS[team1_select], width=150)
            st.metric(f"{team1_select}", f"{team1_wins} Wins")
            
        with logo_col2:
            st.markdown("<h4 style='text-align: center; color: gray;'>Total Encounters</h4>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; font-size: 4rem;'>{len(h2h_matches)}</h1>", unsafe_allow_html=True)
            
        with logo_col3:
            if team2_select in TEAM_LOGOS: st.image(TEAM_LOGOS[team2_select], width=150)
            st.metric(f"{team2_select}", f"{team2_wins} Wins")
            
        # Replaced H2H Pie Chart with a "Tug-of-War" Stacked Bar Chart
        st.markdown("<br>", unsafe_allow_html=True)
        h2h_df = pd.DataFrame({'Matchup': ['Win Ratio'], team1_select: [team1_wins], team2_select: [team2_wins]})
        fig_h2h = px.bar(h2h_df, x=[team1_select, team2_select], y='Matchup', orientation='h', 
                         title="Head-to-Head Dominance Ratio", text_auto=True,
                         color_discrete_sequence=['#ff4b2b', '#2a5298'])
        fig_h2h.update_layout(barmode='stack', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Matches Won", yaxis_title="")
        st.plotly_chart(fig_h2h, use_container_width=True)
    else:
        st.warning(f"No matches found between {team1_select} and {team2_select}.")

# --- TIME SERIES & PLAYERS ---
st.header("🌟 League Trends & Star Players")
col3, col4 = st.columns(2)

with col3:
    matches_by_year = filtered_df.groupby('year').size().reset_index(name='matches')
    fig_timeline = px.line(matches_by_year, x='year', y='matches', title="Matches Played Per Year", markers=True)
    fig_timeline.update_traces(line_color='#ff4b2b', line_width=4, marker_size=12)
    fig_timeline.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_timeline, use_container_width=True)

with col4:
    potm_counts = filtered_df['player_of_match'].value_counts().head(10).reset_index()
    potm_counts.columns = ['Player', 'Awards']
    fig_potm = px.bar(potm_counts, x='Awards', y='Player', orientation='h', title="Top 10 Player of the Match Awards", color='Awards', color_continuous_scale='Teal')
    fig_potm.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_potm, use_container_width=True)

# --- DATA TABLE ---
st.markdown("---")
st.header("📋 Raw Match Database")
st.dataframe(filtered_df[['match_number', 'team1', 'team2', 'match_date', 'venue', 'city', 'winner', 'player_of_match']].sort_values('match_date', ascending=False), use_container_width=True, height=300)

csv = filtered_df.to_csv(index=False)
st.download_button(label="📥 Export Filtered Data (CSV)", data=csv, file_name=f"ipl_analytics_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
