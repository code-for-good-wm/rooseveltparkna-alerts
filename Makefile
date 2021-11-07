ifdef CIRCLECI
	RUN := poetry run
else ifdef HEROKU_APP_NAME
	SKIP_INSTALL := true
else
	RUN := poetry run
endif

.PHONY: all
all: install

.PHONY: ci
ci: check test ## CI | Run all validation targets

.PHONY: watch
watch: install ## CI | Rerun all validation targests in a loop
	@ rm -rf $(FAILURES)
	$(RUN) sniffer

# SYSTEM DEPENDENCIES #########################################################

.PHONY: doctor
doctor: ## Check for required system dependencies
	bin/verchew --exit-code

.envrc:
	echo export SECRET_KEY=local >> $@
	echo export DATABASE_URL=postgresql://localhost/rpna_dev >> $@
	echo export REDIS_URL=redis://127.0.0.1:6379/0 >> $@
	echo >> $@
	echo export TWILIO_ACCOUNT_SID=??? >> $@
	echo export TWILIO_AUTH_TOKEN=??? >> $@
	- direnv allow

# PROJECT DEPENDENCIES ########################################################

VIRTUAL_ENV ?= .venv

BACKEND_DEPENDENCIES = $(VIRTUAL_ENV)/.poetry-$(shell bin/checksum pyproject.toml poetry.lock)
FRONTEND_DEPENDENCIES =

.PHONY: install
ifndef SKIP_INSTALL
install: $(BACKEND_DEPENDENCIES) $(FRONTEND_DEPENDENCIES) ## Install project dependencies
endif

$(BACKEND_DEPENDENCIES): poetry.lock runtime.txt requirements.txt
	@ rm -rf $(VIRTUAL_ENV)/.poetry-*
	@ poetry config virtualenvs.in-project true
	poetry install
	@ mkdir -p staticfiles
	@ touch $@

ifndef CI
poetry.lock: pyproject.toml
	poetry lock --no-update
	@ touch $@
runtime.txt: .python-version
	echo "python-$(shell cat $<)" > $@
requirements.txt: poetry.lock
	poetry export --format requirements.txt --output $@ --without-hashes
endif

$(FRONTEND_DEPENDENCIES):
	@ touch $@

.PHONY: clean
clean:
	rm -rf staticfiles
	rm -rf .coverage htmlcov

.PHONY: clean-all
clean-all: clean
	rm -rf $(VIRTUAL_ENV)

# RUNTIME DEPENDENCIES ########################################################

.PHONY: migrations
migrations: install  ## Database | Generate database migrations
	$(RUN) python manage.py makemigrations

.PHONY: migrate
migrate: install ## Database | Run database migrations
	$(RUN) python manage.py migrate

.PHONY: data
data: install migrate ## Database | Seed data for manual testing
	$(RUN) python manage.py gendata

.PHONY: reset
reset: install ## Database | Create a new database, migrate, and seed it
	- dropdb rpna_dev
	- createdb rpna_dev
	make data

# VALIDATION TARGETS ##########################################################

PYTHON_PACKAGES := config rpna
FAILURES := .cache/v/cache/lastfailed

.PHONY: check
check: check-backend ## Run static analysis

.PHONY: format
format: format-backend

.PHONY: check-backend
check-backend: install format-backend
	$(RUN) mypy $(PYTHON_PACKAGES) tests
	$(RUN) pylint $(PYTHON_PACKAGES) tests --rcfile=.pylint.ini

.PHONY: check-frontend
check-frontend: install

format-backend: install
	$(RUN) isort $(PYTHON_PACKAGES) tests
	$(RUN) black $(PYTHON_PACKAGES) tests

.PHONY: test
test: test-backend test-frontend ## Run all tests

.PHONY: test-backend
test-backend: test-backend-all

.PHONY: test-backend-unit
test-backend-unit: install
	@ ( mv $(FAILURES) $(FAILURES).bak || true ) > /dev/null 2>&1
	$(RUN) pytest $(PYTHON_PACKAGES) tests/unit -m "not django_db"
	@ ( mv $(FAILURES).bak $(FAILURES) || true ) > /dev/null 2>&1

.PHONY: test-backend-integration
test-backend-integration: install
	@ if test -e $(FAILURES); then $(RUN) pytest tests/integration; fi
	@ rm -rf $(FAILURES)
	$(RUN) pytest tests/integration

.PHONY: test-backend-all
test-backend-all: install
	@ if test -e $(FAILURES); then $(RUN) pytest $(PYTHON_PACKAGES) tests/unit tests/integration; fi
	@ rm -rf $(FAILURES)
	$(RUN) pytest $(PYTHON_PACKAGES) tests/unit tests/integration

.PHONY: test-frontend
test-frontend: test-frontend-unit

.PHONY: test-frontend-unit
test-frontend-unit: install

.PHONY: test-system
test-system: install
	$(RUN) honcho start --procfile=tests/system/Procfile --env=tests/system/.env

# SERVER TARGETS ##############################################################

.PHONY: run
run: .envrc install migrate ## Run the applicaiton
	$(RUN) honcho start --procfile=Procfile.dev --port=$${PORT:-8000}

.PHONY: run-production
run-production: .envrc install
	poetry run python manage.py collectstatic --no-input
	poetry run heroku local release
	HEROKU_APP_NAME=local poetry run heroku local web --port=$${PORT:-8000}

# DOCUMENTATION TARGETS #######################################################

.PHONY: translations
translations: install
	poetry run django-admin makemessages --locale es

.PHONY: uml
uml: install
	poetry install --extras uml
	@ echo
	poetry run pyreverse rpna -p rpna -a 1 -f ALL -o png --ignore admin.py,migrations,management,tests
	mv -f classes_rpna.png docs/classes.png
	mv -f packages_rpna.png docs/packages.png
	poetry run python manage.py graph_models alerts --group-models --output=docs/tables.png --exclude-models=TimeStampedModel

# RELEASE TARGETS #############################################################

.PHONY: build
build: install

.PHONY: promote
promote: install
	TEST_SITE=https://staging.rpna.com $(RUN) pytest tests/system --cache-clear
	heroku pipelines:promote --app rpna-staging --to rpna
	TEST_SITE=https://rpna.com $(RUN) pytest tests/system

# HELP ########################################################################

.PHONY: help
help: all
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
