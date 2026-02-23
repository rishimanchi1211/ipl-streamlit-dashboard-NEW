import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

st.set_page_config(page_title="IPL Analytics Hub", page_icon="🏏", layout="wide", initial_sidebar_state="collapsed")

# --- COMPRESSED CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; background-color: #f4f7fa; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Outfit', sans-serif !important; }
    .glow-header-container { background: linear-gradient(135deg, #0A1A3C 0%, #1B3A6B 100%); padding: 25px 35px; border-radius: 20px; display: flex; align-items: center; justify-content: center; gap: 25px; box-shadow: 0 10px 30px -5px rgba(27, 58, 107, 0.4), inset 0 0 10px rgba(255,255,255,0.1); margin-bottom: 30px; margin-top: -10px; border: 1px solid #2c4a7c; flex-wrap: wrap; }
    .ipl-logo-glow { width: 70px; filter: brightness(0) invert(1) drop-shadow(0 0 8px rgba(255,255,255,0.5)); }
    .glow-text { color: #FFFFFF !important; margin: 0; font-size: clamp(28px, 5vw, 42px); font-weight: 800; letter-spacing: 1px; text-shadow: 0 0 15px rgba(255,255,255,0.5); text-align: center; }
    .objective-wrapper { display: flex; justify-content: center; width: 100%; margin-bottom: 40px; }
    .analytical-objective { background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%); border-radius: 24px; padding: 35px 45px; max-width: 900px; box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.08); border: 1px solid rgba(226, 232, 240, 0.8); text-align: center; position: relative; transition: transform 0.3s ease; }
    .analytical-objective:hover { transform: translateY(-3px); box-shadow: 0 25px 50px -15px rgba(15, 23, 42, 0.12); }
    .obj-title { font-family: 'Outfit', sans-serif; font-size: clamp(20px, 3vw, 26px); font-weight: 800; text-transform: uppercase; letter-spacing: 1px; background: linear-gradient(90deg, #2563eb, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 15px; display: flex; align-items: center; justify-content: center; gap: 12px; }
    .obj-text { color: #475569; font-size: clamp(15px, 2.5vw, 17px); line-height: 1.8; font-weight: 500; }
    .insight-card { background: #ffffff; border-radius: 20px; padding: 25px 30px; margin-top: 30px; margin-bottom: 15px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04); border: 1px solid #f1f5f9; display: flex; gap: 20px; align-items: flex-start; transition: all 0.4s ease; }
    .insight-card:hover { transform: translateY(-5px) scale(1.01); box-shadow: 0 20px 35px -10px rgba(139, 92, 246, 0.15); border-color: #ddd6fe; }
    .insight-icon { background: linear-gradient(135deg, #8b5cf6, #3b82f6); color: white; min-width: 50px; height: 50px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 8px 16px -6px rgba(139, 92, 246, 0.6); flex-shrink: 0; }
    .insight-content { color: #334155; font-size: clamp(14px, 2.5vw, 15px); line-height: 1.7; }
    .insight-title { font-family: 'Outfit', sans-serif; font-weight: 800; color: #0f172a; font-size: 19px; margin-bottom: 8px; display: block; letter-spacing: 0.5px; }
    .logo-banner { display: flex; justify-content: center; flex-wrap: wrap; gap: 15px; margin-bottom: 35px; }
    .logo-card { background: white; border-radius: 14px; padding: 10px 18px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; transition: all 0.3s ease; display: flex; align-items: center; justify-content: center; }
    .logo-card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0,0,0,0.08); border-color: #3b82f6; }
    .logo-card img { height: clamp(35px, 5vw, 55px); object-fit: contain; }
    [data-testid="stPlotlyChart"], .stDataFrame { background-color: white; border-radius: 16px; padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; width: 100%; overflow-x: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 12px; padding-bottom: 15px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { border-radius: 10px; background-color: #fff; border: 1px solid #e2e8f0; padding: 10px 20px; margin-bottom: 5px; font-size: clamp(13px, 3vw, 16px); font-family: 'Outfit', sans-serif; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #eff6ff; border-color: #3b82f6; color: #1e40af; border-bottom: 3px solid #2563eb !important; }
    .kpi-wrapper { background-color: white; border-radius: 16px; padding: 24px; box-shadow: 0 6px 15px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; display: flex; flex-direction: column; transition: all 0.3s ease; margin-bottom: 15px; align-items: center; text-align: center; }
    .kpi-wrapper:hover { transform: translateY(-4px); box-shadow: 0 15px 25px rgba(0,0,0,0.08); border-color: #3b82f6; }
    .kpi-title { color: #64748b; font-size: clamp(12px, 2vw, 14px); font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .kpi-value { color: #0f172a; font-family: 'Outfit', sans-serif; font-size: clamp(28px, 5vw, 40px); font-weight: 800; line-height: 1.2; }
    .kpi-icon { font-size: clamp(24px, 4vw, 32px); margin-bottom: 10px; }
    @media (max-width: 768px) { .glow-header-container { padding: 20px; gap: 15px; } .ipl-logo-glow { width: 55px; } .analytical-objective { padding: 25px 20px; border-radius: 16px; } .insight-card { flex-direction: column; align-items: center; text-align: center; padding: 20px; gap: 15px; } }
    </style>
""", unsafe_allow_html=True)

def get_image_base64(path_or_url):
    if not path_or_url: return ""
    if path_or_url.startswith("http"): return path_or_url
    if os.path.isfile(path_or_url):
        with open(path_or_url, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            ext = path_or_url.split(".")[-1].lower()
            return f"data:image/{'jpeg' if ext in ['jpg', 'jpeg'] else ext};base64,{encoded}"
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
    df['team1'], df['team2'], df['winner'] = df['team1'].str.strip(), df['team2'].str.strip(), df['winner'].str.strip()
    return df[df['result'] == 'Win'].copy()

df = load_data()

st.markdown('''
    <div class="glow-header-container">
        <img src="https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Indian_Premier_League_Official_Logo.svg/200px-Indian_Premier_League_Official_Logo.svg.png" class="ipl-logo-glow" alt="IPL Logo">
        <h1 class="glow-text">IPL Analytics Hub</h1>
    </div>
    <div class="objective-wrapper">
        <div class="analytical-objective">
            <div class="obj-title"><span>🎯</span> Analytical Objective</div>
            <div class="obj-text">This interactive dashboard evaluates historical IPL franchise performance, analyzes the statistical impact of toss decisions on match outcomes, and visualizes head-to-head match records to uncover strategic trends across different venues and seasons.</div>
        </div>
    </div>
''', unsafe_allow_html=True)

active_teams = ["Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore", "Kolkata Knight Riders", "Sunrisers Hyderabad", "Rajasthan Royals", "Delhi Capitals", "Punjab Kings", "Gujarat Titans", "Lucknow Super Giants"]
banner_html = '<div class="logo-banner">' + "".join([f'<div class="logo-card"><img src="{get_image_base64(TEAM_LOGOS.get(t, ""))}" title="{t}" alt="{t}"></div>' for t in active_teams if TEAM_LOGOS.get(t, "")]) + "</div>"
st.markdown(banner_html, unsafe_allow_html=True)

with st.expander("⚙️ Dashboard Filters", expanded=True):
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    years = sorted(df['year'].dropna().unique(), reverse=True)
    all_teams = sorted(set(df['team1'].unique().tolist() + df['team2'].unique().tolist()))
    all_venues = sorted(df['venue'].dropna().unique())

    with col_f1: selected_years = st.multiselect("Select Year(s)", options=years, default=years[:5] if len(years) >= 5 else years)
    with col_f2: selected_teams = st.multiselect("Select Team(s)", options=all_teams, default=all_teams)
    with col_f3: selected_venues = st.multiselect("Select Venue(s)", options=all_venues, default=all_venues)

filtered_df = df[(df['year'].isin(selected_years) if selected_years else True) & ((df['team1'].isin(selected_teams)) | (df['team2'].isin(selected_teams)) if selected_teams else True) & (df['venue'].isin(selected_venues) if selected_venues else True)].copy()

st.markdown("<br>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns([1, 1, 1, 1])

with kpi1: st.markdown(f'<div class="kpi-wrapper"><div class="kpi-icon">🏏</div><div class="kpi-title">Matches</div><div class="kpi-value">{len(filtered_df):,}</div></div>', unsafe_allow_html=True)
with kpi2: st.markdown(f'<div class="kpi-wrapper"><div class="kpi-icon">🛡️</div><div class="kpi-title">Teams</div><div class="kpi-value">{len(set(filtered_df["team1"].unique().tolist() + filtered_df["team2"].unique().tolist()))}</div></div>', unsafe_allow_html=True)
with kpi3: st.markdown(f'<div class="kpi-wrapper"><div class="kpi-icon">🏟️</div><div class="kpi-title">Venues</div><div class="kpi-value">{filtered_df["venue"].nunique()}</div></div>', unsafe_allow_html=True)
with kpi4: st.markdown(f'<div class="kpi-wrapper"><div class="kpi-icon">🏙️</div><div class="kpi-title">Cities</div><div class="kpi-value">{filtered_df["city"].nunique()}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance Analysis", "⚔️ Head-to-Head", "📋 Raw Dataset", "🔬 Advanced Insights"])

with tab1:
    row1_col1, row1_col2 = st.columns([1, 1])
    with row1_col1:
        st.markdown("### Team Win Count")
        team_wins = filtered_df['winner'].value_counts().head(10).reset_index()
        team_wins.columns = ['Team', 'Wins']
        fig_wins = px.bar(team_wins, x='Team', y='Wins', color='Wins', color_continuous_scale='Blues')
        fig_wins.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Plus Jakarta Sans", color="#334155"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_wins, use_container_width=True)
    with row1_col2:
        st.markdown("### Toss Decision Trends")
        toss_decision = filtered_df['toss_decision'].value_counts().reset_index()
        toss_decision.columns = ['Decision', 'Count']
        fig_toss = px.pie(toss_decision, names='Decision', values='Count', hole=0.5, color_discrete_sequence=['#2563eb', '#8b5cf6'])
        fig_toss.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Plus Jakarta Sans", color="#334155"), legend=dict(orientation="h", y=-0.2), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_toss, use_container_width=True)

    row2_col1, row2_col2 = st.columns([1, 1])
    with row2_col1:
        st.markdown("### Bat/Field Win Strategy")
        wins_by_decision = {'Bat First': 0, 'Field First': 0}
        for _, row in filtered_df.iterrows():
            if row['toss_winner'] == row['winner']: wins_by_decision['Bat First' if str(row['toss_decision']).lower() == 'bat' else 'Field First'] += 1
            else: wins_by_decision['Field First' if str(row['toss_decision']).lower() == 'bat' else 'Bat First'] += 1
        decision_df = pd.DataFrame({'Strategy': list(wins_by_decision.keys()), 'Matches Won': list(wins_by_decision.values())})
        fig_toss_win = px.bar(decision_df, x='Strategy', y='Matches Won', color='Strategy', color_discrete_sequence=['#1e40af', '#3b82f6'])
        fig_toss_win.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Plus Jakarta Sans", color="#334155"), showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_toss_win, use_container_width=True)
    with row2_col2:
        st.markdown("### Recent Match Log")
        display_df = filtered_df[['match_date', 'team1', 'team2', 'winner', 'player_of_match']].copy()
        display_df['match_date'] = display_df['match_date'].dt.strftime('%Y-%m-%d')
        display_df = display_df.sort_values('match_date', ascending=False).head(10)
        display_df.columns = ['Date', 'Team 1', 'Team 2', 'Winner', 'Player of Match']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
    st.markdown('''<div class="insight-card"><div class="insight-icon">💡</div><div class="insight-content"><span class="insight-title">Strategic Performance Insight</span>The bar chart demonstrates a clear hierarchy in franchise performance, with select teams accumulating significantly more historical wins. The toss analysis reveals a distinct trend where captains prefer to field first, and the subsequent win strategy chart proves this decision is structurally advantageous, yielding higher match win rates when chasing targets.</div></div>''', unsafe_allow_html=True)

with tab2:
    st.markdown("### Compare Teams")
    h2h_col1, h2h_col2 = st.columns([1, 1])
    team1_select = h2h_col1.selectbox("Select Team 1", options=all_teams, index=all_teams.index('Chennai Super Kings') if 'Chennai Super Kings' in all_teams else 0)
    team2_select = h2h_col2.selectbox("Select Team 2", options=all_teams, index=all_teams.index('Mumbai Indians') if 'Mumbai Indians' in all_teams else 1)

    if team1_select and team2_select and team1_select != team2_select:
        h2h_matches = filtered_df[((filtered_df['team1'] == team1_select) & (filtered_df['team2'] == team2_select)) | ((filtered_df['team1'] == team2_select) & (filtered_df['team2'] == team1_select))]
        team1_wins = len(h2h_matches[h2h_matches['winner'] == team1_select])
        team2_wins = len(h2h_matches[h2h_matches['winner'] == team2_select])
        total_matches = len(h2h_matches)
        logo1 = get_image_base64(TEAM_LOGOS.get(team1_select, ""))
        logo2 = get_image_base64(TEAM_LOGOS.get(team2_select, ""))

        logo_col1, logo_col2, logo_col3 = st.columns([1, 1, 1])
        with logo_col1:
            st.markdown(f"<div style='text-align: center; padding: 10px;'><img src='{logo1}' style='width: 100%; max-width: 130px; object-fit: contain;'></div><h2 style='text-align: center; color: #1e40af; margin: 0; font-family: Outfit; font-size: clamp(1.5rem, 4vw, 2.5rem);'>{team1_wins} Wins</h2>", unsafe_allow_html=True)
        with logo_col2:
            st.markdown(f"<h4 style='text-align: center; color: #64748b; margin-top: 20px; margin-bottom: 5px; font-family: Outfit; font-size: clamp(1rem, 3vw, 1.5rem);'>Encounters</h4><h1 style='text-align: center; font-size: clamp(3rem, 8vw, 5rem); font-family: Outfit; color: #0f172a; margin: 0;'>{total_matches}</h1>", unsafe_allow_html=True)
            if total_matches == 0: st.markdown("<p style='text-align: center; color: #dc2626; font-weight: 500; margin-top: 15px; font-size: clamp(0.8rem, 2vw, 1rem);'>No matches found.</p>", unsafe_allow_html=True)
        with logo_col3:
            st.markdown(f"<div style='text-align: center; padding: 10px;'><img src='{logo2}' style='width: 100%; max-width: 130px; object-fit: contain;'></div><h2 style='text-align: center; color: #1e40af; margin: 0; font-family: Outfit; font-size: clamp(1.5rem, 4vw, 2.5rem);'>{team2_wins} Wins</h2>", unsafe_allow_html=True)

    st.markdown('''<div class="insight-card"><div class="insight-icon">🔍</div><div class="insight-content"><span class="insight-title">Head-to-Head Insight</span>This comparison isolates historical matchups between specific franchises. Reviewing direct win-loss ratios exposes psychological advantages and matchup dependencies that are obscured in aggregate seasonal standings. Outliers in these direct records often dictate specific player auction strategies.</div></div>''', unsafe_allow_html=True)

with tab3:
    st.markdown("### Full Match Database")
    st.dataframe(filtered_df, use_container_width=True)
    st.download_button(label="📥 Download as CSV", data=filtered_df.to_csv(index=False), file_name="ipl_analysis_data.csv", mime="text/csv")
    st.markdown('''<div class="insight-card"><div class="insight-icon">📊</div><div class="insight-content"><span class="insight-title">Data Transparency</span>Providing the raw dataset ensures analytical transparency and allows users to trace the visual insights back to specific event occurrences. The table format is necessary for identifying edge cases, examining anomalies in specific venues, and auditing match outcomes at a highly granular level.</div></div>''', unsafe_allow_html=True)

with tab4:
    adv_col1, adv_col2 = st.columns([1, 1])
    with adv_col1:
        st.markdown("### Match Frequency Over Time")
        matches_by_year = filtered_df.groupby('year').size().reset_index(name='matches')
        fig_timeline = px.line(matches_by_year, x='year', y='matches', markers=True, color_discrete_sequence=['#2563eb'])
        fig_timeline.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Plus Jakarta Sans", color="#334155"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_timeline, use_container_width=True)

        st.markdown("### Most Active Venues")
        top_venues = filtered_df['venue'].value_counts().head(8).reset_index()
        top_venues.columns = ['Venue', 'Matches']
        fig_venues = px.bar(top_venues, x='Matches', y='Venue', orientation='h', color='Matches', color_continuous_scale='Blues')
        fig_venues.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Plus Jakarta Sans", color="#334155"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_venues, use_container_width=True)

    with adv_col2:
        st.markdown("### Top Star Performers (POTM)")
        top_players = filtered_df['player_of_match'].value_counts().head(8).reset_index()
        top_players.columns = ['Player', 'Awards']
        fig_players = px.bar(top_players, x='Awards', y='Player', orientation='h', color='Awards', color_continuous_scale='Purples')
        fig_players.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Plus Jakarta Sans", color="#334155"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_players, use_container_width=True)

        st.markdown("### Win Efficiency Distribution")
        team_stats = [{'Team': t, 'Matches Played': len(filtered_df[(filtered_df['team1'] == t) | (filtered_df['team2'] == t)]), 'Wins': len(filtered_df[filtered_df['winner'] == t]), 'Win Rate (%)': (len(filtered_df[filtered_df['winner'] == t]) / len(filtered_df[(filtered_df['team1'] == t) | (filtered_df['team2'] == t)])) * 100} for t in all_teams if len(filtered_df[(filtered_df['team1'] == t) | (filtered_df['team2'] == t)]) > 0]
        fig_scatter = px.scatter(pd.DataFrame(team_stats), x='Matches Played', y='Wins', size='Win Rate (%)', color='Team', hover_name='Team')
        fig_scatter.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Plus Jakarta Sans", color="#334155"), margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown('''<div class="insight-card"><div class="insight-icon">🚀</div><div class="insight-content"><span class="insight-title">Advanced Metric Observations</span>The line chart documents scheduling shifts and timeline disruptions, while the venue layout reveals spatial dependencies for specific teams. The scatter plot provides crucial insight into win efficiency, plotting total matches against actual wins. Teams positioned above the general cluster line represent positive outliers with superior match conversion rates.</div></div>''', unsafe_allow_html=True)

# === END OF FILE - IF YOU DO NOT SEE THIS LINE IN GITHUB, YOU DID NOT COPY THE WHOLE THING! ===
