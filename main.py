import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="IPL Match Analysis", page_icon="🏏", layout="wide")

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

# --- HEADER ---
st.title("🏏 IPL Match Analysis Dashboard")
st.markdown("A focused look at Team Dominance, Toss Strategy, Star Players, and Historical Trends.")
st.markdown("---")

# --- DASHBOARD LAYOUT ---
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# PLOT 1: Team Win Percentage
with row1_col1:
    st.subheader("1. Highest Win Percentage")
    all_teams = set(df['team1'].unique().tolist() + df['team2'].unique().tolist())
    team_matches = {}
    for team in all_teams:
        matches = len(df[(df['team1'] == team) | (df['team2'] == team)])
        wins = len(df[df['winner'] == team])
        if matches > 20: # Filter out temporary teams with few matches
            team_matches[team] = {'win_percentage': (wins / matches) * 100}
            
    win_pct_df = pd.DataFrame(team_matches).T.sort_values('win_percentage', ascending=False).head(10)
    fig1 = px.bar(win_pct_df, y='win_percentage', title="Top 10 Teams by Win % (Min 20 Matches)", 
                  labels={'index': 'Team', 'win_percentage': 'Win %'}, color='win_percentage', color_continuous_scale='plasma')
    st.plotly_chart(fig1, use_container_width=True)

# PLOT 2: Toss Strategy
with row1_col2:
    st.subheader("2. Toss Decision Impact")
    wins_by_decision = {'bat': 0, 'field': 0}
    for _, row in df.iterrows():
        if row['toss_winner'] == row['winner']:
            decision = str(row['toss_decision']).lower()
            if decision in wins_by_decision: wins_by_decision[decision] += 1
        else:
            opposite_decision = 'field' if str(row['toss_decision']).lower() == 'bat' else 'bat'
            if opposite_decision in wins_by_decision: wins_by_decision[opposite_decision] += 1
            
    decision_df = pd.DataFrame({'Decision': ['Chose to Field', 'Chose to Bat'], 'Wins': [wins_by_decision['field'], wins_by_decision['bat']]})
    fig2 = px.bar(decision_df, x='Decision', y='Wins', title="Match Wins based on Toss Decision", 
                  color='Decision', color_discrete_sequence=['#4ECDC4', '#FF6B6B'])
    st.plotly_chart(fig2, use_container_width=True)

# PLOT 3: Top Players
with row2_col1:
    st.subheader("3. Biggest Match Winners")
    potm_counts = df['player_of_match'].value_counts().head(10)
    fig3 = px.bar(x=potm_counts.values, y=potm_counts.index, orientation='h', 
                  title="Top 10 Player of the Match Awards", labels={'x': 'Awards', 'y': 'Player'}, color=potm_counts.values)
    fig3.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

# PLOT 4: Matches over time
with row2_col2:
    st.subheader("4. IPL Growth Over Time")
    matches_by_year = df.groupby('year').size().reset_index(name='matches')
    fig4 = px.line(matches_by_year, x='year', y='matches', title="Number of Matches per Season", markers=True)
    fig4.update_traces(line_color='#1f77b4', line_width=3, marker_size=8)
    st.plotly_chart(fig4, use_container_width=True)
