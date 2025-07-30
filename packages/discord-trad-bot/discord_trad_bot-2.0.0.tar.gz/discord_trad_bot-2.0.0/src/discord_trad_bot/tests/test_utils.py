import sys
import os
from discord_trad_bot.utils import preserve_user_mentions, restore_mentions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from discord_trad_bot import db
from unittest.mock import AsyncMock
from discord_trad_bot.commands import user_commands
from discord.ext import commands
from discord import Intents



def test_preserve_and_restore_mentions():
    text = 'Hello <@12345> and <@!67890>'
    preserved, mention_map = preserve_user_mentions(text)
    # Placeholders should be present
    assert '[[[MENTION1]]]' in preserved
    assert '[[[MENTION2]]]' in preserved
    # Map should have correct values
    assert mention_map['[[[MENTION1]]]'] == '<@12345>'
    assert mention_map['[[[MENTION2]]]'] == '<@!67890>' or mention_map['[[[MENTION2]]]'] == '<@67890>'
    # Restoring should give back the original text (allowing for both mention formats)
    restored = restore_mentions(preserved, mention_map)
    assert restored.replace('<@!67890>', '<@67890>') == text.replace('<@!67890>', '<@67890>')


@pytest.mark.asyncio
async def test_set_and_get_user_lang(tmp_path):
    db.DB_PATH = str(tmp_path / 'test.db')
    await db.init_db()
    await db.set_user_lang(42, 'fr')
    lang = await db.get_user_lang(42)
    assert lang == 'fr'


@pytest.mark.asyncio
async def test_setlang_valid(monkeypatch):
    bot = commands.Bot(command_prefix="!", intents=Intents.default())
    user_commands.setup(bot)
    setlang = bot.get_command("setlang").callback

    # Mock context and db
    ctx = AsyncMock()
    ctx.author.id = 123
    ctx.send = AsyncMock()
    monkeypatch.setattr(db, "set_user_lang", AsyncMock())
    monkeypatch.setattr("discord_trad_bot.commands.user_commands.SUPPORTED_LANGUAGES", {"fr", "en", "de"})

    # Call the command (note: pass self as first arg for method)
    await setlang(ctx, "fr")
    ctx.send.assert_awaited_with("Your preferred language has been set to `fr`")


@pytest.mark.asyncio
async def test_setlang_invalid(monkeypatch):
    bot = commands.Bot(command_prefix="!", intents=Intents.default())
    user_commands.setup(bot)
    setlang = bot.get_command("setlang").callback

    ctx = AsyncMock()
    ctx.author.id = 123
    ctx.send = AsyncMock()
    monkeypatch.setattr(db, "set_user_lang", AsyncMock())
    monkeypatch.setattr("discord_trad_bot.commands.user_commands.SUPPORTED_LANGUAGES", {"fr", "en"})

    await setlang(ctx, "de")
    ctx.send.assert_awaited_with("`de` is not a supported language code. Use `!languages` to see the list of supported codes.")


@pytest.mark.asyncio
async def test_ping():
    bot = commands.Bot(command_prefix="!", intents=Intents.default())
    user_commands.setup(bot)
    ping = bot.get_command("ping").callback

    ctx = AsyncMock()
    ctx.send = AsyncMock()

    await ping(ctx)
    ctx.send.assert_awaited_with("Pong!")

@pytest.mark.asyncio
async def test_mylang_with_lang(monkeypatch):
    bot = commands.Bot(command_prefix="!", intents=Intents.default())
    user_commands.setup(bot)
    mylang = bot.get_command("mylang").callback

    ctx = AsyncMock()
    ctx.author.id = 123
    ctx.send = AsyncMock()
    monkeypatch.setattr(db, "get_user_lang", AsyncMock(return_value="fr"))

    await mylang(ctx)
    ctx.send.assert_awaited_with("Your preferred language is `fr`.")

@pytest.mark.asyncio
async def test_languages_chunking(monkeypatch):
    bot = commands.Bot(command_prefix="!", intents=Intents.default())
    user_commands.setup(bot)
    languages = bot.get_command("languages").callback

    ctx = AsyncMock()
    ctx.send = AsyncMock()
    # Patch SUPPORTED_LANGUAGES to 120 fake codes
    fake_langs = {f"lang{i}" for i in range(120)}
    monkeypatch.setattr("discord_trad_bot.commands.user_commands.SUPPORTED_LANGUAGES", fake_langs)

    await languages(ctx)
    # Should send 3 times (120/50 = 2.4 -> 3 chunks)
    assert ctx.send.await_count == 3

@pytest.mark.asyncio
async def test_setlang_uppercase(monkeypatch):
    bot = commands.Bot(command_prefix="!", intents=Intents.default())
    user_commands.setup(bot)
    setlang = bot.get_command("setlang").callback

    ctx = AsyncMock()
    ctx.author.id = 123
    ctx.send = AsyncMock()
    monkeypatch.setattr(db, "set_user_lang", AsyncMock())
    monkeypatch.setattr("discord_trad_bot.commands.user_commands.SUPPORTED_LANGUAGES", {"fr", "en"})

    await setlang(ctx, "FR")
    ctx.send.assert_awaited_with("Your preferred language has been set to `fr`")