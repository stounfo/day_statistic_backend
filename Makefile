.PHONY: master_check
master_check:
	@git remote update;
	@if [ $$(git log HEAD..origin/master --pretty=oneline | wc -l) -gt 0 ]; then \
	  echo "your branch is behind by master"; \
	  exit 1; \
	fi


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
