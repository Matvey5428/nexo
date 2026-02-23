import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# Токен твоего бота
BOT_TOKEN = "8613625963:AAEbL9d5GQNmTy1xXgjh-dJq0IJ2m8aJ8SA"

# Ссылка на твой сайт
WEB_APP_URL = "https://matvey5428.github.io/nexo/"

# Создаём объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хэндлер для команды /start
@dp.message()
async def handle_start(message: types.Message):
    if message.text == "start":
        web_app = WebAppInfo(url=WEB_APP_URL)
        button = InlineKeyboardButton(text="Торговать", web_app=web_app)
        keyboard = InlineKeyboardMarkup().add(button)
        await message.answer("нажмите торговать", reply_markup=keyboard)

# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())