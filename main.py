import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="IPL Match Analysis Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/Match_Info.csv")
    # Convert match_date to datetime
    df['match_date'] = pd.to_datetime(df['match_date'], errors='coerce')
    # Extract year from match_date
    df['year'] = df['match_date'].dt.year
    # Clean team names (handle variations)
    df['team1'] = df['team1'].str.strip()
    df['team2'] = df['team2'].str.strip()
    df['winner'] = df['winner'].str.strip()
    # Filter out rows with no result or invalid data
    df = df[df['result'] == 'Win'].copy()
    return df

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Year filter
years = sorted(df['year'].dropna().unique(), reverse=True)
selected_years = st.sidebar.multiselect(
    "Select Year(s)",
    options=years,
    default=years[:5] if len(years) >= 5 else years
)

# Team filter
all_teams = sorted(set(df['team1'].unique().tolist() + df['team2'].unique().tolist()))
selected_teams = st.sidebar.multiselect(
    "Select Team(s)",
    options=all_teams,
    default=all_teams
)

# Venue filter
all_venues = sorted(df['venue'].dropna().unique())
selected_venues = st.sidebar.multiselect(
    "Select Venue(s)",
    options=all_venues,
    default=all_venues
)

# City filter
all_cities = sorted(df['city'].dropna().unique())
selected_cities = st.sidebar.multiselect(
    "Select City/Cities",
    options=all_cities,
    default=all_cities
)

# Apply filters
filtered_df = df[
    (df['year'].isin(selected_years) if selected_years else True) &
    ((df['team1'].isin(selected_teams)) | (df['team2'].isin(selected_teams)) if selected_teams else True) &
    (df['venue'].isin(selected_venues) if selected_venues else True) &
    (df['city'].isin(selected_cities) if selected_cities else True)
].copy()

# Main title
st.title("🏏 IPL Match Analysis Dashboard")
st.markdown("---")

# KPI Metrics
st.header("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_matches = len(filtered_df)
    st.metric("Total Matches", total_matches)

with col2:
    unique_teams = len(set(filtered_df['team1'].unique().tolist() + filtered_df['team2'].unique().tolist()))
    st.metric("Teams", unique_teams)

with col3:
    unique_venues = filtered_df['venue'].nunique()
    st.metric("Venues", unique_venues)

with col4:
    unique_cities = filtered_df['city'].nunique()
    st.metric("Cities", unique_cities)

st.markdown("---")

# Team Performance Section
st.header("🏆 Team Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    # Wins by team
    team_wins = filtered_df['winner'].value_counts().head(10)
    fig_wins = px.bar(
        x=team_wins.values,
        y=team_wins.index,
        orientation='h',
        title="Top 10 Teams by Wins",
        labels={'x': 'Number of Wins', 'y': 'Team'},
        color=team_wins.values,
        color_continuous_scale='viridis'
    )
    fig_wins.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_wins, use_container_width=True)

with col2:
    # Win percentage by team
    team_matches = {}
    for team in all_teams:
        matches = len(filtered_df[(filtered_df['team1'] == team) | (filtered_df['team2'] == team)])
        wins = len(filtered_df[filtered_df['winner'] == team])
        if matches > 0:
            team_matches[team] = {
                'matches': matches,
                'wins': wins,
                'win_percentage': (wins / matches) * 100
            }
    
    win_pct_df = pd.DataFrame(team_matches).T.sort_values('win_percentage', ascending=False).head(10)
    fig_pct = px.bar(
        x=win_pct_df.index,
        y=win_pct_df['win_percentage'],
        title="Top 10 Teams by Win Percentage",
        labels={'x': 'Team', 'y': 'Win Percentage (%)'},
        color=win_pct_df['win_percentage'],
        color_continuous_scale='plasma'
    )
    fig_pct.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_pct, use_container_width=True)

# Toss Analysis
st.header("🎲 Toss Analysis")

col1, col2 = st.columns(2)

