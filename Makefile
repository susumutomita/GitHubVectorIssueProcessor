.PHONY: install
install: install_python_deps install_node_deps setup_husky

.PHONY: install_python_deps
install_python_deps:
	pip3 install -r requirements.txt
	pip3 install .

.PHONY: install_node_deps
install_node_deps:
	npm install

.PHONY: setup_husky
setup_husky:
	npm run prepare

.PHONY: clean
clean:
	npm run clean

.PHONY: lint
lint:
	black app/ --check
	isort app/ --check-only
	cd app && pylint . --rcfile=../.pylintrc
	yamllint -c .yamllint .
	flake8 app/

.PHONY: lint_text
lint_text:
	npm run lint:text

.PHONY: lint_text_fix
lint_text_fix:
	npm run lint:text:fix

.PHONY: format
format:
	black app/
	isort .

.PHONY: run
run:
	github-vector-issue-processor

.PHONY: before_commit
before_commit: format lint lint_text
