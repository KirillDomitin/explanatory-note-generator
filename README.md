v0.1.0 добавил простой фронтенд

docker compose up --build

docker compose exec auth_service alembic upgrade head

docker compose exec auth_service python -m src.scripts.create_admin