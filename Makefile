# Default RERANKING Model is BAAI/bge-reranker-large from huggingface
export RERANKING_MODEL_PATH ?= BAAI/bge-reranker-large

.PHONY: lint
lint:
	@python -m pip install --upgrade pip
	@python -m pip install -e './libs/core/.[dev]'
	@pylint -d all -e E0602 ./libs/
	@black .

.PHONY: install
install:
	@pip install -e libs/core/
	@pip install -e 'libs/cli/.[server, core, eval]'

install-eval:
	@pip install -e 'libs/cli/.[eval]'

install-server:
	@pip install -e 'libs/cli/.[server]'

.PHONY: server
server: install
	@kubeagi-cli serve



