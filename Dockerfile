# Базовый образ с Python
FROM python:3.12-slim

# Установка зависимостей
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники бота
COPY . .

# Запуск бота
CMD ["python", "tg_bot.py"]
