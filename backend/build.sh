IP=419492045574.dkr.ecr.eu-central-1.amazonaws.com
ENV=latest

docker build -t plant2win_backend:${ENV} .
docker tag plant2win_backend:${ENV} ${IP}/plant2win_backend:${ENV}
# docker run ${IP}/plant2win_backend:${ENV}
docker push ${IP}/plant2win_backend:${ENV}