with col1:
    # Toss decision distribution
    toss_decision = filtered_df['toss_decision'].value_counts()
    fig_toss = px.pie(
        values=toss_decision.values,
        names=toss_decision.index,
        title="Toss Decision Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_toss.update_layout(height=400)
    st.plotly_chart(fig_toss, use_container_width=True)

with col2:
    # Toss winner vs Match winner
    toss_winner_match_winner = filtered_df[filtered_df['toss_winner'] == filtered_df['winner']]
    toss_impact = {
        'Toss Winner Won': len(toss_winner_match_winner),
        'Toss Winner Lost': len(filtered_df) - len(toss_winner_match_winner)
    }
    fig_impact = px.pie(
        values=list(toss_impact.values()),
        names=list(toss_impact.keys()),
        title="Toss Winner Impact on Match Result",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_impact.update_layout(height=400)
    st.plotly_chart(fig_impact, use_container_width=True)

# Match wins by decision (bat vs field)
st.subheader("🏆 Match Wins by Toss Decision")

col1, col2, col3 = st.columns(3)

# Calculate wins by decision
wins_by_decision = {'bat': 0, 'field': 0}
for _, row in filtered_df.iterrows():
    if row['toss_winner'] == row['winner']:
        # Winner won the toss, so they made the toss_decision
        decision = row['toss_decision'].lower()
        if decision in wins_by_decision:
            wins_by_decision[decision] += 1
    else:
        # Winner lost the toss, so they made the opposite decision
        opposite_decision = 'field' if row['toss_decision'].lower() == 'bat' else 'bat'
        if opposite_decision in wins_by_decision:
            wins_by_decision[opposite_decision] += 1

# Display metrics
with col1:
    st.metric("Wins Choosing to Bat", wins_by_decision['bat'])
with col2:
    total_wins = wins_by_decision['bat'] + wins_by_decision['field']
    bat_percentage = (wins_by_decision['bat'] / total_wins * 100) if total_wins > 0 else 0
    field_percentage = (wins_by_decision['field'] / total_wins * 100) if total_wins > 0 else 0
    st.metric("Wins Choosing to Field", wins_by_decision['field'])
with col3:
    st.metric("Total Matches", total_wins)

# Visualization
col1, col2 = st.columns(2)

with col1:
    # Pie chart
    fig_decision_wins = px.pie(
        values=list(wins_by_decision.values()),
        names=[f"Chose to {k.capitalize()}" for k in wins_by_decision.keys()],
        title="Match Wins by Toss Decision",
        color_discrete_sequence=['#FF6B6B', '#4ECDC4']
    )
    fig_decision_wins.update_layout(height=400)
    st.plotly_chart(fig_decision_wins, use_container_width=True)

with col2:
    # Bar chart with percentages
    decision_df = pd.DataFrame({
        'Decision': ['Chose to Bat', 'Chose to Field'],
        'Wins': [wins_by_decision['bat'], wins_by_decision['field']],
        'Percentage': [bat_percentage, field_percentage]
    })
    fig_decision_bar = px.bar(
        decision_df,
        x='Decision',
        y='Wins',
        text='Percentage',
        title="Match Wins by Toss Decision (with Win %)",
        labels={'Wins': 'Number of Wins', 'Decision': 'Toss Decision'},
        color='Wins',
        color_continuous_scale='Blues'
    )
    fig_decision_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_decision_bar.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_decision_bar, use_container_width=True)

# Venue Analysis
st.header("📍 Venue Analysis")

col1, col2 = st.columns(2)

with col1:
    # Top venues by matches
    venue_counts = filtered_df['venue'].value_counts().head(10)
    fig_venue = px.bar(
        x=venue_counts.index,
        y=venue_counts.values,
        title="Top 10 Venues by Number of Matches",
        labels={'x': 'Venue', 'y': 'Number of Matches'},
        color=venue_counts.values,
        color_continuous_scale='blues'
    )
    fig_venue.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_venue, use_container_width=True)

