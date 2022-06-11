FROM python:3.7

WORKDIR /backend

ENV DOCKERIZE_VERSION v0.4.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt
COPY . ./

RUN sed -i 's/self.http_client_cls(headers=self.headers)/self.http_client_cls(headers=self.headers, timeout=None)/' /usr/local/lib/python3.7/site-packages/universal_analytics/requests.py

RUN cat /usr/local/lib/python3.7/site-packages/universal_analytics/requests.py

#RUN cat app.py
ENV TZ=Europe/Bucharest
EXPOSE 8000

# RUN python3 /backend/app.py