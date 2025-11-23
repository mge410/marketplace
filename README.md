# marketplace

Сервис представляет собой простой механизм для управления постами

Инструкция для развертки проекта:  
Проект разворачивается при помощи docker.

1. Копируем .env.example и создаём файл .env
2. В папке certs нужно создать 2 файла - `jwt-private.pem` и `jwt-public.pem`. В файле Makefile есть команды для генерации этих файлов `gen-public-rsa` и `gen-private-rsa`
3. Запускаем docker-compose up -d
4. Входим в docker контейнер `docker exec -it backend /bin/bash` и применяем миграции `alembic upgrade head`
5. Для использования localstack нужно создать bucket `docker exec -it localstack awslocal s3 mb s3://dev`
6. На http://localhost:8000 будет проект

Список endpoint можно будет посмотреть тут, после развертки проекта

http://localhost:8000/docs
