# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY . .

# Устанавливаем переменную окружения, чтобы Python не буферизовал вывод
ENV PYTHONUNBUFFERED=1

# Команда для запуска бота
CMD ["python", "main.py"]
