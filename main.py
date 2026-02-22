import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="IPL Analytics Pro",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #f8fafc;
    }

    .custom-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 25px 30px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        margin-top: -30px;
    }
    .custom-header h1 {
        color: #f8fafc !important;
        margin: 0;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    .logo-card {
        background: white;
        padding: 10px 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.2s;
        border: 1px solid #e2e8f0;
    }
    .logo-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        border-color: #cbd5e1;
    }

    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    div[data-testid="metric-container"] label {
        color: #64748b !important;
        font-weight: 600;
        font-size: 15px;
    }
    div[data-testid="metric-container"] div {
        color: #0f172a !important;
        font-weight: 700;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        border-bottom: 3px solid #3b82f6;
        color: #3b82f6;
        font-weight: 600;
    }
    
    [data-testid="stPlotlyChart"], .stDataFrame {
        background-color: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

TEAM_LOGOS = {
    "Chennai Super Kings": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313421.logo.png",
    "Mumbai Indians": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313419.logo.png",
    "Royal Challengers Bangalore": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313418.logo.png",
    "Royal Challengers Bengaluru": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313418.logo.png",
    "Kolkata Knight Riders": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313411.logo.png",
    "Sunrisers Hyderabad": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313480.logo.png",
    "Rajasthan Royals": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313423.logo.png",
    "Delhi Capitals": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313422.logo.png",
    "Delhi Daredevils": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313422.logo.png",
    "Punjab Kings": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313412.logo.png",
    "Kings XI Punjab": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313412.logo.png",
    "Gujarat Titans": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/334700/334707.png",
    "Lucknow Super Giants": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/334700/334704.png",
    "Pune Warriors": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313490.logo.png",
    "Deccan Chargers": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313487.logo.png",
    "Gujarat Lions": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313482.logo.png",
    "Rising Pune Supergiant": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313481.logo.png",
    "Rising Pune Supergiants": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313481.logo.png",
    "Kochi Tuskers Kerala": "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_160,q_50/lsci/db/PICTURES/CMS/313400/313489.logo.png"
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

st.markdown("""
<div class="custom-header">
    <h1 style="font-size: 38px;">🏏 IPL Analytics Hub</h1>
</div>
""", unsafe_allow_html=True)

active_teams = [
    "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Sunrisers Hyderabad", "Rajasthan Royals",
    "Delhi Capitals", "Punjab Kings", "Gujarat Titans", "Lucknow Super Giants"
]

banner_html = "<div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 30px;'>"
for team in active_teams:
    if team in TEAM_LOGOS:
        banner_html += f"<div class='logo-card'><img src='{TEAM_LOGOS[team]}' height='55' title='{team}'></div>"
banner_html += "</div>"
st.markdown(banner_html, unsafe_allow_html=True)

with st.expander("Filter Data", expanded=True):
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

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Matches", f"{len(filtered_df):,}")
with col2: st.metric("Unique Teams", len(set(filtered_df['team1'].unique().tolist() + filtered_df['team2'].unique().tolist())))
with col3: st.metric("Stadiums Played", filtered_df['venue'].nunique())
with col4: st.metric("Total Cities", filtered_df['city'].nunique())
st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Performance Overview", "⚔️ Head-to-Head Clash", "📋 Raw Data"])

with tab1:
    row1_col1, row1_col2 = st.columns([1.5, 1])

    with row1_col1:
        st.markdown("<h4 style='color: #0f172a;'>Matches Won by Team</h4>", unsafe_allow_html=True)
        team_wins = filtered_df['winner'].value_counts().head(8).reset_index()
        team_wins.columns = ['Team', 'Wins']
        fig_wins = px.bar(team_wins, x='Team', y='Wins', color_discrete_sequence=['#3b82f6'])
        fig_wins.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Plus Jakarta Sans", color="#333"))
        st.plotly_chart(fig_wins, use_container_width=True)

    with row1_col2:
        st.markdown("<h4 style='color: #0f172a;'>Toss Decisions</h4>", unsafe_allow_html=True)
        toss_decision = filtered_df['toss_decision'].value_counts().reset_index()
        toss_decision.columns = ['Decision', 'Count']
        fig_toss = px.pie(toss_decision, names='Decision', values='Count', hole=0.5, color_discrete_sequence=['#0ea5e9', '#6366f1'])
        fig_toss.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Plus Jakarta Sans", color="#333"), legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_toss, use_container_width=True)

    row2_col1, row2_col2 = st.columns([1, 1.5])

    with row2_col1:
        st.markdown("<h4 style='color: #0f172a;'>Toss Strategy Impact</h4>", unsafe_allow_html=True)
        wins_by_decision = {'Bat First': 0, 'Field First': 0}
        for _, row in filtered_df.iterrows():
            if row['toss_winner'] == row['winner']:
                decision = 'Bat First' if str(row['toss_decision']).lower() == 'bat' else 'Field First'
                wins_by_decision[decision] += 1
            else:
                opposite = 'Field First' if str(row['toss_decision']).lower() == 'bat' else 'Bat First'
                wins_by_decision[opposite] += 1
                
        decision_df = pd.DataFrame({'Strategy': list(wins_by_decision.keys()), 'Matches Won': list(wins_by_decision.values())})
        fig_toss_win = px.bar(decision_df, x='Strategy', y='Matches Won', color_discrete_sequence=['#1e293b'])
        fig_toss_win.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Plus Jakarta Sans", color="#333"))
        st.plotly_chart(fig_toss_win, use_container_width=True)

    with row2_col2:
        st.markdown("<h4 style='color: #0f172a;'>Recent Match Results</h4>", unsafe_allow_html=True)
        display_df = filtered_df[['match_date', 'team1', 'team2', 'winner', 'player_of_match']].copy()
        display_df['match_date'] = display_df['match_date'].dt.strftime('%Y-%m-%d')
        display_df = display_df.sort_values('match_date', ascending=False).head(10)
        display_df.columns = ['Date', 'Team 1', 'Team 2', 'Winner', 'Player of Match']
        st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("<h4 style='color: #0f172a;'>Head-to-Head Comparison</h4>", unsafe_allow_html=True)
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
                st.markdown(f"<h3 style='text-align: center; color: #1e293b;'>{team1_wins} Wins</h3>", unsafe_allow_html=True)
                
            with logo_col2:
                st.markdown("<h4 style='text-align: center; color: #64748b; margin-top: 25px;'>Total Matches</h4>", unsafe_allow_html=True)
                st.markdown(f"<h1 style='text-align: center; font-size: 3.5rem; color: #0f172a;'>{len(h2h_matches)}</h1>", unsafe_allow_html=True)
                
            with logo_col3:
                st.markdown(f"<div style='text-align: center;'><img src='{TEAM_LOGOS.get(team2_select, '')}' width='120'></div>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center; color: #1e293b;'>{team2_wins} Wins</h3>", unsafe_allow_html=True)
        else:
            st.info("No matches found between these teams in the selected filter range.")

with tab3:
    st.markdown("<h4 style='color: #0f172a;'>Complete Dataset</h4>", unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="📥 Download Dataset", data=csv, file_name=f"ipl_dataset.csv", mime="text/csv")
