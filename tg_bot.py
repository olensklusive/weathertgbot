from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from get_weather import get_city_weather

TELEGRAM_TOKEN = '7776255848:AAGVPHlKM43SFUBHLgn4MoQS0OTwtw3baAQ'

user_states = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}!\n"
        "Напиши название города, чтобы я показал погоду на ближайшие дни."
    )


async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Проверка, уточняет ли пользователь страну
    if user_id in user_states and user_states[user_id].get('awaiting_country'):
        city = user_states[user_id]['city']
        country_code = text.upper()
        _, _, report = get_city_weather(city, country_code)
        user_states.pop(user_id)
        await update.message.reply_text(report)
        return

    # Обычный запрос города
    city_name, country, report = get_city_weather(text)

    if city_name is None:
        await update.message.reply_text(report)
    else:
        if text.lower() != city_name.lower():
            user_states[user_id] = {'awaiting_country': True, 'city': text}
            await update.message.reply_text(
                f"Уточните страну для города {text} (например: RU, US, KZ):"
            )
        else:
            await update.message.reply_text(report)


if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))
    app.run_polling()
