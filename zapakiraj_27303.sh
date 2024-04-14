#!/bin/bash

# Exit immediately if a command exits with a non-zero status and for any failures in pipelines.
set -eo pipefail

# Assign command line arguments to variables 
DOCKER_USERNAME="$1"
GITHUB_SHA="$2"

# Print variables for debugging (make sure to remove or obfuscate sensitive data in production!)
echo "DOCKER_USERNAME: ${DOCKER_USERNAME}"
echo "GITHUB_SHA: ${GITHUB_SHA}"

# Check if variables are set
if [ -z "$DOCKER_USERNAME" ]; then
    echo "DOCKER_USERNAME is not set. Exiting..."
    exit 1
fi

if [ -z "$GITHUB_SHA" ]; then
    echo "GITHUB_SHA is not set. Exiting..."
    exit 1
fi

# Build, tag, and push the Docker image
docker build -t ${DOCKER_USERNAME}/myapp:${GITHUB_SHA} .
docker tag ${DOCKER_USERNAME}/myapp:${GITHUB_SHA} ${DOCKER_USERNAME}/myapp:latest
docker push ${DOCKER_USERNAME}/myapp:latest

echo "Docker image pushed successfully!"