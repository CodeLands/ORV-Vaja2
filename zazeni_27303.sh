#!/bin/bash

# Pull the latest version of the image from DockerHub
docker pull pckill3r/myapp:latest

# Run the Docker container with host display
docker run -d -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix pckill3r/myapp:latest