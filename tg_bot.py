import threading
import time
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from http.server import HTTPServer, BaseHTTPRequestHandler

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/forecast'

# Фейковый веб-сервер для Render (требуется, чтобы не останавливался Web Service)
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running.")

def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('', port), PingHandler)
    server.serve_forever()

# Telegram handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}!\n"
        "Я покажу погоду на 5 дней. Просто напиши название города."
    )

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        response = requests.get(WEATHER_URL, params=params)
        data = response.json()

        if data['cod'] != '200':
            await update.message.reply_text("Город не найден. Попробуйте еще раз.")
            return

        weather_info = f"Погода в {city} на 5 дней:\n\n"

        for forecast in data['list'][::8]:
            date = forecast['dt_txt']
            temp = forecast['main']['temp']
            desc = forecast['weather'][0]['description']
            weather_info += f"📅 {date}\n🌡 {temp:.1f}°C, {desc.capitalize()}\n\n"

        await update.message.reply_text(weather_info)

    except Exception as e:
        await update.message.reply_text("Ошибка. Попробуйте позже.")
        print(f"Error: {e}")

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))
    app.run_polling()

if __name__ == '__main__':
    threading.Thread(target=start_web_server).start()
    run_bot()
