IP=419492045574.dkr.ecr.eu-central-1.amazonaws.com
TAG=test

set -x

docker build -f SegmentationDocker/Dockerfile -t leaf_segmentation:${TAG} .

# docker run -e XVISION_ENV=dev -e RUN_TYPE=0 -v /home/tzeny/Downloads/test_output:/test_output xvision_chexnetboundingbox_algorithm:${TAG}
docker tag leaf_segmentation:${TAG} ${IP}/leaf_segmentation:${TAG}

docker push ${IP}/leaf_segmentation:${TAG}
