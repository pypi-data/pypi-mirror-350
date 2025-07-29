# Discord Translation Bot

A Discord bot that automatically translates messages in a designated channel to each user's preferred language while maintaining Discord's rich formatting.

## Features

- Automatic translation of messages in a designated channel
- User language preferences
- Preserves Discord formatting (emojis, mentions, etc.)
- Free to use (uses Google Translate API free tier)

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your Discord bot token and Google Translate API key
5. Run the bot:
   ```
   python src/main.py
   ```

## Configuration

Create a `.env` file with the following variables:
```
DISCORD_TOKEN=your_discord_bot_token
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key
```

## Commands

### User Commands
- `!setlang <language_code>` - Set preferred language
- `!mylang` - Show current language setting
- `!languages` - List available languages

### Admin Commands
- `!settranschannel <channel>` - Set translation channel
- `!transstatus` - Show bot status and usage
