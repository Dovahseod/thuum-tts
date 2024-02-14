import aiosqlite


async def _initialize_database(db: aiosqlite.Connection):
    cursor = await db.execute("CREATE TABLE preferences(guild, user, voice, wpm, gap, pitch, amplitude)")
    await db.commit()
    await cursor.close()
