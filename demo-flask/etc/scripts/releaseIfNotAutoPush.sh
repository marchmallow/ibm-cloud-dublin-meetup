#!/bin/bash

#===============================================================
# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#===============================================================

#Script that checks if this is an automatied driven release. If so we don't need to trigger another build.
#Otherwise do make release to create a new release tag and version in the pom

echo ${TRAVIS_COMMIT_MESSAGE}
regex='^Automated Release [0-9]+\.[0-9]+\.[0-9]+.*$'
skip_release_regex='^SKIP RELEASE'
shopt -s nocasematch
if [[ "${TRAVIS_COMMIT_MESSAGE}" =~ $regex ]]; then
  echo "This is automated push to master. Do nothing."
elif [[ "${TRAVIS_COMMIT_MESSAGE}" =~ $skip_release_regex ]]; then
  echo "Not to perform release trigger was set. Do nothing."
else
  echo "Merged PR. Making a new release."
  make release
  echo "git remote set-url origin https://${GITHUB_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git"
  git remote set-url origin https://${GITHUB_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git
  make release-push
fi
