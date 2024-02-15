import aiosqlite


async def initialize_database(db: aiosqlite.Connection):
    cursor = await db.execute("CREATE TABLE preferences(guild, user, voice, wpm, wordgap, pitch, amplitude)")
    await db.commit()
    await cursor.close()
