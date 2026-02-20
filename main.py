import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ultimate IPL Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Custom Header Design */
    .dashboard-header {
        background: linear-gradient(135deg, #141E30 0%, #243B55 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    .dashboard-header h1 {
        color: #F2C94C;
        font-weight: 800;
        margin: 0;
        font-size: 3rem;
        letter-spacing: 1px;
    }
    .dashboard-header p {
        color: #E0E0E0;
        font-size: 1.2rem;
        margin-top: 5px;
        font-weight: 300;
    }

    /* Scrolling Logo Marquee */
    .marquee-container {
        width: 100%;
        overflow: hidden;
        background: #ffffff;
        padding: 15px 0;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        white-space: nowrap;
        margin-bottom: 30px;
    }
    .marquee-content {
        display: inline-block;
        animation: scroll 35s linear infinite;
    }
    .marquee-content img {
        height: 60px;
        margin: 0 30px;
        vertical-align: middle;
        object-fit: contain;
    }
    @keyframes scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    /* Custom Footer Design */
    .dashboard-footer {
        background: linear-gradient(90deg, #F2C94C 0%, #F2994A 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: #141E30;
        font-weight: 600;
        margin-top: 50px;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.1);
    }
    
    /* Improve metric cards */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #F2C94C;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- COMPLETE TEAM LOGOS DICTIONARY ---
TEAM_LOGOS = {
    "Chennai Super Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Chennai_Super_Kings_Logo.svg/200px-Chennai_Super_Kings_Logo.svg.png",
    "Mumbai Indians": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Mumbai_Indians_Logo.svg/200px-Mumbai_Indians_Logo.svg.png",
    "Royal Challengers Bangalore": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f0/Royal_Challengers_Bengaluru_logo.svg/200px-Royal_Challengers_Bengaluru_logo.svg.png",
    "Royal Challengers Bengaluru": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f0/Royal_Challengers_Bengaluru_logo.svg/200px-Royal_Challengers_Bengaluru_logo.svg.png",
    "Kolkata Knight Riders": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/200px-Kolkata_Knight_Riders_Logo.svg.png",
    "Sunrisers Hyderabad": "https://upload.wikimedia.org/wikipedia/en/thumb/8/81/Sunrisers_Hyderabad.svg/200px-Sunrisers_Hyderabad.svg.png",
    "Rajasthan Royals": "https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Rajasthan_Royals_Logo.svg/200px-Rajasthan_Royals_Logo.svg.png",
    "Delhi Capitals": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Delhi_Capitals.svg/200px-Delhi_Capitals.svg.png",
    "Delhi Daredevils": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Delhi_Capitals.svg/200px-Delhi_Capitals.svg.png",
    "Punjab Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/200px-Punjab_Kings_Logo.svg.png",
    "Kings XI Punjab": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/200px-Punjab_Kings_Logo.svg.png",
    "Gujarat Titans": "https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Gujarat_Titans_Logo.svg/200px-Gujarat_Titans_Logo.svg.png",
    "Lucknow Super Giants": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/Lucknow_Super_Giants_IPL_Logo.svg/200px-Lucknow_Super_Giants_IPL_Logo.svg.png",
    "Pune Warriors": "https://upload.wikimedia.org/wikipedia/en/thumb/1/18/Pune_Warriors_India_logo.svg/200px-Pune_Warriors_India_logo.svg.png",
    "Deccan Chargers": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/Deccan_Chargers_Logo.svg/200px-Deccan_Chargers_Logo.svg.png",
    "Gujarat Lions": "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Gujarat_Lions_Logo.svg/200px-Gujarat_Lions_Logo.svg.png",
    "Rising Pune Supergiant": "https://upload.wikimedia.org/wikipedia/en/thumb/0/02/Rising_Pune_Supergiants_Logo.svg/200px-Rising_Pune_Supergiants_Logo.svg.png",
    "Rising Pune Supergiants": "https://upload.wikimedia.org/wikipedia/en/thumb/0/02/Rising_Pune_Supergiants_Logo.svg/200px-Rising_Pune_Supergiants_Logo.svg.png",
    "Kochi Tuskers Kerala": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Kochi_Tuskers_Kerala_Logo.svg/200px-Kochi_Tuskers_Kerala_Logo.svg.png"
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
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Indian_Premier_League_Official_Logo.svg/200px-Indian_Premier_League_Official_Logo.svg.png", width=150)
st.sidebar.markdown("### 🔍 Filter Dashboard")

years = sorted(df['year'].dropna().unique(), reverse=True)
selected_years = st.sidebar.multiselect("Select Year(s)", options=years, default=years[:5] if len(years) >= 5 else years)

all_teams = sorted(set(df['team1'].unique().tolist() + df['team2'].unique().tolist()))
selected_teams = st.sidebar.multiselect("Select Team(s)", options=all_teams, default=all_teams)

all_venues = sorted(df['venue'].dropna().unique())
selected_venues = st.sidebar.multiselect("Select Venue(s)", options=all_venues, default=all_venues)

all_cities = sorted(df['city'].dropna().unique())
selected_cities = st.sidebar.multiselect("Select City/Cities", options=all_cities, default=all_cities)

filtered_df = df[
    (df['year'].isin(selected_years) if selected_years else True) &
    ((df['team1'].isin(selected_teams)) | (df['team2'].isin(selected_teams)) if selected_teams else True) &
    (df['venue'].isin(selected_venues) if selected_venues else True) &
    (df['city'].isin(selected_cities) if selected_cities else True)
].copy()

# --- MAIN HEADER ---
st.markdown("""
<div class="dashboard-header">
    <h1>🏏 Ultimate IPL Analytics Hub</h1>
    <p>Dive deep into match statistics, toss strategies, and head-to-head dominance</p>
</div>
""", unsafe_allow_html=True)

# --- SCROLLING LOGO BANNER ---
# Create the HTML for the logos. We duplicate the list to make the scroll seamless.
logos_html = "".join([f"<img src='{url}' title='{team}'>" for team, url in TEAM_LOGOS.items()])
marquee_html = f"""
<div class="marquee-container">
    <div class="marquee-content">
        {logos_html}
        {logos_html} </div>
</div>
"""
st.markdown(marquee_html, unsafe_allow_html=True)

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Matches Analyzed", len(filtered_df))
with col2: st.metric("Teams Involved", len(set(filtered_df['team1'].unique().tolist() + filtered_df['team2'].unique().tolist())))
with col3: st.metric("Venues Played", filtered_df['venue'].nunique())
with col4: st.metric("Cities Visited", filtered_df['city'].nunique())
st.markdown("<br>", unsafe_allow_html=True)

# --- TEAM PERFORMANCE ---
st.header("🏆 Dominance & Performance")
col1, col2 = st.columns(2)

with col1:
    team_wins = filtered_df['winner'].value_counts().head(10).reset_index()
    team_wins.columns = ['Team', 'Wins']
    fig_wins = px.bar(team_wins, x='Wins', y='Team', orientation='h', title="Top 10 Teams by Total Wins", color='Wins', color_continuous_scale='Magma')
    fig_wins.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_wins, use_container_width=True)

with col2:
    team_matches = {}
    for team in all_teams:
        matches = len(filtered_df[(filtered_df['team1'] == team) | (filtered_df['team2'] == team)])
        wins = len(filtered_df[filtered_df['winner'] == team])
        if matches > 0:
            team_matches[team] = {'Team': team, 'Win %': (wins / matches) * 100}
    
    win_pct_df = pd.DataFrame(team_matches.values()).sort_values('Win %', ascending=False).head(10)
    fig_pct = px.bar(win_pct_df, x='Team', y='Win %', title="Most Efficient Teams (Win Percentage)", color='Win %', color_continuous_scale='Viridis')
    fig_pct.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis_tickangle=-45)
    st.plotly_chart(fig_pct, use_container_width=True)

