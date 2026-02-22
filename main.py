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
        flex-wrap: wrap;
        justify-content: center;
    }

    .ipl-logo-glow {
        width: 75px;
        filter: brightness(0) invert(1) drop-shadow(0 0 5px rgba(255,255,255,0.6));
    }

    .glow-text {
        color: #FFFFFF !important;
        margin: 0;
        font-size: clamp(24px, 4vw, 36px);
        font-weight: 800;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(255,255,255,0.7);
        text-align: center;
    }

    .logo-banner {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 30px;
    }

    .logo-card {
        background: white;
        border-radius: 12px;
        padding: 10px 15px;
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
        height: clamp(35px, 5vw, 55px);
        object-fit: contain;
    }

    [data-testid="stPlotlyChart"], .stDataFrame {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        width: 100%;
        overflow-x: auto;
    }

    .stTabs [data-baseweb="tab-list"] { 
        gap: 10px; 
        padding-bottom: 10px;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] { 
        border-radius: 8px; 
        background-color: #fff; 
        border: 1px solid #e2e8f0; 
        padding: 8px 16px;
        margin-bottom: 5px;
        font-size: clamp(12px, 3vw, 16px);
    }
    
    .stTabs [aria-selected="true"] { 
        background-color: #ebf8ff; 
        border-color: #3b82f6; 
        color: #1e40af; 
        font-weight: 600; 
        border-bottom: 3px solid #3b82f6 !important;
    }

    .kpi-wrapper {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
        margin-bottom: 10px;
        align-items: center;
        text-align: center;
    }
    
    .kpi-wrapper:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }
    
    .kpi-title {
        color: #64748b;
        font-size: clamp(11px, 2vw, 14px);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        color: #0f172a;
        font-size: clamp(24px, 5vw, 36px);
        font-weight: 800;
        line-height: 1.2;
    }
    
    .kpi-icon {
        font-size: clamp(20px, 4vw, 28px);
        margin-bottom: 8px;
    }
    
    @media (max-width: 768px) {
        .glow-header-container {
            padding: 15px;
            gap: 15px;
        }
        .ipl-logo-glow {
            width: 50px;
        }
        .logo-card {
            padding: 8px 10px;
        }
    }
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
            ext = path_or_url.split(".")[-1].lower()
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

banner_html = '<div class="logo-banner">'
for team in active_teams:
    logo_path = TEAM_LOGOS.get(team, "")
    if logo_path:
        img_src = get_image_base64(logo_path)
        banner_html += f'<div class="logo-card"><img src="{img_src}" title="{team}" alt="{team}"></div>'
banner_html += "</div>"
st.markdown(banner_html, unsafe_allow_html=True)

with st.expander("Dashboard Filters", expanded=True):
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
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

