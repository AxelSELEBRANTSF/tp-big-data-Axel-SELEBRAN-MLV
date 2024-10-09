#!/bin/bash

# Set variables
IMAGE_NAME="velib-image"
CONTAINER_NAME="velib-container"
MONGO_IMAGE="mongo:latest"
MONGO_CONTAINER_NAME="velib-mongo"
NETWORK_NAME="velib-network"

# Build the Docker image
echo "Building Docker image..."
sudo docker build -t $IMAGE_NAME .

# Stop and remove any existing containers
echo "Stopping and removing existing containers..."
sudo docker stop $CONTAINER_NAME $MONGO_CONTAINER_NAME || true
sudo docker rm $CONTAINER_NAME $MONGO_CONTAINER_NAME || true

# Check if network exists, create if it doesn't
if ! sudo docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
    echo "Creating Docker network..."
    sudo docker network create $NETWORK_NAME
else
    echo "Network $NETWORK_NAME already exists."
fi

# Run the MongoDB container
echo "Running MongoDB container..."
sudo docker run -d --name $MONGO_CONTAINER_NAME --network $NETWORK_NAME -p 27018:27017 $MONGO_IMAGE

# Run the Docker container for Velib
echo "Running Docker container for Velib..."
sudo docker run -d --name $CONTAINER_NAME --network $NETWORK_NAME $IMAGE_NAME

echo "Docker containers are running on the $NETWORK_NAME network."