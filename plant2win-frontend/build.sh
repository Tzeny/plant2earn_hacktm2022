#!/usr/bin/env bash

TAG=test123
ng build
IP=419492045574.dkr.ecr.eu-central-1.amazonaws.com
#IP=127.0.0.1:5000

docker build -t plant2win_app:${TAG} .
docker tag plant2win_app:${TAG} ${IP}/plant2win_app:${TAG}
docker push ${IP}/plant2win_app:${TAG}
