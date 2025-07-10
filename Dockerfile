FROM python:3.10-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем файлы
COPY . .

# Установка зависимостей Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Запуск бота
CMD ["python", "tg_bot.py"]
