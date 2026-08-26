.PHONY: install test test-postgres report up down clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest

test-postgres:
	pytest -m postgres

report:
	allure serve reports/allure-results

up:
	docker compose up -d postgres

down:
	docker compose down

clean:
	rm -rf .pytest_cache reports/allure-results/* reports/allure-report/*
