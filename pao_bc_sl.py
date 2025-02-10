import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Sofascore API URL to get Panathinaikos BC upcoming matches
API_URL = "https://api.sofascore.com/api/v1/team/3508/events/next/0"

# Cache the data for 24 hours using st.cache_data
@st.cache_data(ttl=86400)  # 86400 seconds = 24 hours
def fetch_matches():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Extract upcoming matches
        matches = data.get('events', [])
        upcoming_matches = []

        for match in matches:
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            start_time = match['startTimestamp']
            competition = match['tournament']['name']  # Extract the competition name

            # Convert timestamp to readable format
            match_date = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

            # Store match details in a dictionary
            match_info = {
                "Date": match_date,
                "Game": f"{home_team} vs {away_team}",
                "Type": competition,  # Show the actual competition name
                "Month": datetime.fromtimestamp(start_time).strftime('%B')  # Extract the month
            }
            upcoming_matches.append(match_info)

        return upcoming_matches

    except requests.exceptions.RequestException as e:
        return [{"error": str(e)}]

# Streamlit UI
st.title("🏀 Panathinaikos BC Upcoming Matches")

matches = fetch_matches()

if "error" in matches[0]:
    st.error("Error fetching data: " + matches[0]["error"])
else:
    # Create DataFrame
    df = pd.DataFrame(matches)

    # Add filter options
    st.sidebar.title("Filter Options")
    
    # Default filters will be "All"
    month_filter = st.sidebar.selectbox("Select Month", ["All"] + list(df['Month'].unique()))
    type_filter = st.sidebar.selectbox("Select Competition Type", ["All"] + list(df['Type'].unique()))

    # Apply filters only if a filter is selected
    if month_filter != "All":
        df = df[df['Month'] == month_filter]

    if type_filter != "All":
        df = df[df['Type'] == type_filter]

    # Display the filtered table
    st.table(df)