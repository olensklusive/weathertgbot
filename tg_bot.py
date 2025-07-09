import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = '7776255848:AAGVPHlKM43SFUBHLgn4MoQS0OTwtw3baAQ'
WEATHER_API_KEY = 'a61019d898eb1475d0762593c6196ddb'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/forecast'


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

        for forecast in data['list'][::8]:  # Берем прогноз на каждый день
            date = forecast['dt_txt']
            temp = forecast['main']['temp']
            desc = forecast['weather'][0]['description']
            weather_info += f"📅 {date}\n🌡 {temp}°C, {desc.capitalize()}\n\n"

        await update.message.reply_text(weather_info)

    except Exception as e:
        await update.message.reply_text("Ошибка. Попробуйте позже.")
        print(f"Error: {e}")


if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))

    app.run_polling()