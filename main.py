import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('API_FOOTBALL_KEY')

# Base URL and headers for RapidAPI
BASE_URL = 'https://api-football-v1.p.rapidapi.com/v3'

headers = {
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
    'x-rapidapi-key': API_KEY
}

def get_leagues():
    url = f'{BASE_URL}/leagues'
    response = requests.get(url, headers=headers)
    data = response.json()
    return data.get('response', [])

def get_matches(league_id, date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    season = date_obj.year
    url = f'{BASE_URL}/fixtures'
    params = {
        'league': league_id,
        'season': season,
        'date': date_str
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data.get('response', [])

def get_match_stats(fixture_id):
    url = f'{BASE_URL}/fixtures/statistics'
    params = {
        'fixture': fixture_id
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data.get('response', [])

def get_team_form(team_id, league_id, season):
    url = f'{BASE_URL}/teams/statistics'
    params = {
        'team': team_id,
        'league': league_id,
        'season': season
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data.get('response', {})

def predict_winner(home_team_stats, away_team_stats):
    # Simple scoring based on key statistics
    scoring_factors = {
        'wins': 3,
        'draws': 1,
        'loses': -1,
        'goals_for': 0.5,
        'goals_against': -0.5
    }
    
    def calculate_score(team_stats):
        score = 0
        form = team_stats.get('form', '')
        fixtures = team_stats.get('fixtures', {})
        goals = team_stats.get('goals', {})
        lineups = team_stats.get('lineups', [])
        
        # Recent form: W/D/L
        recent_form = form.replace('W', '3 ').replace('D', '1 ').replace('L', '-1 ').split()
        recent_score = sum([int(x) for x in recent_form]) if recent_form else 0
        score += recent_score
        
        # Total wins, draws, loses
        wins = fixtures.get('wins', {}).get('total', 0)
        draws = fixtures.get('draws', {}).get('total', 0)
        loses = fixtures.get('loses', {}).get('total', 0)
        score += (wins * scoring_factors['wins'] + draws * scoring_factors['draws'] + loses * scoring_factors['loses'])
        
        # Goals for and against
        goals_for = goals.get('for', {}).get('total', {}).get('total', 0)
        goals_against = goals.get('against', {}).get('total', {}).get('total', 0)
        score += (goals_for * scoring_factors['goals_for'] + goals_against * scoring_factors['goals_against'])
        
        return score
    
    home_score = calculate_score(home_team_stats)
    away_score = calculate_score(away_team_stats)
    
    if home_score > away_score:
        prediction = f"Home team is more likely to win ({home_score} vs {away_score})"
    elif away_score > home_score:
        prediction = f"Away team is more likely to win ({away_score} vs {home_score})"
    else:
        prediction = f"The match is likely to be a draw ({home_score} vs {away_score})"
    
    return prediction

def main():
    # Prompt for date input
    date_str = input("Enter the date (YYYY-MM-DD) to get matches (leave blank for today): ") or datetime.today().strftime('%Y-%m-%d')

    # Get leagues
    leagues = get_leagues()

    # Prompt user for league selection
    print("\nAvailable Leagues:")
    league_options = []
    for league_info in leagues:
        league = league_info['league']
        country = league_info['country']
        league_options.append({
            'id': league['id'],
            'name': league['name'],
            'country': country['name']
        })
        print(f"{league['id']}: {league['name']} ({country['name']})")

    # Ask for league ID
    league_id_input = input("\nEnter the League ID you want to get matches for (e.g., 3 for Europa League): ")
    try:
        league_id = int(league_id_input)
    except ValueError:
        print("Invalid League ID. Please enter a numeric value.")
        return

    # Check if the league ID exists
    league_exists = any(league['id'] == league_id for league in league_options)
    if not league_exists:
        print("League ID not found.")
        return

    season = datetime.strptime(date_str, '%Y-%m-%d').year
    matches = get_matches(league_id, date_str)
    if not matches:
        print(f"No matches found for {date_str} in the selected league.")
        return

    for match in matches:
        fixture = match['fixture']
        teams = match['teams']
        fixture_id = fixture['id']
        home_team = teams['home']
        away_team = teams['away']
        print(f'\nMatch: {home_team["name"]} vs {away_team["name"]}')

        # Get statistics for the match
        stats = get_match_stats(fixture_id)
        if not stats:
            print("No statistics available for this match yet.")
        else:
            for team_stats in stats:
                team_name = team_stats['team']['name']
                print(f'\nStatistics for {team_name}:')
                for stat in team_stats['statistics']:
                    stat_type = stat['type']
                    stat_value = stat['value'] if stat['value'] is not None else 'N/A'
                    print(f'  {stat_type}: {stat_value}')

        # Get team forms
        home_team_stats = get_team_form(home_team['id'], league_id, season)
        away_team_stats = get_team_form(away_team['id'], league_id, season)

        if home_team_stats and away_team_stats:
            prediction = predict_winner(home_team_stats, away_team_stats)
            print(f'\nPrediction: {prediction}')
        else:
            print("Team statistics not available for prediction.")

if __name__ == '__main__':
    main()
