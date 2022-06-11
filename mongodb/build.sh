#!/usr/bin/env bash

TAG=latest
IP=419492045574.dkr.ecr.eu-central-1.amazonaws.com

docker build -t plant2win_db:${TAG} .
docker tag plant2win_db:${TAG} ${IP}/plant2win_db:${TAG}
docker push ${IP}/plant2win_db:${TAG}