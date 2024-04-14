#!/bin/bash

# Exit immediately if a command exits with a non-zero status and for any failures in pipelines.
set -eo pipefail

# Assign command line arguments to variables
DOCKER_USERNAME="$1"
GITHUB_SHA="$2"

# Check if DOCKER_USERNAME is set
if [ -z "$DOCKER_USERNAME" ]; then
    echo "DOCKER_USERNAME is not set. Exiting..."
    exit 1
fi

# Check if GITHUB_SHA is set
if [ -z "$GITHUB_SHA" ]; then
    echo "GITHUB_SHA is not set. Exiting..."
    exit 1
fi

# Build the Docker image with the commit SHA as a tag
docker build -t myapp:${GITHUB_SHA} .

# Tag the image for the repository on DockerHub
docker tag myapp:${GITHUB_SHA} $DOCKER_USERNAME/myapp:latest

# Push the image to DockerHub
docker push $DOCKER_USERNAME/myapp:latest

echo "Docker image pushed successfully!"
