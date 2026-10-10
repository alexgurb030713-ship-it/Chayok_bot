import aiosqlite

DB_NAME = "game.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                level INTEGER DEFAULT 1,
                coins INTEGER DEFAULT 0,
                spins INTEGER DEFAULT 0,
                energy INTEGER DEFAULT 100,
                max_energy INTEGER DEFAULT 100
            )
        """)
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT level, coins, spins, energy, max_energy FROM users WHERE user_id = ?", 
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "level": row[0],
                    "coins": row[1],
                    "spins": row[2],
                    "energy": row[3],
                    "max_energy": row[4]
                }
            
            # Создаем нового игрока
            await db.execute(
                "INSERT INTO users (user_id, level, coins, spins, energy, max_energy) VALUES (?, 1, 0, 0, 100, 100)", 
                (user_id,)
            )
            await db.commit()
            return {"level": 1, "coins": 0, "spins": 0, "energy": 100, "max_energy": 100}

async def add_click(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        user = await get_user(user_id)
        if user["energy"] > 0:
            new_coins = user["coins"] + 1
            new_energy = user["energy"] - 1
            # Пример: каждые 50 монет повышают уровень
            new_level = 1 + (new_coins // 50)
            
            await db.execute(
                "UPDATE users SET coins = ?, energy = ?, level = ? WHERE user_id = ?", 
                (new_coins, new_energy, new_level, user_id)
            )
            await db.commit()
            return {
                "level": new_level,
                "coins": new_coins,
                "spins": user["spins"],
                "energy": new_energy,
                "max_energy": user["max_energy"]
            }
        return user

async def get_top_players(limit: int = 10):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT user_id, coins, level FROM users ORDER BY coins DESC LIMIT ?", 
            (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [{"user_id": row[0], "coins": row[1], "level": row[2]} for row in rows]
