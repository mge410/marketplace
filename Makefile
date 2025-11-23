# ===============================
# Настройки проекта
# ===============================
# Каталоги с кодом/тестами
PY_SRCS=src

# Порог для Radon:
# - запрещаем функции со сложностью CC уровней E/F
# - минимальный Maintainability Index (MI)
RADON_MIN_MI=45

# ===============================
# Служебные цели
# ===============================
.PHONY: help install lint fmt type security cc mi hal raw check

help:
	@echo "Доступные цели:"
	@echo " lint       - ruff check (с автофиксом)"
	@echo " fmt        - ruff format"
	@echo " type       - mypy (проверка типов)"
	@echo " security   - bandit (скан безопасности)"
	@echo " cc         - radon cc (цикломатическая сложность) + quality gate"
	@echo " mi         - radon mi (индекс поддерживаемости) + quality gate"
	@echo " hal        - radon hal (метрика Халстеда)"
	@echo " raw        - radon raw (SLOC, LLOC, комментарии, число функций/классов)"
	@echo " check      - быстрый локальный quality gate (ruff+mypy+bandit+radon)"

# ===============================
# Ruff: линт и форматирование
# ===============================
lint:
	uv run ruff check $(PY_SRCS) --fix

fmt:
	uv run ruff format $(PY_SRCS)

# ===============================
# Mypy: проверка типов
# ===============================
type:
	uv run mypy $(PY_SRCS)

# ===============================
# Bandit: анализ безопасности
# ===============================
security:
	# -r: рекурсивно, -lll: максимум строгости вывода, -x: исключения
	uv run bandit -r $(PY_SRCS) -lll -x .venv,venv,build,dist,migrations

# ===============================
# Radon: метрики
# ===============================
# Цикломатическая сложность: подробный вывод (-s), среднее (-a)
cc:
	uv run radon cc -s -a $(PY_SRCS)
	@# QUALITY GATE: проваливаем, если есть элементы со сложностью E/F
	@if uv run radon cc -s $(PY_SRCS) | awk '{print $$5}' | grep -E '^[EF]$$'; then \
		echo "❌ Radon CC: обнаружены функции со сложностью E/F"; \
		exit 1; \
	else \
		echo "✅ Radon CC: нет функций с E/F"; \
	fi

# Индекс поддерживаемости
mi:
	uv run radon mi -s $(PY_SRCS)
	@# QUALITY GATE: проваливаем, если есть MI < $(RADON_MIN_MI)
	@MI_BAD=$$(uv run radon mi -s $(PY_SRCS) | awk -v min=$(RADON_MIN_MI) '{match($$0, /\(([0-9]+\.[0-9]+)\)$$/); mi_value = substr($$0, RSTART+1, RLENGTH-2); if(mi_value+0 < min) print $$0}'); \
	if [ -n "$$MI_BAD" ]; then \
		echo "❌ Radon MI: найдено файлов с MI < $(RADON_MIN_MI):"; \
		echo "$$MI_BAD"; \
		exit 1; \
	else \
		echo "✅ Radon MI: все файлы с MI >= $(RADON_MIN_MI)"; \
	fi

# Метрика Халстеда
hal:
	uv run radon hal $(PY_SRCS)

# Метрика Raw
raw:
	uv run radon raw $(PY_SRCS)

# ===============================
# Комплексные цели
# ===============================
# Локальный быстрый прогон с автофиксом Ruff
check: lint fmt type security cc mi hal raw

# ===============================
# Docker управление
# ===============================
up:
	docker compose up -d
down:
	docker compose down
rebuild:
	docker compose build --no-cache
	docker compose up -d
in:
	docker exec -it backend /bin/bash
make-bucket:
	docker exec -it localstack awslocal s3 mb s3://dev
gen-public-rsa:
	openssl genrsa -out jwt-private.pem 2048
gen-private-rsa:
	openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
