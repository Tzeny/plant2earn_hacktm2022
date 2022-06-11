#!/usr/bin/env bash

IP=419492045574.dkr.ecr.eu-central-1.amazonaws.com
TAG=latest

docker build -t plant2win_nginx:${TAG}  .
docker tag plant2win_nginx:${TAG} ${IP}/plant2win_nginx:${TAG}
docker push ${IP}/plant2win_nginx:${TAG}
