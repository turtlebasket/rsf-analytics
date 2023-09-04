SHELL = /bin/bash
.DEFAULT_GOAL := run

dev:
	LOCAL_ENV=true pipenv run hypercorn main.py --reload

run:
	LOCAL_ENV=true pipenv run hypercorn main.py
