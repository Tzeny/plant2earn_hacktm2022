IP=419492045574.dkr.ecr.eu-central-1.amazonaws.com
TAG=test

set -x

docker build -f SegmentationDocker/Dockerfile -t leaf_segmentation:${TAG} .

docker run -e ENV=dev -e INPUT_DIR=/input -e OUTPUT_DIR=/output -v /home/tzeny/Downloads/test_output:/output -v /home/tzeny/Downloads/test_input:/input  leaf_segmentation:${TAG}
docker tag leaf_segmentation:${TAG} ${IP}/leaf_segmentation:${TAG}

# docker push ${IP}/leaf_segmentation:${TAG}
