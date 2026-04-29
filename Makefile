install:
	uv sync
lint:
	uv run ruff check task_manager
test:
	uv run python3 manage.py test
test-coverage:
	uv run python3 -m coverage run manage.py test && uv run python3 -m coverage xml
build:
	./build.sh

dev:
	uv run python3 manage.py runserver
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