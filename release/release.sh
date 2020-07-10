#!/bin/sh

VERSION_FILE_PATH="./VERSION"
DOCKER_REGISTRY="docker.io"

function docker_tag_exists() {
  curl --silent -f -lSL https://index.${DOCKER_REGISTRY}/v1/repositories/$1/tags/$2 > /dev/null 2>&1
}

function log_stdout() {
  echo "$(date) => $1"
}

function log_stderr() {
  echo "$(date) => $1" >&2
}

log_stdout "Finding version information"
if [[ -f "$VERSION_FILE_PATH" ]]; then
  VERSION="$(egrep -v '^$|^#' $VERSION_FILE_PATH)"
else
  log_stderr "File $VERSION_FILE_PATH does not exist. Please, create it"
  exit 1
fi

START_WITH="${VERSION:0:1}"
if [[ "$START_WITH" != "v" ]]; then
  log_stderr "The version must start with v. Found $START_WITH. Please, fix the version format in the file $VERSION_FILE_PATH"
  exit 1
fi

if docker_tag_exists thiagonache/flask-simple-api ${VERSION}; then
  log_stderr "Docker image tag ${VERSION} already exists. Please, increment the version in file $VERSION_FILE_PATH"
  exit 1
fi

echo "Building version is $VERSION"

docker build --pull -t thiagonache/flask-simple-api:${VERSION} .
if [[ "$?" != 0 ]]; then
  echo "Cannot build image"
  exit 1
fi

docker push thiagonache/flask-simple-api:${VERSION}
if [[ "$?" != 0 ]]; then
  echo "Cannot push image"
  exit 1
fi
