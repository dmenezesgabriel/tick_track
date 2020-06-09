
install-py:
	cd backend && pipenv install pipfile

migrate:
	(cd backend; make migrate)

run-prod:
	(cd backend; make run-prod) &
	(cd frontend; make run-prod)

run-dev:
	(cd backend; make run-dev) &
	(cd frontend; make run-dev)