st.markdown("<br>", unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4 = st.columns([1, 1, 1, 1])

total_matches = len(filtered_df)
total_teams = len(set(filtered_df['team1'].unique().tolist() + filtered_df['team2'].unique().tolist()))
total_venues = filtered_df['venue'].nunique()
total_cities = filtered_df['city'].nunique()

with kpi1:
    st.markdown(f'''
        <div class="kpi-wrapper">
            <div class="kpi-icon">🏏</div>
            <div class="kpi-title">Matches</div>
            <div class="kpi-value">{total_matches:,}</div>
        </div>
    ''', unsafe_allow_html=True)
    
with kpi2:
    st.markdown(f'''
        <div class="kpi-wrapper">
            <div class="kpi-icon">🛡️</div>
            <div class="kpi-title">Teams</div>
            <div class="kpi-value">{total_teams}</div>
        </div>
    ''', unsafe_allow_html=True)
    
with kpi3:
    st.markdown(f'''
        <div class="kpi-wrapper">
            <div class="kpi-icon">🏟️</div>
            <div class="kpi-title">Venues</div>
            <div class="kpi-value">{total_venues}</div>
        </div>
    ''', unsafe_allow_html=True)
    
with kpi4:
    st.markdown(f'''
        <div class="kpi-wrapper">
            <div class="kpi-icon">🏙️</div>
            <div class="kpi-title">Cities</div>
            <div class="kpi-value">{total_cities}</div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Performance Analysis", "Head-to-Head", "Raw Dataset", "Advanced Insights"])

with tab1:
    row1_col1, row1_col2 = st.columns([1, 1])
    with row1_col1:
        st.markdown("### Team Win Count")
        team_wins = filtered_df['winner'].value_counts().head(10).reset_index()
        team_wins.columns = ['Team', 'Wins']
        fig_wins = px.bar(team_wins, x='Team', y='Wins', color='Wins', color_continuous_scale='Blues')
        fig_wins.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Inter", color="#333"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_wins, use_container_width=True)
    with row1_col2:
        st.markdown("### Toss Decision Trends")
        toss_decision = filtered_df['toss_decision'].value_counts().reset_index()
        toss_decision.columns = ['Decision', 'Count']
        fig_toss = px.pie(toss_decision, names='Decision', values='Count', hole=0.5, color_discrete_sequence=['#2563eb', '#7c3aed'])
        fig_toss.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Inter", color="#333"), legend=dict(orientation="h", y=-0.2), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_toss, use_container_width=True)

    row2_col1, row2_col2 = st.columns([1, 1])
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
        fig_toss_win.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Inter", color="#333"), showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
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
    h2h_col1, h2h_col2 = st.columns([1, 1])
    team1_select = h2h_col1.selectbox("Select Team 1", options=all_teams, index=all_teams.index('Chennai Super Kings') if 'Chennai Super Kings' in all_teams else 0)
    team2_select = h2h_col2.selectbox("Select Team 2", options=all_teams, index=all_teams.index('Mumbai Indians') if 'Mumbai Indians' in all_teams else 1)

    if team1_select and team2_select and team1_select != team2_select:
        h2h_matches = filtered_df[
            ((filtered_df['team1'] == team1_select) & (filtered_df['team2'] == team2_select)) |
            ((filtered_df['team1'] == team2_select) & (filtered_df['team2'] == team1_select))
        ]
        
        team1_wins = len(h2h_matches[h2h_matches['winner'] == team1_select])
        team2_wins = len(h2h_matches[h2h_matches['winner'] == team2_select])
        total_matches = len(h2h_matches)

        logo1 = TEAM_LOGOS.get(team1_select, "")
        logo2 = TEAM_LOGOS.get(team2_select, "")
        
        img_src1 = get_image_base64(logo1)
        img_src2 = get_image_base64(logo2)

        logo_col1, logo_col2, logo_col3 = st.columns([1, 1, 1])
        with logo_col1:
            st.markdown(f"<div style='text-align: center; padding: 10px;'><img src='{img_src1}' style='width: 100%; max-width: 130px; object-fit: contain;'></div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: #1e40af; margin: 0; font-size: clamp(1.5rem, 4vw, 2rem);'>{team1_wins} Wins</h2>", unsafe_allow_html=True)
        with logo_col2:
            st.markdown("<h4 style='text-align: center; color: #64748b; margin-top: 20px; margin-bottom: 5px; font-size: clamp(1rem, 3vw, 1.5rem);'>Encounters</h4>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; font-size: clamp(2.5rem, 8vw, 4rem); color: #0f172a; margin: 0;'>{total_matches}</h1>", unsafe_allow_html=True)
            if total_matches == 0:
                st.markdown("<p style='text-align: center; color: #dc2626; font-weight: 500; margin-top: 15px; font-size: clamp(0.8rem, 2vw, 1rem);'>No matches found.</p>", unsafe_allow_html=True)
        with logo_col3:
            st.markdown(f"<div style='text-align: center; padding: 10px;'><img src='{img_src2}' style='width: 100%; max-width: 130px; object-fit: contain;'></div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: #1e40af; margin: 0; font-size: clamp(1.5rem, 4vw, 2rem);'>{team2_wins} Wins</h2>", unsafe_allow_html=True)

with tab3:
    st.markdown("### Full Match Database")
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Download as CSV", data=csv, file_name="ipl_analysis_data.csv", mime="text/csv")

with tab4:
    adv_col1, adv_col2 = st.columns([1, 1])
    with adv_col1:
        st.markdown("### Match Frequency Over Time")
        matches_by_year = filtered_df.groupby('year').size().reset_index(name='matches')
        fig_timeline = px.line(matches_by_year, x='year', y='matches', markers=True, color_discrete_sequence=['#1e40af'])
        fig_timeline.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Inter", color="#333"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_timeline, use_container_width=True)

        st.markdown("### Most Active Venues")
        top_venues = filtered_df['venue'].value_counts().head(8).reset_index()
        top_venues.columns = ['Venue', 'Matches']
        fig_venues = px.bar(top_venues, x='Matches', y='Venue', orientation='h', color='Matches', color_continuous_scale='Blues')
        fig_venues.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Inter", color="#333"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_venues, use_container_width=True)

    with adv_col2:
        st.markdown("### Top Star Performers (POTM)")
        top_players = filtered_df['player_of_match'].value_counts().head(8).reset_index()
        top_players.columns = ['Player', 'Awards']
        fig_players = px.bar(top_players, x='Awards', y='Player', orientation='h', color='Awards', color_continuous_scale='Purples')
        fig_players.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Inter", color="#333"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_players, use_container_width=True)

        st.markdown("### Toss & Match Win Correlation")
        toss_match_wins = filtered_df[filtered_df['toss_winner'] == filtered_df['winner']]['winner'].value_counts().head(8).reset_index()
        toss_match_wins.columns = ['Team', 'Wins']
        fig_toss_team = px.bar(toss_match_wins, x='Team', y='Wins', color_discrete_sequence=['#7c3aed'])
        fig_toss_team.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Inter", color="#333"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_toss_team, use_container_width=True)
