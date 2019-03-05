test:
	python -m pytest -v test/

tasks-test:
	python -m pytest -v test/test_tasks.py

run:
	python run.py

.PHONY: test run tasks-test
