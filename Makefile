up:
	docker compose up -d
down:
	docker compose down
in:
	docker exec -it backend /bin/bash
make-migration:
	alembic revision --autogenerate
migrate:
	alembic upgrade head
ruff-format:
	uv run ruff format .
ruff-check-fix:
	uv run ruff check . --fix
ruff-check:
	uv run ruff check .
make-bucket:
	docker exec -it localstack awslocal s3 mb s3://dev
gen-public-rsa:
	openssl genrsa -out jwt-private.pem 2048
gen-private-rsa:
	openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
