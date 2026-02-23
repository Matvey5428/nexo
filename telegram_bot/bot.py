import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command

BOT_TOKEN = "8613625963:AAEbL9d5GQNmTy1xXgjh-dJq0IJ2m8aJ8SA"
WEB_APP_URL = "https://matvey5428.github.io/nexo/"

# --- Подключение к базе ---
conn = sqlite3.connect('database.db')  # база рядом с bot.py
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    username TEXT,
    balance_usdt REAL DEFAULT 0,
    balance_rub REAL DEFAULT 0,
    trading_volume REAL DEFAULT 0,
    verified INTEGER DEFAULT 0
)
""")
conn.commit()

# --- Функции работы с пользователями ---
def add_user(telegram_id: int, username: str):
    cursor.execute(
        "INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)",
        (telegram_id, username)
    )
    conn.commit()

def get_user_balance(telegram_id: int):
    cursor.execute(
        "SELECT balance_usdt, balance_rub, trading_volume, verified FROM users WHERE telegram_id=?",
        (telegram_id,)
    )
    row = cursor.fetchone()
    if row:
        return {
            "usdt": row[0],
            "rub": row[1],
            "trading_volume": row[2],
            "verified": row[3]
        }
    return {"usdt": 0, "rub": 0, "trading_volume": 0, "verified": 0}

# --- Создание бота ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- /start ---
async def cmd_start(message: types.Message):
    add_user(message.from_user.id, message.from_user.username or "Unknown")
    web_app = WebAppInfo(url=WEB_APP_URL)
    button = InlineKeyboardButton(text="Торговать", web_app=web_app)
    keyboard = InlineKeyboardMarkup().add(button)
    await message.answer(
        "Добро пожаловать! Нажмите 'Торговать', чтобы открыть обмен.",
        reply_markup=keyboard
    )

# --- /balance ---
async def cmd_balance(message: types.Message):
    balance = get_user_balance(message.from_user.id)
    verified_text = "✅ Пройдено" if balance['verified'] else "❌ Не пройдено"
    text = (
        f"Ваш баланс:\n\n"
        f"RUB: {balance['rub']:.2f} ₽\n"
        f"USDT: {balance['usdt']:.2f} $\n\n"
        f"Объем торгов: {balance['trading_volume']:.2f} $\n"
        f"Верификация: {verified_text}"
    )
    await message.answer(text)

# --- Регистрация хэндлеров ---
dp.message.register(cmd_start, Command(commands=["start"]))
dp.message.register(cmd_balance, Command(commands=["balance"]))

# --- Запуск бота ---
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())