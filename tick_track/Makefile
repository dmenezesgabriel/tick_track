requirements:
	pipenv lock --requirements > requirements.txt

run-prod:
	export ENVIRONMENT=production; \
	pipenv run python __main__.py

run-dev:
	export ENVIRONMENT=development; \
	pipenv run python __main__.py

migrate:
	export ENVIRONMENT=production; \
	export DATABASE_PATH=./database/database_prod.db; \
	pipenv run python ./database/migrations.py

run-test:
	export ENVIRONMENT=testing; \
	pipenv run python -m pytest -s