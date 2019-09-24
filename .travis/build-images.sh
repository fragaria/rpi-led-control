#!/bin/bash

# kudos https://dev.to/zeerorg/build-multi-arch-docker-images-on-travis-5428

DIR=`dirname "$0"`

echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin
docker info

# Build for armhf and push
buildctl build --frontend dockerfile.v0 \
            --local dockerfile=. \
            --local context=. \
            --output type=image,name=docker.io/fragaria/rpi-led-control:latest-amd64,push=true \
            --opt platform=linux/amd64 \
            --opt filename=./Dockerfile


buildctl build --frontend dockerfile.v0 \
            --local dockerfile=. \
            --local context=. \
            --output type=image,name=docker.io/fragaria/rpi-led-control:latest-armhf,push=true \
            --opt platform=linux/armhf \
            --opt filename=./Dockerfile


export DOCKER_CLI_EXPERIMENTAL=enabled

# Create manifest list and push that
docker manifest create fragaria/rpi-led-control:latest \
            fragaria/rpi-led-control:latest-amd64 \
            fragaria/rpi-led-control:latest-armhf

docker manifest annotate fragaria/rpi-led-control:latest fragaria/rpi-led-control:latest-armhf --arch arm
docker manifest annotate fragaria/rpi-led-control:latest fragaria/rpi-led-control:latest-amd64 --arch amd64

docker manifest push fragaria/rpi-led-control:latest