# --- TOSS ANALYSIS (NO PIE CHARTS) ---
st.markdown("---")
st.header("🎲 The Toss Strategy")
col1, col2 = st.columns(2)

with col1:
    # Bar chart replacing Pie Chart for Decision
    toss_decision = filtered_df['toss_decision'].value_counts().reset_index()
    toss_decision.columns = ['Decision', 'Count']
    fig_toss = px.bar(toss_decision, x='Decision', y='Count', title="What do captains choose?", color='Decision', color_discrete_sequence=['#243B55', '#F2C94C'])
    fig_toss.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_toss, use_container_width=True)

with col2:
    # Bar chart replacing Pie Chart for Match Wins
    wins_by_decision = {'Bat First': 0, 'Field First': 0}
    for _, row in filtered_df.iterrows():
        if row['toss_winner'] == row['winner']:
            decision = 'Bat First' if str(row['toss_decision']).lower() == 'bat' else 'Field First'
            wins_by_decision[decision] += 1
        else:
            opposite = 'Field First' if str(row['toss_decision']).lower() == 'bat' else 'Bat First'
            wins_by_decision[opposite] += 1
            
    decision_df = pd.DataFrame({'Strategy': list(wins_by_decision.keys()), 'Matches Won': list(wins_by_decision.values())})
    fig_toss_win = px.bar(decision_df, x='Strategy', y='Matches Won', title="Which Strategy Actually Wins Matches?", color='Strategy', color_discrete_sequence=['#F2C94C', '#243B55'])
    fig_toss_win.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_toss_win, use_container_width=True)

