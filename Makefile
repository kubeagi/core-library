
.PHONY: lint
lint:
	@python -m pip install --upgrade pip
	@python -m pip install -e './libs/core/.[dev]'
	@pylint -d all -e E0602 ./libs/
	@black .