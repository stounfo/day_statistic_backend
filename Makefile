.PHONY: install
install:
	@poetry install
	@poetry run pre-commit install

.PHONY: start
start:
	@docker-compose -f docker-compose.base.yaml -f docker-compose.local.yaml up -d
	@poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080


.PHONY: stop
stop:
	@docker-compose -f docker-compose.base.yaml -f docker-compose.local.yaml down


deploy:
	@poetry run ansible-playbook -i ${DEPLOY_HOST}, -u ${DEPLOY_USER} --become  -e "deploy_project_path=${DEPLOY_PROJECT_PATH} app_image_url=${APP_IMAGE_URL}" deploy.yaml


.PHONY: black_format
black_format:
	poetry run black ./app ./tests


.PHONY: flake_format
flake_format:
	poetry run autoflake --recursive ./app ./tests


.PHONY: isort_format
isort_format:
	poetry run isort ./app ./tests


lint_format: black_format flake_format isort_format


.PHONY: black_check
black_check:
	poetry run black --check ./app ./tests


.PHONY: flake_check
flake_check:
	poetry run autoflake --recursive --check ./app ./tests


.PHONY: isort_check
isort_check:
	poetry run isort --check-only ./app ./tests


.PHONY: pyright_check
pyright_check:
	poetry run pyright ./app ./tests


lint_check: black_check flake_check isort_check pyright_check


.PHONY: test
test:
	poetry run pytest
