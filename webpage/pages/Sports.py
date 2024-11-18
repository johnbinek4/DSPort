import streamlit as st
import pandas as pd
import os

# Set the page title and layout
st.set_page_config(page_title="Sports Analytics", layout="wide")

# Add styling
st.markdown("""
    <style>
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    #MainMenu {
        display: none;
    }
    section[data-testid="stSidebarNav"] {
        display: none;
    }
    .main-title {
        text-align: center;
        color: #1f1f1f;
        font-size: 36px;
        font-weight: 600;
        margin-bottom: 30px;
        padding-top: 20px;
    }
    .conference-box {
        padding: 30px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .afc-box {
        background-color: rgba(207, 20, 43, 0.05);
        border: 3px solid #CF142B;
    }
    .nfc-box {
        background-color: rgba(0, 51, 141, 0.05);
        border: 3px solid #00338D;
    }
    .conference-title {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
        color: #333;
    }
    .team-row {
        display: grid;
        grid-template-columns: 50px auto;
        align-items: center;
        padding: 12px 15px;
        border-radius: 5px;
        margin: 8px 0;
        color: white;
    }
    .rank-column {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
    }
    .team-info {
        display: flex;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

def load_team_data():
    """Load team data using paths that work both locally and in cloud"""
    try:
        # First try local path
        with open('team_logos.txt', 'r') as file:
            logos = dict(line.strip().split(': ') for line in file if line.strip())
        
        with open('team_colors.txt', 'r') as file:
            colors = {}
            for line in file:
                if ': ' in line:
                    team, color_str = line.strip().split(': ')
                    primary_color = color_str.split(',')[0].strip()
                    colors[team] = primary_color.replace('#', '')
    except FileNotFoundError:
        # Try alternative path
        with open('webpage/pages/team_logos.txt', 'r') as file:
            logos = dict(line.strip().split(': ') for line in file if line.strip())
        
        with open('webpage/pages/team_colors.txt', 'r') as file:
            colors = {}
            for line in file:
                if ': ' in line:
                    team, color_str = line.strip().split(': ')
                    primary_color = color_str.split(',')[0].strip()
                    colors[team] = primary_color.replace('#', '')
    
    print(f"Loaded {len(logos)} logos and {len(colors)} colors")
    return logos, colors

def load_rankings_data():
    """Load rankings using paths that work both locally and in cloud"""
    try:
        # First try local path
        with open('rankings.txt', 'r') as file:
            rankings = dict(line.strip().split(': ') for line in file if line.strip())
    except FileNotFoundError:
        # Try alternative path
        try:
            with open('webpage/pages/rankings.txt', 'r') as file:
                rankings = dict(line.strip().split(': ') for line in file if line.strip())
        except FileNotFoundError:
            print("Rankings file not found")
            rankings = {}
    
    print(f"Loaded {len(rankings)} rankings")
    return rankings

def create_team_df(teams, logos, colors, rankings):
    df = pd.DataFrame({
        'Logo': [logos.get(team) for team in teams],
        'Team': teams,
        'Background': [f"#{colors.get(team, '000000')}" for team in teams],
        'Rank': [rankings.get(team, '-') for team in teams],
    })
    print(f"Created DataFrame with {len(df)} teams")
    print(df)
    return df

def create_team_rows(df):
    rows = []
    for _, row in df.iterrows():
        team_row = f'''
        <div class="team-row" style="background-color: {row['Background']}">
            <div class="rank-column">{row['Rank']}</div>
            <div class="team-info">
                <img src="{row['Logo']}" style="height:40px;">
                <span style="margin-left: 15px">{row['Team']}</span>
            </div>
        </div>
        '''
        rows.append(team_row)
    print(f"Created {len(rows)} team rows")
    return '\n'.join(rows)

# Add sidebar navigation
with st.sidebar:
    st.title("Sports Categories")
    sports_nav = st.radio(
        "Select Sport",
        ["Baseball", "Football", "NFL Big Data Bowl '25 (Kaggle Competition)"],
        key="sports_nav",
        label_visibility="collapsed"
    )

if sports_nav == "Football":
    # Main title
    st.markdown('<h1 style="text-align: center; margin-bottom: 20px;">NFL Power Rankings</h1>', unsafe_allow_html=True)
    
    # Add description paragraph
    st.markdown("""
        <div style="text-align: center; max-width: 800px; margin: 0 auto 40px auto; padding: 0 20px;">
        Welcome to our NFL Power Rankings, where we combine advanced analytics with on-field performance metrics 
        to rank all 32 NFL teams. Our model incorporates factors such as offensive and defensive efficiency, 
        strength of schedule, recent performance trends, and key player metrics. Rankings are updated weekly 
        to reflect the most recent game results and statistical trends.
        </div>
    """, unsafe_allow_html=True)

    print("\n=== Starting Data Loading ===")
    # Load all data
    logos, colors = load_team_data()
    rankings = load_rankings_data()
    
    print("\n=== Debug Information ===")
    print(f"Logos loaded: {len(logos)}")
    print(f"Colors loaded: {len(colors)}")
    print(f"Rankings loaded: {rankings}")
    
    # Create team lists
    afc_teams = ['PIT', 'KC', 'BAL', 'MIA', 'JAX', 'BUF', 'CLE', 'HOU', 'IND', 'LAC', 
                 'CIN', 'NYJ', 'TEN', 'LV', 'DEN', 'NE']
    nfc_teams = ['SF', 'DAL', 'PHI', 'DET', 'SEA', 'MIN', 'GB', 'ATL', 'NO', 'TB', 
                 'CHI', 'LAR', 'NYG', 'WAS', 'ARI', 'CAR']
    
    print("\nTeam Lists:")
    print(f"AFC Teams: {afc_teams}")
    print(f"NFC Teams: {nfc_teams}")
    
    print("\n=== Creating DataFrames ===")
    # Create DataFrames
    afc_df = create_team_df(afc_teams, logos, colors, rankings)
    nfc_df = create_team_df(nfc_teams, logos, colors, rankings)
    
    print("\n=== Sorting DataFrames ===")
    # Sort DataFrames by ranking
    afc_df['Rank'] = pd.to_numeric(afc_df['Rank'])
    nfc_df['Rank'] = pd.to_numeric(nfc_df['Rank'])
    afc_df = afc_df.sort_values('Rank')
    nfc_df = nfc_df.sort_values('Rank')
    
    print("\nDataFrames after sorting:")
    print("AFC DataFrame:")
    print(afc_df)
    print("\nNFC DataFrame:")
    print(nfc_df)
    
    print("\n=== Creating Columns ===")
    # Create two columns
    st.write("Testing AFC Display:")
    st.markdown('''
    <div class="conference-box afc-box">
        <div class="conference-title">AFC Test</div>
        <div class="team-row" style="background-color: #241773">
            <div class="rank-column">1</div>
            <div class="team-info">
                <span style="margin-left: 15px">TEST AFC</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.write("Testing NFC Display:")
    st.markdown('''
    <div class="conference-box nfc-box">
        <div class="conference-title">NFC Test</div>
        <div class="team-row" style="background-color: #97233F">
            <div class="rank-column">1</div>
            <div class="team-info">
                <span style="margin-left: 15px">TEST NFC</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

elif sports_nav == "Baseball":
    st.header("Baseball Analytics")
    st.write("Coming Soon!")

elif sports_nav == "NFL Big Data Bowl '25 (Kaggle Competition)":
    st.header("NFL Big Data Bowl '25")
    st.write("Coming Soon!")
