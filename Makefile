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
	black src/ --check
	isort src/ --check-only
	cd src && pylint . --rcfile=../.pylintrc
	yamllint -c .yamllint .
	flake8 src/

.PHONY: lint_text
lint_text:
	npm run lint:text

.PHONY: lint_text_fix
lint_text_fix:
	npm run lint:text:fix

.PHONY: format
format:
	black src/
	isort .

.PHONY: before_commit
before_commit: lint_text
