import aiosqlite


async def initialize_database(db: aiosqlite.Connection):
    cursor = await db.execute(
        """CREATE TABLE preferences(
                guild INTEGER NOT NULL,
                user INTEGER NOT NULL,
                voice TEXT,
                wpm INTEGER,
                wordgap INTEGER,
                pitch INTEGER,
                amplitude INTEGER,
                PRIMARY KEY(guild, user)
            )""")
    await db.commit()
    await cursor.close()
