IP=419492045574.dkr.ecr.eu-central-1.amazonaws.com
TAG=test

set -x

docker build -f TreeDetectionDocker/Dockerfile -t tree_detection:${TAG} .

docker run -e ENV=dev -e INPUT_DIR=/input -e OUTPUT_DIR=/output -v /home/tzeny/Downloads/test_output:/output -v /home/tzeny/Downloads/test_input:/input  tree_detection:${TAG}
docker tag tree_detection:${TAG} ${IP}/tree_detection:${TAG}

# docker push ${IP}/tree_detection:${TAG}
