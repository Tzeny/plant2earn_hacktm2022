IP=419492045574.dkr.ecr.eu-central-1.amazonaws.com
TAG=test

set -x

docker build -f TreeClassificationDocker/Dockerfile -t tree_classification:${TAG} .

# docker run -e ENV=dev -e INPUT_DIR=/input -e OUTPUT_DIR=/output -v /home/tzeny/Downloads/test_output:/output -v /home/tzeny/Downloads/test_input:/input  tree_classification:${TAG}
# docker run -v /dataimages:/dataimages tree_classification:${TAG}
docker tag tree_classification:${TAG} ${IP}/tree_classification:${TAG}

docker push ${IP}/tree_classification:${TAG}
