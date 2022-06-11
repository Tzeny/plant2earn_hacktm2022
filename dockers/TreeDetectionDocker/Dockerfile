FROM python:3.7

ENV TZ=Europe/Bucharest
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./TreeDetectionDocker/tree_detection_requirements.txt .

RUN pip3 install -r tree_detection_requirements.txt

RUN python3 -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
# RUN python3 -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/index.html

ENV DOCKERIZE_VERSION v0.4.0

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN apt-get update && apt-get install 'ffmpeg' \
    'libsm6' \ 
    'libxext6' 'libopencv-dev' 'python3-opencv' -y

WORKDIR /TreeDetection

RUN mkdir -p /TreeDetection/Local/Models

COPY ./TreeDetectionDocker/* /TreeDetection/
COPY ./common/ /TreeDetection
COPY ./ai_models/TreeDetectionDocker/ /TreeDetection/models/
RUN true

CMD python3 ./TreeDetection.py
