# Базовый образ
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем только файлы Poetry для кэширования зависимостей на этапе сборки
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости без создания виртуального окружения (оно не нужно в контейнере)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем весь проект
COPY . .

# Указываем порт для приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]