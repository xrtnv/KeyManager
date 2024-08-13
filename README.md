# One-Time Secret API

## Описание

API сервис для создания и получения одноразовых секретов.

## Установка и запуск

1. Клонируйте репозиторий:
    ```sh
    git clone <repository_url>
    cd KeyManager
    ```

2. Создайте файл `.env` и добавьте необходимые переменные окружения:
    ```env
    SECRET_KEY=<your_secret_key>
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    MONGODB_URL=mongodb://mongo:27017
    ```

3. Запустите Docker Compose:
    ```sh
    docker-compose up --build
    ```

4. Откройте браузер и перейдите по адресу `http://localhost:8000/docs` для просмотра документации API.