from src import db
from src.constants import SUPPORTED_LANGUAGES



def setup(bot):
    @bot.command(name='setlang')
    async def setlang(ctx, lang: str):
        """Set your preferred language for translations. Example: !setlang fr"""
        lang = lang.lower()
        if lang not in SUPPORTED_LANGUAGES:
            await ctx.send(f'`{lang}` is not a supported language code. Use `!languages` to see the list of supported codes.')
            return
        await db.set_user_lang(ctx.author.id, lang)
        await ctx.send(f'Your preferred language has been set to `{lang}`')

    @bot.command(name='languages')
    async def languages(ctx):
        """Display all supported language codes"""
        codes = sorted(SUPPORTED_LANGUAGES)
        chunk_size = 50
        for i in range(0, len(codes), chunk_size):
            await ctx.send(' '.join(codes[i:i+chunk_size]))

    @bot.command(name='mylang')
    async def mylang(ctx):
        """Show your current preferred language setting"""
        user_lang = await db.get_user_lang(ctx.author.id)
        if user_lang:
            await ctx.send(f'Your preferred language is `{user_lang}`.')
        else:
            await ctx.send('You have not set a preferred language yet. Use `!setlang <language_code>`.')

    @bot.command(name='ping')
    async def ping(ctx):
        """Simple command to test if the bot is working"""
        await ctx.send('Pong!') 