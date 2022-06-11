#IP=127.0.0.1:5000
IP=419492045574.dkr.ecr.eu-central-1.amazonaws.com
TAG=latest

docker build -t plant2win_rabbitmq:${TAG} .
docker tag plant2win_rabbitmq:${TAG} ${IP}/plant2win_rabbitmq:${TAG}
docker push ${IP}/plant2win_rabbitmq:${TAG}