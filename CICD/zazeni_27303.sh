#!/bin/bash

# Pull the latest version of the image from DockerHub
docker pull $DOCKER_USERNAME/myapp:latest

# Run the Docker container
docker run -d -p 80:80 $DOCKER_USERNAME/myapp:latest
