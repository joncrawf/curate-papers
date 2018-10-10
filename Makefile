.DEFAULT_GOAL := help

build: test qbuild ## Build dockerfile for running commands

qbuild:
	@docker build -t joncrawf/curate-papers .

test: ## Test code
	@docker run --rm -v $(shell pwd):/code joncrawf/pylint curate_papers/**.py --disable=missing-docstring

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
