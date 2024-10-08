#!/bin/bash

# Set variables
IMAGE_NAME="velib-image"
CONTAINER_NAME="velib-container"
MONGO_IMAGE="mongo:latest"
MONGO_CONTAINER_NAME="velib-mongo"

# Build the Docker image
echo "Building Docker image..."
sudo docker build -t $IMAGE_NAME .

# Stop and remove any existing Velib container with the same name
echo "Stopping and removing existing Velib container..."
sudo docker stop $CONTAINER_NAME || true
sudo docker rm $CONTAINER_NAME || true

# Stop and remove any existing MongoDB container with the same name
echo "Stopping and removing existing MongoDB container..."
sudo docker stop $MONGO_CONTAINER_NAME || true
sudo docker rm $MONGO_CONTAINER_NAME || true

# Run the MongoDB container
echo "Running MongoDB container..."
sudo docker run -d --name $MONGO_CONTAINER_NAME -p 27018:27017 mongo:latest

# Run the Docker container for Velib
echo "Running Docker container for Velib..."
sudo docker run -d --name $CONTAINER_NAME --link $MONGO_CONTAINER_NAME:mongo $IMAGE_NAME

echo "Docker containers are running."
