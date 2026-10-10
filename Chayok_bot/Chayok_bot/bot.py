import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Замени на свой токен от @BotFather
BOT_TOKEN = "7659480716:AAGALAkWV8r7ltBbfCrSx6Hpj8wozpeHUl0"

# Ссылку изменим позже, когда запустим ngrok
WEB_APP_URL = " https://chayok-bot.onrender.com" 

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Запустить кликер 🐹", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton(text="Заказать услуги 💬", url="https://t.me/Chayok_UKRAINE")]
    ])
    
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n\n"
        "Кликай, поднимай уровень и получай спины для рулетки с бонусами и скидками!",
        reply_markup=kb
    )

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())