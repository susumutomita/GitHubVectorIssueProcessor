.PHONY: install
install:
	npm install

.PHONY: setup_husky
setup_husky:
	npm run prepare

.PHONY: clean
clean:
	npm run clean

.PHONY: lint
lint:
	black . --check
	isort . --check
	cd src && pylint . --rcfile=../.pylintrc
	yamllint -c .yamllint .
	flake8 .

.PHONY: lint_text
lint_text:
	npm run lint:text

.PHONY: lint_text_fix
lint_text_fix:
	npm run lint:text:fix

.PHONY: format
format:
	black .
	isort .

.PHONY: before_commit
before_commit: lint_text
