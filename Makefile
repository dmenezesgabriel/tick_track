run-prod:
	export ENVIRONMENT=production; \
	python3 tick_track/__main__.py

run-dev:
	export ENVIRONMENT=development; \
	python3 tick_track/__main__.py

migrate:
	export ENVIRONMENT=production; \
	export DATABASE_PATH=tick_track/database/database_prod.db; \
	python3 tick_track/database/migrations.py

run-test:
	export ENVIRONMENT=testing; \
	python3 -m pytest -s