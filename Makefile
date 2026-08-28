.PHONY: install test test-postgres test-opensearch test-dashboards test-client-data check-opensearch report open-report serve-report up down clean clean-cache

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

test-client-data:
	$(PYTHON) -m pytest -m client_data

check-opensearch:
	@set -a && . ./.env && set +a && scheme=http; if [ "$$OPENSEARCH_USE_SSL" = "true" ]; then scheme=https; fi; host="$(if $(TARGET_HOST),$(TARGET_HOST),$$OPENSEARCH_HOST)"; curl -vk --connect-timeout 10 -u "$$OPENSEARCH_USER:$$OPENSEARCH_PASSWORD" "$$scheme://$$host:$$OPENSEARCH_PORT/"

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

clean-cache:
	rm -rf .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
