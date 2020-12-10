
install-py:
	cd tick_track && pipenv install pipfile

migrate:
	(cd tick_track; make migrate)

run-prod:
	(cd tick_track; make run-prod) &
	(cd frontend; make run-prod)

run-dev:
	(cd tick_track; make run-dev) &
	(cd frontend; make run-dev)