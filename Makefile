SETTINGS_DEV=core.settings.dev


install_requirements:
	@echo "Installing requirements"
	pip install -r requirements.txt

run_makemigrations:
	@echo "Making Migration files"
	python src/manage.py makemigrations --settings=$(SETTINGS_DEV)

run_migrations:
	@echo "Running Migrations Docker"
	docker-compose run --rm api python src/manage.py migrate

build_app_docker:
	@echo "building API test server docker"
	docker-compose build

run_app_docker:
	@echo "starting API test server docker"
	docker-compose up

install_pre_commit: install_requirements
	@echo "Installing pre-commit"
	pre-commit install

run_tests:
	@echo "running tests docker"
	docker-compose run --rm api python src/manage.py test
