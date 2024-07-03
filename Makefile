.PHONY: install
install: install_python_deps install_node_deps setup_husky

.PHONY: install_python_deps
install_python_deps:
	pip3 install -r requirements.txt

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

.PHONY: run
run:
	python3 src/main.py

.PHONY: setup
setup:
	python3 setup.py

.PHONY: before_commit
before_commit: lint_text
