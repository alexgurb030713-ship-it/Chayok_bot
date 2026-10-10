import random
import aiosqlite

DB_NAME = "game.db"

async def init_db():
    """Создает таблицу пользователей при запуске."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                clicks INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                spins INTEGER DEFAULT 0,
                inventory TEXT DEFAULT ''
            )
        """)
        await db.commit()

async def get_or_create_user(user_id: int):
    """Возвращает данные игрока или создает нового."""
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
            if user:
                return dict(user)
            
            # Создаем нового пользователя
            await db.execute(
                "INSERT INTO users (user_id, clicks, level, spins, inventory) VALUES (?, 0, 1, 0, '')",
                (user_id,)
            )
            await db.commit()
            return {"user_id": user_id, "clicks": 0, "level": 1, "spins": 0, "inventory": ""}

async def process_click_db(user_id: int, count: int = 1):
    """Добавляет клики и повышает уровень каждые 50 кликов."""
    async with aiosqlite.connect(DB_NAME) as db:
        user = await get_or_create_user(user_id)
        new_clicks = user["clicks"] + count
        
        # Расчет уровня: каждые 50 кликов = +1 уровень и +1 прокрут рулетки
        new_level = (new_clicks // 50) + 1
        new_spins = user["spins"]
        
        if new_level > user["level"]:
            level_diff = new_level - user["level"]
            new_spins += level_diff # Даем по 1 прокруту за каждый новый уровень

        await db.execute(
            "UPDATE users SET clicks = ?, level = ?, spins = ? WHERE user_id = ?",
            (new_clicks, new_level, new_spins, user_id)
        )
        await db.commit()
        return {"clicks": new_clicks, "level": new_level, "spins": new_spins}

async def spin_roulette_db(user_id: int):
    """Крутит рулетку с процентами выпадания призов."""
    async with aiosqlite.connect(DB_NAME) as db:
        user = await get_or_create_user(user_id)
        
        if user["spins"] <= 0:
            return {"error": "Нет доступных прокрутов! Повышайте уровень."}
        
        # Список наград и их шансы (%)
        prizes = [
            "50 монет",
            "Скидка 10% на услуги",
            "Брейнрот (130+ млн)",
            "Бесплатная реклама в TG",
            "СУПЕР-ПРИЗ 🔥"
        ]
        weights = [60, 25, 10, 4.9, 0.1]
        
        won_prize = random.choices(prizes, weights=weights, k=1)[0]
        
        # Обновляем инвентарь и списываем 1 спин
        current_inv = user["inventory"]
        new_inv = f"{current_inv}, {won_prize}".strip(", ")
        new_spins = user["spins"] - 1
        
        await db.execute(
            "UPDATE users SET spins = ?, inventory = ? WHERE user_id = ?",
            (new_spins, new_inv, user_id)
        )
        await db.commit()
        
        return {"prize": won_prize, "spins_left": new_spins, "inventory": new_inv}