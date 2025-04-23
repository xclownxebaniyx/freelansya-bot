import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Конфигурация
TOKEN = "8012249971:AAHNFX7sk0M5ADWgIWSnBlqCR-WhXhduczE"
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "supersecret"
WEBHOOK_URL = f"https://freelansya-bot.onrender.com{WEBHOOK_PATH}"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик сообщений
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer("Привет, я ФрилансЯ. Скоро начну присылать тебе заказы!")

# Webhook-хуки
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()

# aiohttp-приложение
async def create_app():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot, on_startup=on_startup, on_shutdown=on_shutdown)
    return app

# Запуск приложения
if __name__ == "__main__":
    web.run_app(
        create_app(),
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000))
    )
