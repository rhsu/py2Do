test:
	python -m pytest -vv test/

task-test:
	python -m pytest -vv test/test_tasks.py

status-test:
	python -m pytest -vv test/test_statuses.py

db-reset:
	python db_reset.py

run:
	python run.py

.PHONY: test run tasks-test db_reset
