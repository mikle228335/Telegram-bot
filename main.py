import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "google/gemma-7b-it")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def ask_openrouter(user_text):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/Dymalken_bot",
        "X-Title": "TelegramBot"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": user_text}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                             headers=headers, json=data)

    if response.ok:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Ошибка от OpenRouter: {response.text}"

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("👋 Привет! Я бот Dymalken. Напиши мне что-нибудь, и я постараюсь ответить!")

@dp.message_handler()
async def handle_message(message: types.Message):
    await message.answer("⏳ Думаю...")
    reply = await ask_openrouter(message.text)
    await message.answer(reply)

if __name__ == "__main__":
    print("✅ Бот запущен…")
    executor.start_polling(dp, skip_updates=True)
