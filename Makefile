.PHONY: install test test-postgres report open-report serve-report up down clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest

test-postgres:
	pytest -m postgres

report:
	pytest

open-report:
	xdg-open reports/test-report.html

serve-report:
	python -m http.server 8000 --directory reports

up:
	docker compose up -d postgres

down:
	docker compose down

clean:
	rm -rf .pytest_cache reports/test-report.html
