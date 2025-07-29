import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'user_prefs.db')

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Drop old table if it exists
        await db.execute('DROP TABLE IF EXISTS trans_channel')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_lang (
                user_id TEXT PRIMARY KEY,
                lang TEXT NOT NULL
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS trans_channels (
                channel_id TEXT PRIMARY KEY,
                default_lang TEXT DEFAULT 'en'
            )
        ''')
        await db.commit()

async def set_user_lang(user_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO user_lang (user_id, lang) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET lang=excluded.lang
        ''', (str(user_id), lang))
        await db.commit()

async def get_user_lang(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT lang FROM user_lang WHERE user_id = ?', (str(user_id),)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def add_trans_channel(channel_id: int, default_lang: str = 'en'):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO trans_channels (channel_id, default_lang) VALUES (?, ?)
            ON CONFLICT(channel_id) DO UPDATE SET default_lang=excluded.default_lang
        ''', (str(channel_id), default_lang))
        await db.commit()

async def remove_trans_channel(channel_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('DELETE FROM trans_channels WHERE channel_id = ?', (str(channel_id),))
        await db.commit()

async def get_trans_channels():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT channel_id, default_lang FROM trans_channels') as cursor:
            rows = await cursor.fetchall()
            return [(int(row[0]), row[1]) for row in rows]

async def is_trans_channel(channel_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT 1 FROM trans_channels WHERE channel_id = ?', (str(channel_id),)) as cursor:
            row = await cursor.fetchone()
            return bool(row)

async def set_channel_default_lang(channel_id: int, default_lang: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            UPDATE trans_channels 
            SET default_lang = ? 
            WHERE channel_id = ?
        ''', (default_lang, str(channel_id)))
        await db.commit()

async def get_channel_default_lang(channel_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT default_lang FROM trans_channels WHERE channel_id = ?', (str(channel_id),)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 'en'

async def set_trans_channel(channel_id: int):
    await add_trans_channel(channel_id)

async def get_trans_channel():
    channels = await get_trans_channels()
    return channels[0][0] if channels else None 