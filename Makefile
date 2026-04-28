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
	gunicorn task_manager.wsgi
migrate:
	python manage.py migrate
makemigrations:
	python manage.py makemigrations
collectstatic:
	python manage.py collectstatic --noinput
    
shell-rec:
	asciinema rec demo.cast
shell-upload:
	upload demo.cast