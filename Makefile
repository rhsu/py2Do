test:
	python -m pytest -v test/

tasks-test:
	python -m pytest -v test/test_tasks.py

db-reset:
	python db_reset.py

run:
	python run.py

.PHONY: test run tasks-test db_reset
