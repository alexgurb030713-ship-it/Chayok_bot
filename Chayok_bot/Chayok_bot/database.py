import aiosqlite

DB_NAME = "game.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                clicks INTEGER DEFAULT 0,
                energy INTEGER DEFAULT 100,
                max_energy INTEGER DEFAULT 100,
                last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT clicks, energy, max_energy FROM users WHERE user_id = ?", 
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"clicks": row[0], "energy": row[1], "max_energy": row[2]}
            
            # Если нового пользователя нет — создаем с 100 энергии
            await db.execute(
                "INSERT INTO users (user_id, clicks, energy, max_energy) VALUES (?, 0, 100, 100)", 
                (user_id,)
            )
            await db.commit()
            return {"clicks": 0, "energy": 100, "max_energy": 100}

async def add_click(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        user = await get_user(user_id)
        if user["energy"] > 0:
            new_clicks = user["clicks"] + 1
            new_energy = user["energy"] - 1
            await db.execute(
                "UPDATE users SET clicks = ?, energy = ? WHERE user_id = ?", 
                (new_clicks, new_energy, user_id)
            )
            await db.commit()
            return {"clicks": new_clicks, "energy": new_energy, "max_energy": user["max_energy"]}
        return user

async def get_top_players(limit: int = 10):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT user_id, clicks FROM users ORDER BY clicks DESC LIMIT ?", 
            (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [{"user_id": row[0], "clicks": row[1]} for row in rows]