# --- HEAD-TO-HEAD WITH TUG OF WAR CHART ---
st.markdown("---")
st.header("⚔️ Ultimate Head-to-Head Clash")
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
            st.markdown("<h4 style='text-align: center; color: gray;'>Total Encounters</h4>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; font-size: 3.5rem; color: #243B55;'>{len(h2h_matches)}</h1>", unsafe_allow_html=True)
            
        with logo_col3:
            if team2_select in TEAM_LOGOS: st.image(TEAM_LOGOS[team2_select], width=120)
            st.metric(f"{team2_select} Wins", team2_wins)
            
        # Tug of War Bar Chart (Replaces Pie Chart)
        st.markdown("<br>", unsafe_allow_html=True)
        h2h_df = pd.DataFrame({'Matchup': ['Dominance Ratio'], team1_select: [team1_wins], team2_select: [team2_wins]})
        fig_h2h = px.bar(h2h_df, x=[team1_select, team2_select], y='Matchup', orientation='h', 
                         title="Head-to-Head Tug of War", text_auto=True,
                         color_discrete_sequence=['#F2C94C', '#243B55'])
        fig_h2h.update_layout(barmode='stack', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Total Matches Won", yaxis_title="")
        st.plotly_chart(fig_h2h, use_container_width=True)
    else:
        st.info(f"No matches found between {team1_select} and {team2_select} based on current filters.")

# --- TIME SERIES & PLAYERS ---
st.markdown("---")
st.header("📈 Historical Trends & Star Power")
col1, col2 = st.columns(2)

with col1:
    matches_by_year = filtered_df.groupby('year').size().reset_index(name='matches')
    fig_timeline = px.line(matches_by_year, x='year', y='matches', title="Number of Matches per Season", markers=True)
    fig_timeline.update_traces(line_color='#F2C94C', line_width=4, marker_size=10, marker_color='#243B55')
    fig_timeline.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_timeline, use_container_width=True)

with col2:
    potm_counts = filtered_df['player_of_match'].value_counts().head(10).reset_index()
    potm_counts.columns = ['Player', 'Awards']
    fig_potm = px.bar(potm_counts, x='Awards', y='Player', orientation='h', title="Top 10 Player of the Match Awards", color='Awards', color_continuous_scale='teal')
    fig_potm.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_potm, use_container_width=True)

# --- DATA TABLE & FOOTER ---
st.markdown("---")
st.header("📋 Raw Database")
st.dataframe(filtered_df[['match_number', 'team1', 'team2', 'match_date', 'venue', 'city', 'winner', 'player_of_match']].sort_values('match_date', ascending=False), use_container_width=True, height=250)

csv = filtered_df.to_csv(index=False)
st.download_button(label="📥 Download Filtered Data as CSV", data=csv, file_name=f"ipl_matches_filtered_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# Custom Footer
st.markdown("""
<div class="dashboard-footer">
    Built with Python & Streamlit 🚀 | IPL Analytics Engine
</div>
""", unsafe_allow_html=True)
