# Используйте официальный образ Python
FROM python:3.9-slim

# Установите рабочую директорию
WORKDIR /app

# Копируйте зависимости и установите их
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируйте все файлы в рабочую директорию
COPY . .

# Установите переменные окружения
ENV FLASK_APP=run.py
ENV FLASK_ENV=docker

# Открываем порт 5000 для Flask
EXPOSE 5000

# Определите команду для запуска приложения
CMD ["python", "run.py"]