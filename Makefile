.PHONY: install test test-postgres test-opensearch test-dashboards report open-report serve-report up down clean

PYTHON ?= python3

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest

test-postgres:
	$(PYTHON) -m pytest -m postgres

test-opensearch:
	$(PYTHON) -m pytest -m opensearch

test-dashboards:
	$(PYTHON) -m pytest -m dashboards

report:
	$(PYTHON) -m pytest

open-report:
	xdg-open reports/test-report.html

serve-report:
	$(PYTHON) -m http.server 8000 --directory reports

up:
	docker compose up -d postgres opensearch

down:
	docker compose down

clean:
	rm -rf .pytest_cache reports/test-report.html
