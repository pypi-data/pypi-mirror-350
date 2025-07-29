from discord_trad_bot import db
from discord.ext import commands
import aiosqlite
from discord.ext.commands import has_permissions, CheckFailure

# Supported language codes should be imported from main or constants if moved
from discord_trad_bot.constants import SUPPORTED_LANGUAGES

def setup(bot):
    @bot.command(name='debugdb')
    @has_permissions(administrator=True)
    async def debugdb(ctx):
        """Debug command to check database schema and content"""
        try:
            # Get all translation channels
            channels = await db.get_trans_channels()
            channels_info = "\n".join([f"Channel ID: {ch[0]}, Default Lang: {ch[1]}" for ch in channels])
            # Get some user preferences (limit to 5 for readability)
            async with aiosqlite.connect(db.DB_PATH) as conn:
                async with conn.execute('SELECT user_id, lang FROM user_lang LIMIT 5') as cursor:
                    users = await cursor.fetchall()
            users_info = "\n".join([f"User ID: {u[0]}, Lang: {u[1]}" for u in users])
            # Get table info
            async with aiosqlite.connect(db.DB_PATH) as conn:
                async with conn.execute("SELECT name FROM sqlite_master WHERE type='table'") as cursor:
                    tables = await cursor.fetchall()
            tables_info = "\n".join([f"Table: {t[0]}" for t in tables])
            # Format the response
            response = f"""**Database Debug Info:**\n\n**Tables:**\n{tables_info}\n\n**Translation Channels:**\n{channels_info}\n\n**Sample User Preferences (up to 5):**\n{users_info}"""
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error checking database: {str(e)}")

    @debugdb.error
    async def debugdb_error(ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send('You need to be an administrator to use this command.')

    @bot.command(name='settranschannel')
    @has_permissions(administrator=True)
    async def settranschannel(ctx, channel: commands.TextChannelConverter):
        """Set the translation channel. Usage: !settranschannel #channel"""
        await db.add_trans_channel(channel.id)
        await ctx.send(f'Translation channel added: {channel.mention}')

    @bot.command(name='addtranschannel')
    @has_permissions(administrator=True)
    async def addtranschannel(ctx, channel: commands.TextChannelConverter):
        """Add a new channel for automatic translation. Usage: !addtranschannel #channel"""
        if not await db.is_trans_channel(channel.id):
            await db.add_trans_channel(channel.id)
            await ctx.send(f'Translation channel added: {channel.mention}')
        else:
            await ctx.send(f'{channel.mention} is already a translation channel.')

    @bot.command(name='removetranschannel')
    @has_permissions(administrator=True)
    async def removetranschannel(ctx, channel: commands.TextChannelConverter):
        """Remove a channel from automatic translation. Usage: !removetranschannel #channel"""
        if not await db.is_trans_channel(channel.id):
            await ctx.send(f'{channel.mention} is not a translation channel.')
            return
        await db.remove_trans_channel(channel.id)
        await ctx.send(f'Translation channel removed: {channel.mention}')

    @bot.command(name='listtranschannels')
    @has_permissions(administrator=True)
    async def listtranschannels(ctx):
        """List all channels configured for automatic translation"""
        channels = await db.get_trans_channels()
        if not channels:
            await ctx.send('No translation channels configured.')
            return
        channel_list = []
        for channel_id, default_lang in channels:
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                channel_list.append(f"{channel.mention} (default: {default_lang})")
        await ctx.send("**Translation Channels:**\n" + "\n".join(channel_list))

    @bot.command(name='setchannellang')
    @has_permissions(administrator=True)
    async def setchannellang(ctx, channel: commands.TextChannelConverter, lang: str):
        """Set the default language for a translation channel. Usage: !setchannellang #channel <language_code>"""
        if not await db.is_trans_channel(channel.id):
            await ctx.send(f'{channel.mention} is not a translation channel.')
            return
        if lang not in SUPPORTED_LANGUAGES:
            await ctx.send(f'`{lang}` is not a supported language code. Use `!languages` to see the list of supported codes.')
            return
        await db.set_channel_default_lang(channel.id, lang)
        await ctx.send(f'Default language for {channel.mention} set to `{lang}`') 