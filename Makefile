SHELL = /bin/sh

.DEFAULT_GOAL := help

RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(RUN_ARGS):;@:)

docker_bin := $(shell command -v docker 2> /dev/null)
docker_compose_bin := $(shell command -v docker-compose 2> /dev/null)
pwd := $(shell pwd)

help: ## Show this help
        @awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Start container (in background)
        docker build -t test_task .
        docker run --name test_task -v $(pwd)/web:/web -d -p 8080:8080 test_task
        docker logs -f test_task

down: ## Stop container
        docker stop test_task
        docker rm test_task