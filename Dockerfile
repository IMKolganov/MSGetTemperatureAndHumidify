# Используйте официальный образ Python
FROM python:3.9-slim

# Установите рабочую директорию
WORKDIR /app

# Установите curl и другие зависимости
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Скачайте wait-for-it
RUN curl -sSLO https://github.com/vishnubob/wait-for-it/releases/download/v0.1.7/wait-for-it.sh && \
    chmod +x wait-for-it.sh && \
    mv wait-for-it.sh /usr/local/bin/wait-for-it

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

# Определите команду для запуска приложения с wait-for-it
CMD ["wait-for-it", "rabbitmq:5672", "--", "python", "run.py"]