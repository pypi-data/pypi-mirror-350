import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord_trad_bot import db
from discord import app_commands
from discord_trad_bot.utils import preserve_user_mentions, restore_mentions, translate_message, detect_language
from discord_trad_bot.constants import SUPPORTED_LANGUAGES
# Import command modules
from discord_trad_bot.commands import user_commands, admin_commands, misc_commands
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'bot_status': 'online' if bot.is_ready() else 'offline'
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_health_server():
    server = HTTPServer(('0.0.0.0', int(os.getenv('PORT', '8080'))), HealthCheckHandler)
    print(f"Health check server running on port {os.getenv('PORT', '8080')}")
    server.serve_forever()

class TranslationBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents, help_command=None)
        
    async def setup_hook(self):
        # Add autocomplete for language codes
        @self.tree.command(name="setlang", description="Set your preferred language")
        @app_commands.describe(language="Your preferred language")
        async def setlang(interaction: discord.Interaction, language: str):
            if language not in SUPPORTED_LANGUAGES:
                await interaction.response.send_message(f'`{language}` is not a supported language code. Use `!languages` to see the list of supported codes.', ephemeral=True)
                return
            await db.set_user_lang(interaction.user.id, language)
            await interaction.response.send_message(f'Your preferred language has been set to `{language}`', ephemeral=True)
        
        @setlang.autocomplete('language')
        async def language_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
            return [
                app_commands.Choice(name=lang, value=lang)
                for lang in sorted(SUPPORTED_LANGUAGES)
                if current.lower() in lang.lower()
            ][:25]  # Discord limits to 25 choices

bot = TranslationBot()

# Register commands
user_commands.setup(bot)
admin_commands.setup(bot)
misc_commands.setup(bot)

# --- Bot Events ---
@bot.event
async def on_ready():
    await db.init_db()
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # Skip translation for commands
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return
    # Check if the message is in a translation channel
    if await db.is_trans_channel(message.channel.id):
        user_lang = await db.get_user_lang(message.author.id)
        if not user_lang:
            # Use channel's default language if user hasn't set one
            user_lang = await db.get_channel_default_lang(message.channel.id)
        # Preserve user mentions
        content_preserved, mention_map = preserve_user_mentions(message.content)
        detected_lang = detect_language(content_preserved)
        # Only translate if the message isn't already in the user's preferred language
        if detected_lang and detected_lang != user_lang:
            try:
                translated_text = translate_message(content_preserved, user_lang)
                translated_text = restore_mentions(translated_text, mention_map)
                await message.reply(f"{translated_text}")
            except Exception as e:
                await message.reply(f"[Translation error: {e}]")
        else:
            content_preserved = restore_mentions(content_preserved, mention_map)
            await message.reply(f"{content_preserved}")
    await bot.process_commands(message)

def run_bot():
    """Entry point for the bot when used as a package."""
    # Start the health check server in a separate thread
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    
    # Run the bot
    bot.run(os.getenv('DISCORD_TOKEN'))

# Run the bot if this file is executed directly
if __name__ == '__main__':
    run_bot() 