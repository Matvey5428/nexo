from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils import executor

# Токен твоего бота
BOT_TOKEN = "8613625963:AAFBGozcjBMJ6OyCbTC2GBvMxPTrFwfGYHo"

# Ссылка на твой сайт
WEB_APP_URL = "https://matvey5428.github.io/nexo/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    web_app = WebAppInfo(url=WEB_APP_URL)
    button = InlineKeyboardButton(text="Открыть мини-приложение", web_app=web_app)
    keyboard = InlineKeyboardMarkup().add(button)
    await message.answer("Привет! Нажми на кнопку ниже, чтобы открыть приложение:", reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)