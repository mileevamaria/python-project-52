install:
	uv sync
lint:
	uv run ruff check task_manager
test:
	pytest
build:
	./build.sh

dev:
	uv run manage.py runserver
render-start:
	make collectstatic && make migrate && gunicorn task_manager.wsgi
migrate:
	python3 manage.py migrate
makemigrations:
	python3 manage.py makemigrations
collectstatic:
	python3 manage.py collectstatic --noinput
    
shell-rec:
	asciinema rec demo.cast
shell-upload:
	upload demo.cast