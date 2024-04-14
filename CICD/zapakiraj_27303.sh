#!/bin/bash

# Exit immediately if a command exits with a non-zero status and for any failures in pipelines.
set -eo pipefail

# Load Docker environment variables, if any
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Check if DOCKER_USERNAME is set
if [ -z "$DOCKER_USERNAME" ]; then
    echo "DOCKER_USERNAME is not set. Exiting..."
    exit 1
fi

# Build the Docker image with the commit SHA as a tag
docker build -t myapp:${GITHUB_SHA} .

# Tag the image for the repository on DockerHub
docker tag myapp:${GITHUB_SHA} $DOCKER_USERNAME/myapp:latest

# Push the image to DockerHub
docker push $DOCKER_USERNAME/myapp:latest

echo "Docker image pushed successfully!"
