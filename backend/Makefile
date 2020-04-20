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

migrate-testing:
	export ENVIRONMENT=testing; \
	export DATABASE_PATH=./tests/database_test.db; \
	pipenv run python ./database/migrations.py