with col2:
    # Top cities by matches
    city_counts = filtered_df['city'].value_counts().head(10)
    fig_city = px.bar(
        x=city_counts.index,
        y=city_counts.values,
        title="Top 10 Cities by Number of Matches",
        labels={'x': 'City', 'y': 'Number of Matches'},
        color=city_counts.values,
        color_continuous_scale='greens'
    )
    fig_city.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_city, use_container_width=True)

# Time Series Analysis
st.header("📈 Matches Over Time")

matches_by_year = filtered_df.groupby('year').size().reset_index(name='matches')
fig_timeline = px.line(
    matches_by_year,
    x='year',
    y='matches',
    title="Number of Matches by Year",
    markers=True,
    labels={'year': 'Year', 'matches': 'Number of Matches'}
)
fig_timeline.update_traces(line_color='#1f77b4', line_width=3, marker_size=10)
fig_timeline.update_layout(height=400)
st.plotly_chart(fig_timeline, use_container_width=True)

# Player of the Match Analysis
st.header("⭐ Player of the Match Analysis")

col1, col2 = st.columns(2)

with col1:
    # Top players by POTM awards
    potm_counts = filtered_df['player_of_match'].value_counts().head(15)
    fig_potm = px.bar(
        x=potm_counts.values,
        y=potm_counts.index,
        orientation='h',
        title="Top 15 Players by Player of the Match Awards",
        labels={'x': 'Number of Awards', 'y': 'Player'},
        color=potm_counts.values,
        color_continuous_scale='sunset'
    )
    fig_potm.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig_potm, use_container_width=True)

with col2:
    # POTM distribution by team
    potm_by_team = filtered_df.groupby('winner')['player_of_match'].count().sort_values(ascending=False).head(10)
    fig_potm_team = px.bar(
        x=potm_by_team.index,
        y=potm_by_team.values,
        title="Top 10 Teams by Player of the Match Awards",
        labels={'x': 'Team', 'y': 'Number of Awards'},
        color=potm_by_team.values,
        color_continuous_scale='reds'
    )
    fig_potm_team.update_layout(showlegend=False, height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig_potm_team, use_container_width=True)

# Team Head-to-Head Analysis
st.header("⚔️ Team Head-to-Head Analysis")

col1, col2 = st.columns(2)

team1_select = col1.selectbox("Select Team 1", options=all_teams, key='team1_h2h')
team2_select = col2.selectbox("Select Team 2", options=all_teams, key='team2_h2h')

if team1_select and team2_select and team1_select != team2_select:
    h2h_matches = filtered_df[
        ((filtered_df['team1'] == team1_select) & (filtered_df['team2'] == team2_select)) |
        ((filtered_df['team1'] == team2_select) & (filtered_df['team2'] == team1_select))
    ]
    
    if len(h2h_matches) > 0:
        team1_wins = len(h2h_matches[h2h_matches['winner'] == team1_select])
        team2_wins = len(h2h_matches[h2h_matches['winner'] == team2_select])
        
        col1, col2, col3 = st.columns(3)
        col1.metric(f"{team1_select} Wins", team1_wins)
        col2.metric("Total Matches", len(h2h_matches))
        col3.metric(f"{team2_select} Wins", team2_wins)
        
        # H2H chart
        h2h_data = {
            team1_select: team1_wins,
            team2_select: team2_wins
        }
        fig_h2h = px.pie(
            values=list(h2h_data.values()),
            names=list(h2h_data.keys()),
            title=f"Head-to-Head: {team1_select} vs {team2_select}",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_h2h.update_layout(height=400)
        st.plotly_chart(fig_h2h, use_container_width=True)
    else:
        st.info(f"No matches found between {team1_select} and {team2_select} with the current filters.")

# Data Table
st.header("📋 Match Data")

# Show filtered data
st.dataframe(
    filtered_df[['match_number', 'team1', 'team2', 'match_date', 'venue', 'city', 'winner', 'player_of_match']].sort_values('match_date', ascending=False),
    use_container_width=True,
    height=400
)

# Download button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name=f"ipl_matches_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("**IPL Match Analysis Dashboard** | Data sourced from Match_Info.csv")
