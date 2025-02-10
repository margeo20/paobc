import requests
import json
from datetime import datetime

def fetch_upcoming_matches(team_id):
    # Sofascore API endpoint for the team's schedule
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/next/0"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Extract upcoming matches
        matches = data.get('events', [])
        upcoming_matches = []

        for match in matches:
            # Extract match details
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            start_time = match['startTimestamp']
            competition = match['tournament']['name']  # Tournament type (e.g., EuroLeague)

            # Convert timestamp to readable format
            match_date = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

            # Create a dictionary for JSON output
            match_info = {
                "date": match_date,
                "game": f"{home_team} vs {away_team}",
                "type": competition
            }
            upcoming_matches.append(match_info)

        return json.dumps(upcoming_matches, indent=4, ensure_ascii=False)  # Convert to JSON format

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return json.dumps({"error": "Failed to fetch matches"})

if __name__ == "__main__":
    # Panathinaikos BC team ID on Sofascore
    team_id = 3508
    matches_json = fetch_upcoming_matches(team_id)
    
    print(matches_json)