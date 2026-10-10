import aiosqlite

DB_NAME = "game.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                clicks INTEGER DEFAULT 0,
                coins INTEGER DEFAULT 0,
                energy INTEGER DEFAULT 100,
                max_energy INTEGER DEFAULT 100
            )
        """)
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT clicks, coins, energy, max_energy FROM users WHERE user_id = ?", 
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "clicks": row[0],
                    "coins": row[1],
                    "energy": row[2],
                    "max_energy": row[3]
                }
            
            # Если пользователя нет в базе — создаем нового
            await db.execute(
                "INSERT INTO users (user_id, clicks, coins, energy, max_energy) VALUES (?, 0, 0, 100, 100)", 
                (user_id,)
            )
            await db.commit()
            return {"clicks": 0, "coins": 0, "energy": 100, "max_energy": 100}

async def add_click(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        user = await get_user(user_id)
        if user["energy"] > 0:
            new_clicks = user["clicks"] + 1
            new_coins = user["coins"] + 1  # За каждый клик даем 1 монету
            new_energy = user["energy"] - 1
            await db.execute(
                "UPDATE users SET clicks = ?, coins = ?, energy = ? WHERE user_id = ?", 
                (new_clicks, new_coins, new_energy, user_id)
            )
            await db.commit()
            return {
                "clicks": new_clicks,
                "coins": new_coins,
                "energy": new_energy,
                "max_energy": user["max_energy"]
            }
        return user

async def get_top_players(limit: int = 10):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT user_id, clicks, coins FROM users ORDER BY clicks DESC LIMIT ?", 
            (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [{"user_id": row[0], "clicks": row[1], "coins": row[2]} for row in rows]