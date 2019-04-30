# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

.PHONY: release build run test get-version notebook

# Set the default target to be the help for this Makefile
.DEFAULT_GOAL: help
SHELL:=bash
PROJECT:=$(shell basename `pwd`)
DESC:="Demo push task to redis service"

PROJECT_VERSION:=$(shell sed -n '/version/,/version/p' setup.py | head -1 | awk -F'version=' '{ print $$2}' | awk -F',' '{print $$1}' | sed "s/^'\(.*\)'$$/\1/")

DOCKER_DEV_IMAGE:=python:3
DOCKER_VOLS:=-v `pwd`/dist:/usr/src/$(PROJECT) -w /usr/src/$(PROJECT)

NAMESPACE?="fd4b-demo"

include .env

help: # http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@echo $(PROJECT):$(PROJECT_VERSION)
	@echo "==========================================================="
	@echo $(DESC)
	@echo
	@echo The targets available in this project are:
	@grep -h -E '^[a-zA-Z0-9_%/-\.]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\t\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo

.env:
	@touch .env

env-%:
	@if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

clean:
	-@rm -r dist
	-@rm -r .specs



dist/$(PROJECT)-$(PROJECT_VERSION).tar.gz: ${shell find flaskform} setup.py
	@echo 'Building PIP package...'
	@mkdir -p dist/flaskform
	@cp setup.py dist/setup.py
	@echo $(PROJECT):$(PROJECT_VERSION) > dist/README
	@cp -R flaskform/* dist/flaskform
	@docker run -it --rm $(DOCKER_VOLS) $(DOCKER_DEV_IMAGE) bash -c 'cp -r . /tmp/src && \
			cd /tmp/src && \
			python setup.py -q sdist && \
			cd - && \
			cp -r /tmp/src/dist/*.tar.gz .'

build: ## Build docker image for service
build:
	@echo 'Building Docker image...'
	@docker build \
		--build-arg SERV=$(PROJECT) \
		--build-arg VERSION=$(PROJECT_VERSION) \
		-t $(PROJECT):$(PROJECT_VERSION) .


run-dev: ## Run the service for development by mounting the latest code on pre-built image
run-dev: dist/$(PROJECT)-$(PROJECT_VERSION).tar.gz .env
	@mkdir -p .work/data
	@docker run -it \
		-v "`pwd`/.work/data:/data" \
		-v `pwd`/dist/flaskform:/usr/local/lib/python3.6/site-packages/flaskform \
		--env-file .env $(PROJECT):$(PROJECT_VERSION)

run: #Runs onboarding service as docker container
run: .env
run:
	@docker run -it --env-file .env $(PROJECT):$(PROJECT_VERSION)

release: ## Creates a release by bumping versions, generating CHANGELOG updates, and tagging the project. Allowed values: major, minor, patch (this will increase the corresponding current release version number as .. by 1)
release: RELEASE_TYPE=patch
release:
	@rm -rf .release || true
	@mkdir .release
	$(eval NEW_VERSION := $(shell docker run -it --rm \
		-v `pwd`/setup.py:/usr/src/$(PROJECT)/setup.py \
		-w /usr/src/$(PROJECT) \
		$(DOCKER_DEV_IMAGE) \
		bash -c 'pip -q -q install bump && bump setup.py --$(RELEASE_TYPE)'))
	@echo Creating new release version: $(NEW_VERSION)
	@git log --oneline HEAD...`git rev-list -n 1 \`git describe --abbrev=0 --tags\`` | awk '{printf "* %s",$$1; $$1=" -"; print $$0;}' > .release/commit.log
	@git add CHANGELOG.md setup.py
	@git commit -m "Automated Release $(NEW_VERSION)"
	@echo "Release $(NEW_VERSION)"
	@git tag -a $(NEW_VERSION) -m "Release $(NEW_VERSION)"


release-if-not-auto-push: ##Checks if the commit was done automatically or not. Does a release if it was not automatically pushed.
release-if-not-auto-push:
	@./etc/scripts/deployment/releaseIfNotAutoPush.sh

release-push: ###Pushes committed changes and tags to github
release-push: BRANCH=master
release-push:
	@git push origin HEAD:$(BRANCH)
	@git push --tags

push: ## Pushes image to registry
push: env-DOCKER_REGISTRY_URL env-REGISTRY_TOKEN
	@echo 'Pushes image to the private docker registry registry'
	@docker tag  $(PROJECT):$(PROJECT_VERSION) $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(PROJECT_VERSION)
	@docker login -u token -p $(REGISTRY_TOKEN) $(DOCKER_REGISTRY_URL)
	@docker push $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(PROJECT_VERSION)
