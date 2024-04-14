#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Load Docker environment variables, if any
if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# Build the Docker image
docker build -t myapp:${GITHUB_SHA} .

# Tag the image for the repository on DockerHub
docker tag myapp:${GITHUB_SHA} $DOCKER_USERNAME/myapp:latest

# Push the image to DockerHub
docker push $DOCKER_USERNAME/myapp:latest
