# Football Stats Project

A Python application that fetches football match data, statistics, and provides match predictions using the RapidAPI Football API.

## 🚀 Features

- **League Selection**: Browse and select from available football leagues worldwide
- **Match Data**: Get match information for specific dates and leagues
- **Live Statistics**: Fetch detailed match statistics including possession, shots, fouls, etc.
- **Team Analytics**: Access team form, season statistics, and performance metrics
- **Match Predictions**: AI-powered predictions based on team statistics and recent form
- **Interactive CLI**: User-friendly command-line interface for easy navigation
- **Security**: Input validation, error handling, and secure API key management

## 📋 Prerequisites

- Python 3.7+
- RapidAPI Football API subscription
- Internet connection for API calls

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone <your-repository-url>
   cd football_stats_project
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```bash
   touch .env
   ```

   Add your RapidAPI key to the `.env` file:

   ```
   API_FOOTBALL_KEY=your_rapidapi_key_here
   ```

## 🔑 API Setup

1. Visit [RapidAPI Football API](https://rapidapi.com/api-sports/api/api-football)
2. Subscribe to the API (free tier available)
3. Copy your API key from the dashboard
4. Add the key to your `.env` file as shown above

## 🎮 Usage

Run the application:

```bash
python main.py
```

### Step-by-step workflow:

1. **Enter Date**: Input a date in YYYY-MM-DD format (or press Enter for today)
2. **Select League**: Choose from the displayed list of available leagues
3. **View Results**: See match details, statistics, and predictions

### Example interaction:

```
⚽ Football Stats Project
========================================
Enter the date (YYYY-MM-DD) to get matches (leave blank for today): 2024-01-15

📡 Fetching available leagues...

📋 Available Leagues:
39: Premier League (England)
140: La Liga (Spain)
78: Bundesliga (Germany)
...

Enter the League ID you want to get matches for: 39

📊 Fetching matches for 2024-01-15...
✅ Found 2 match(es)

🏆 Match 1: Arsenal vs Brighton
   📊 Statistics for Arsenal:
     • Ball Possession: 65%
     • Total Shots: 18
     • Shots on Goal: 8
     • ...

   🔍 Analyzing team forms...
   🎯 Prediction: Home team is more likely to win (45.5 vs 32.1)
```

## 📊 Available Data

The application provides access to:

- **Match Information**: Teams, venues, dates, scores
- **Live Statistics**: Possession, shots, passes, fouls, cards, etc.
- **Team Analytics**: Season statistics, form, goals, wins/draws/losses
- **Predictions**: Algorithm-based match outcome predictions

## 🏗️ Project Structure

```
football_stats_project/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (create this)
├── .gitignore          # Git ignore file (prevents sensitive data exposure)
├── README.md           # Project documentation
└── venv/               # Virtual environment (created after setup)
```

## 🔮 Prediction Algorithm

The prediction system analyzes:

- Recent team form (W/D/L pattern)
- Season statistics (wins, draws, losses)
- Goal scoring and conceding records
- Overall team performance metrics

Scoring factors:

- Win: +3 points
- Draw: +1 point
- Loss: -1 point
- Goals for: +0.5 per goal
- Goals against: -0.5 per goal

## 🚨 Error Handling

The application includes comprehensive error handling for:

- Invalid date formats and ranges
- Non-existent league IDs
- API connection issues
- Missing match data
- Network timeouts
- JSON parsing errors

## 📝 API Rate Limits

Be aware of your RapidAPI subscription limits:

- Free tier: Limited requests per month
- Check your dashboard for current usage
- Consider upgrading for heavy usage

## 🛡️ Security Features

### Input Validation

- Date format and range validation
- League ID numeric validation
- API response validation

### Error Handling

- Graceful API error handling
- Timeout protection (10 seconds)
- JSON parsing error handling

### Secure Configuration

- Environment variable management
- API key validation
- .gitignore protection for sensitive files

## 🛡️ Environment Variables

Required variables in `.env`:

- `API_FOOTBALL_KEY`: Your RapidAPI Football API key

**⚠️ IMPORTANT**: Never commit your `.env` file to version control. The `.gitignore` file prevents this automatically.

## 📈 Future Enhancements

Potential improvements:

- Web interface using Flask/Django
- Database storage for historical data
- Advanced prediction algorithms
- Team comparison features
- Export functionality for statistics
- Rate limiting and caching
- User authentication system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This application is for educational and personal use. Match predictions are for entertainment purposes only and should not be used for gambling or betting decisions.

## 🆘 Troubleshooting

**Common Issues:**

1. **"API_FOOTBALL_KEY not found"**

   - Check your `.env` file configuration
   - Ensure the file is in the project root
   - Verify your RapidAPI subscription is active

2. **"No matches found"**

   - Try a different date
   - Ensure the league has matches on the selected date
   - Check if the league is active for the selected season

3. **"League ID not found"**

   - Use only the numeric IDs displayed in the league list
   - Check for typos in your input
   - Ensure the league is available in the API

4. **"API Error"**

   - Check your internet connection
   - Verify your API key is valid
   - Check your RapidAPI usage limits

5. **Import errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

For additional help, please open an issue in the repository.

## 🔒 Security Notes

- **API Key Protection**: Your API key is stored in the `.env` file which is excluded from version control
- **Input Validation**: All user inputs are validated to prevent injection attacks
- **Error Handling**: Comprehensive error handling prevents crashes and information leakage
- **Rate Limiting**: Built-in timeout protection prevents excessive API usage

**⚠️ CRITICAL**: If you accidentally exposed your API key in git history, immediately:

1. Generate a new API key from RapidAPI
2. Update your `.env` file with the new key
3. Consider the old key compromised
