import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import re
import sys

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('API_FOOTBALL_KEY')

# Validate API key exists
if not API_KEY:
    print("❌ ERROR: API_FOOTBALL_KEY not found in environment variables.")
    print("Please create a .env file with your RapidAPI key:")
    print("API_FOOTBALL_KEY=your_api_key_here")
    sys.exit(1)

# Base URL and headers for RapidAPI
BASE_URL = 'https://api-football-v1.p.rapidapi.com/v3'

headers = {
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
    'x-rapidapi-key': API_KEY
}

def validate_date(date_str):
    """Validate date format and range"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        # Check if date is not in the future
        if date_obj > datetime.now():
            return False, "Date cannot be in the future"
        # Check if date is not too far in the past (e.g., 10 years ago)
        if date_obj < datetime(2014, 1, 1):
            return False, "Date too far in the past"
        return True, date_obj
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"

def validate_league_id(league_id_str):
    """Validate league ID input"""
    try:
        league_id = int(league_id_str)
        if league_id <= 0:
            return False, "League ID must be a positive number"
        return True, league_id
    except ValueError:
        return False, "League ID must be a number"

def safe_api_call(url, headers, params=None):
    """Make API calls with error handling"""
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None
    except ValueError as e:
        print(f"❌ JSON Parse Error: {e}")
        return None

def get_leagues():
    url = f'{BASE_URL}/leagues'
    data = safe_api_call(url, headers)
    if data:
        return data.get('response', [])
    return []

def get_matches(league_id, date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    season = date_obj.year
    url = f'{BASE_URL}/fixtures'
    params = {
        'league': league_id,
        'season': season,
        'date': date_str
    }
    data = safe_api_call(url, headers, params)
    if data:
        return data.get('response', [])
    return []

def get_match_stats(fixture_id):
    url = f'{BASE_URL}/fixtures/statistics'
    params = {
        'fixture': fixture_id
    }
    data = safe_api_call(url, headers, params)
    if data:
        return data.get('response', [])
    return []

def get_team_form(team_id, league_id, season):
    url = f'{BASE_URL}/teams/statistics'
    params = {
        'team': team_id,
        'league': league_id,
        'season': season
    }
    data = safe_api_call(url, headers, params)
    if data:
        return data.get('response', {})
    return {}

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
    print("⚽ Football Stats Project")
    print("=" * 40)
    
    # Prompt for date input with validation
    while True:
        date_str = input("Enter the date (YYYY-MM-DD) to get matches (leave blank for today): ").strip()
        if not date_str:
            date_str = datetime.today().strftime('%Y-%m-%d')
        
        is_valid, result = validate_date(date_str)
        if is_valid:
            break
        else:
            print(f"❌ {result}")
            continue

    # Get leagues
    print("📡 Fetching available leagues...")
    leagues = get_leagues()
    
    if not leagues:
        print("❌ Failed to fetch leagues. Please check your API key and internet connection.")
        return

    # Prompt user for league selection
    print("\n📋 Available Leagues:")
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

    # Ask for league ID with validation
    while True:
        league_id_input = input("\nEnter the League ID you want to get matches for: ").strip()
        is_valid, result = validate_league_id(league_id_input)
        if is_valid:
            league_id = result
            break
        else:
            print(f"❌ {result}")
            continue

    # Check if the league ID exists
    league_exists = any(league['id'] == league_id for league in league_options)
    if not league_exists:
        print("❌ League ID not found in the available leagues.")
        return

    print(f"📊 Fetching matches for {date_str}...")
    season = datetime.strptime(date_str, '%Y-%m-%d').year
    matches = get_matches(league_id, date_str)
    
    if not matches:
        print(f"❌ No matches found for {date_str} in the selected league.")
        return

    print(f"✅ Found {len(matches)} match(es)")
    
    for i, match in enumerate(matches, 1):
        fixture = match['fixture']
        teams = match['teams']
        fixture_id = fixture['id']
        home_team = teams['home']
        away_team = teams['away']
        
        print(f'\n🏆 Match {i}: {home_team["name"]} vs {away_team["name"]}')

        # Get statistics for the match
        stats = get_match_stats(fixture_id)
        if not stats:
            print("   📊 No statistics available for this match yet.")
        else:
            for team_stats in stats:
                team_name = team_stats['team']['name']
                print(f'\n   📊 Statistics for {team_name}:')
                for stat in team_stats['statistics']:
                    stat_type = stat['type']
                    stat_value = stat['value'] if stat['value'] is not None else 'N/A'
                    print(f'     • {stat_type}: {stat_value}')

        # Get team forms
        print("   🔍 Analyzing team forms...")
        home_team_stats = get_team_form(home_team['id'], league_id, season)
        away_team_stats = get_team_form(away_team['id'], league_id, season)

        if home_team_stats and away_team_stats:
            prediction = predict_winner(home_team_stats, away_team_stats)
            print(f'   🎯 Prediction: {prediction}')
        else:
            print("   ❌ Team statistics not available for prediction.")

if __name__ == '__main__':
    main()
