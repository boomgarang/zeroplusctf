# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы в рабочую директорию
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем flag.txt в корень контейнера
COPY flag.txt /flag.txt

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=main.py

# Открываем порт 1234 для Flask
EXPOSE 1234

# Команда для запуска приложения
CMD ["flask", "run", "--host=0.0.0.0", "--port=1234"]
