# Используйте официальный образ Python
FROM python:3.9-slim

# Установите рабочую директорию
WORKDIR /app

# Установите curl и загрузите wait-for-it.sh
RUN apt-get update && apt-get install -y curl \
    && curl -o /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it.sh

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
CMD ["wait-for-it.sh", "rabbitmq:5672", "--", "python", "run.py"]