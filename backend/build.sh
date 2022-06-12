IP=419492045574.dkr.ecr.eu-central-1.amazonaws.com
ENV=test

docker build -t plant2win_backend:${ENV} .
docker tag plant2win_backend:${ENV} ${IP}/plant2win_backend:${ENV}
# docker run -it --entrypoint python3 ${IP}/plant2win_backend:${ENV} /backend/app.py
docker push ${IP}/plant2win_backend:${ENV}
