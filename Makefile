UP := true

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) |  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: install
install: ## Install all dependencies
	@poetry install
	@poetry run pre-commit install


.PHONY: up
up: ## Up project containers
	@docker-compose -f docker-compose.base.yaml -f docker-compose.local.yaml up -d


.PHONY: down
down: ## Down project containers
	@docker-compose -f docker-compose.base.yaml -f docker-compose.local.yaml down


.PHONY: run
run: ## Start project app on 8080 port
	@poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload


start: up run ## Alias to make up and make start


.PHONY: deploy
deploy: ## Deploy project on the server
	@poetry run ansible-playbook -i ${DEPLOY_HOST}, -u ${DEPLOY_USER} --become  -e "deploy_project_path=${DEPLOY_PROJECT_PATH} app_image_url=${APP_IMAGE_URL}" deploy.yaml


.PHONY: autoflake_format
autoflake_format: ## Format project with autoflake
	@poetry run autoflake ./app ./tests


.PHONY: isort_format
isort_format: ## Format project with isort
	@poetry run isort ./app ./tests


.PHONY: black_format
black_format: ## Format project with black
	@poetry run black ./app ./tests


format: autoflake_format isort_format black_format ## Alias to run all formats


.PHONY: autoflake_lint
autoflake_lint: ## Check project with autoflake
	@poetry run autoflake --quiet --check ./app ./tests


.PHONY: isort_lint
isort_lint: ## Check project with isort
	@poetry run isort --check-only ./app ./tests


.PHONY: black_lint
black_lint: ## Check project with black
	@poetry run black --check ./app ./tests


.PHONY: pyright_lint
pyright_lint: ## Check project with pyright
	@poetry run pyright ./app ./tests


.PHONY: flake8_lint
flake8_lint: ## Check project with flake8
	@poetry run flake8 ./app ./tests


lint: autoflake_lint isort_lint black_lint pyright_lint flake8_lint ## Alias to run all lints


.PHONY: test
test: ## Run project tests
	@if [ ${UP} != "false" ]; then\
		make up;\
    fi
	@poetry run pytest ./tests
