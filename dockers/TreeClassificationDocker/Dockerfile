FROM python:3.6

ENV TZ=Europe/Bucharest
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./TreeClassificationDocker/tree_classification_requirements.txt .

RUN pip3 install -r tree_classification_requirements.txt

ENV DOCKERIZE_VERSION v0.4.0

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN apt-get update && apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6' -y

WORKDIR /TreeClassification

COPY ./TreeClassificationDocker/* /TreeClassification/
COPY ./common/ /TreeClassification
COPY ./xfastai/ /TreeClassification/xfastai/
COPY ./ai_models/TreeClassificationDocker/ /TreeClassification/models/

CMD python3 ./Classification.py
