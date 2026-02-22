import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IPL Analytics Hub",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #f4f7f9;
    }

    /* GLOWING HEADER */
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

    /* LOGO BANNER */
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

    /* CARDS & TABS */
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

# --- OFFICIAL & STABLE TEAM LOGOS ---
TEAM_LOGOS = {
    "Chennai Super Kings": "https://www.iplt20.com/assets/images/teams-new-look/csk.png",
    "Mumbai Indians": "https://www.iplt20.com/assets/images/teams-new-look/mi.png",
    "Royal Challengers Bangalore": "https://www.iplt20.com/assets/images/teams-new-look/rcb.png",
    "Royal Challengers Bengaluru": "https://www.iplt20.com/assets/images/teams-new-look/rcb.png",
    "Kolkata Knight Riders": "https://www.iplt20.com/assets/images/teams-new-look/kkr.png",
    "Sunrisers Hyderabad": "https://www.iplt20.com/assets/images/teams-new-look/srh.png",
    "Rajasthan Royals": "https://www.iplt20.com/assets/images/teams-new-look/rr.png",
    "Delhi Capitals": "https://www.iplt20.com/assets/images/teams-new-look/dc.png",
    "Delhi Daredevils": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Delhi_Daredevils_Logo.svg/1200px-Delhi_Daredevils_Logo.svg.png",
    "Punjab Kings": "https://www.iplt20.com/assets/images/teams-new-look/pbks.png",
    "Kings XI Punjab": "https://upload.wikimedia.org/wikipedia/en/thumb/0/06/Kings_XI_Punjab_Logo_2019.svg/1200px-Kings_XI_Punjab_Logo_2019.svg.png",
    "Gujarat Titans": "https://www.iplt20.com/assets/images/teams-new-look/gt.png",
    "Lucknow Super Giants": "https://www.iplt20.com/assets/images/teams-new-look/lsg.png",
    "Pune Warriors": "https://upload.wikimedia.org/wikipedia/en/thumb/1/18/Pune_Warriors_India_logo.svg/200px-Pune_Warriors_India_logo.svg.png",
    "Deccan Chargers": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/Deccan_Chargers_Logo.svg/200px-Deccan_Chargers_Logo.svg.png",
    "Gujarat Lions": "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Gujarat_Lions_Logo.svg/200px-Gujarat_Lions_Logo.svg.png",
    "Rising Pune Supergiant": "https://upload.wikimedia.org/wikipedia/en/thumb/0/02/Rising_Pune_Supergiants_Logo.svg/200px-Rising_Pune_Supergiants_Logo.svg.png",
    "Rising Pune Supergiants": "https://upload.wikimedia.org/wikipedia/en/thumb/0/02/Rising_Pune_Supergiants_Logo.svg/200px-Rising_Pune_Supergiants_Logo.svg.png",
    "Kochi Tuskers Kerala": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Kochi_Tuskers_Kerala_Logo.svg/200px-Kochi_Tuskers_Kerala_Logo.svg.png"
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

# --- HEADER ---
st.markdown("""
    <div class="glow-header-container">
        <img src="https://www.iplt20.com/assets/images/ipl-logo-new-old.png" class="ipl-logo-glow" alt="IPL Logo">
        <h1 class="glow-text">IPL Analytics Hub</h1>
    </div>
""", unsafe_allow_html=True)

# --- LOGO BANNER ---
active_teams = [
    "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Sunrisers Hyderabad", "Rajasthan Royals",
    "Delhi Capitals", "Punjab Kings", "Gujarat Titans", "Lucknow Super Giants"
]

banner_html = '<div class="logo-banner">'
for team in active_teams:
    logo_url = TEAM_LOGOS.get(team, "")
    if logo_url:
        banner_html += f'<div class="logo-card"><img src="{logo_url}" title="{team}" alt="{team}"></div>'
banner_html += "</div>"
st.markdown(banner_html, unsafe_allow_html=True)

# --- FILTERS ---
with st.expander("Dashboard Filters", expanded=True):
    col_f1, col_f2, col_f3 = st.columns(3)
    years = sorted(df['year'].dropna().unique(), reverse=True)
    all_teams = sorted(set(df['team1'].unique().tolist() + df['team2'].unique().tolist()))
    all_venues = sorted(df['venue'].dropna().unique())

    with col_f1: selected_years = st.multiselect("Select Year(s)", options=years, default=years[:5] if len(years) >= 5 else years)
    with col_f2: selected_teams = st.multiselect("Select Team(s)", options=all_teams, default=all_teams)
    with col_f3: selected_venues = st.multiselect("Select Venue(s)", options=all_venues, default=all_venues)

filtered_df = df[
    (df['year'].isin(selected_years) if selected_years else True) &
    ((df['team1'].isin(selected_teams)) | (df['team2'].isin(selected_teams)) if selected_teams else True) &
    (df['venue'].isin(selected_venues) if selected_venues else True)
].copy()

# --- METRICS ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Matches Played", f"{len(filtered_df):,}")
with col2: st.metric("Teams Involved", len(set(filtered_df['team1'].unique().tolist() + filtered_df['team2'].unique().tolist())))
with col3: st.metric("Unique Venues", filtered_df['venue'].nunique())
with col4: st.metric("Host Cities", filtered_df['city'].nunique())
st.markdown("<br>", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["Performance Analysis", "Head-to-Head", "Raw Dataset"])

with tab1:
    row1_col1, row1_col2 = st.columns([1.5, 1])
    with row1_col1:
        st.markdown("### Team Win Count")
        team_wins = filtered_df['winner'].value_counts().head(10).reset_index()
        team_wins.columns = ['Team', 'Wins']
        fig_wins = px.bar(team_wins, x='Team', y='Wins', color='Wins', color_continuous_scale='Blues')
        fig_wins.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Inter", color="#333"))
        st.plotly_chart(fig_wins, use_container_width=True)
    with row1_col2:
        st.markdown("### Toss Decision Trends")
        toss_decision = filtered_df['toss_decision'].value_counts().reset_index()
        toss_decision.columns = ['Decision', 'Count']
        fig_toss = px.pie(toss_decision, names='Decision', values='Count', hole=0.5, color_discrete_sequence=['#2563eb', '#7c3aed'])
        fig_toss.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Inter", color="#333"), legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_toss, use_container_width=True)

    row2_col1, row2_col2 = st.columns([1, 1.5])
    with row2_col1:
        st.markdown("### Bat/Field Win Strategy")
        wins_by_decision = {'Bat First': 0, 'Field First': 0}
        for _, row in filtered_df.iterrows():
            if row['toss_winner'] == row['winner']:
                decision = 'Bat First' if str(row['toss_decision']).lower() == 'bat' else 'Field First'
                wins_by_decision[decision] += 1
            else:
                opposite = 'Field First' if str(row['toss_decision']).lower() == 'bat' else 'Bat First'
                wins_by_decision[opposite] += 1
        decision_df = pd.DataFrame({'Strategy': list(wins_by_decision.keys()), 'Matches Won': list(wins_by_decision.values())})
        fig_toss_win = px.bar(decision_df, x='Strategy', y='Matches Won', color='Strategy', color_discrete_sequence=['#1e40af', '#3b82f6'])
        fig_toss_win.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Inter", color="#333"), showlegend=False)
        st.plotly_chart(fig_toss_win, use_container_width=True)
    with row2_col2:
        st.markdown("### Recent Match Log")
        display_df = filtered_df[['match_date', 'team1', 'team2', 'winner', 'player_of_match']].copy()
        display_df['match_date'] = display_df['match_date'].dt.strftime('%Y-%m-%d')
        display_df = display_df.sort_values('match_date', ascending=False).head(10)
        display_df.columns = ['Date', 'Team 1', 'Team 2', 'Winner', 'Player of Match']
        st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("### Compare Teams")
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

            logo1 = TEAM_LOGOS.get(team1_select, "")
            logo2 = TEAM_LOGOS.get(team2_select, "")

            logo_col1, logo_col2, logo_col3 = st.columns([1, 1, 1])
            with logo_col1:
                st.markdown(f"<div style='text-align: center; padding: 20px;'><img src='{logo1}' width='130'></div>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center; color: #1e40af; margin: 0;'>{team1_wins} Wins</h2>", unsafe_allow_html=True)
            with logo_col2:
                st.markdown("<h4 style='text-align: center; color: #64748b; margin-top: 40px; margin-bottom: 5px;'>Total Encounters</h4>", unsafe_allow_html=True)
                st.markdown(f"<h1 style='text-align: center; font-size: 4rem; color: #0f172a; margin: 0;'>{len(h2h_matches)}</h1>", unsafe_allow_html=True)
            with logo_col3:
                st.markdown(f"<div style='text-align: center; padding: 20px;'><img src='{logo2}' width='130'></div>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center; color: #1e40af; margin: 0;'>{team2_wins} Wins</h2>", unsafe_allow_html=True)
        else:
            st.info("No matches found between these teams in the selected filter range.")

with tab3:
    st.markdown("### Full Match Database")
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Download as CSV", data=csv, file_name="ipl_analysis_data.csv", mime="text/csv")
