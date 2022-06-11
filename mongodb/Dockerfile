FROM registry.hub.docker.com/library/mongo:3.4

MAINTAINER <Cristian Avramescu> cristian.avramescu@mindfullytech.com

# Auth Configuration. Modify as needed.
# These environment variables can also be specified through command line or docker-compose configuration
ENV AUTH yes

ENV MONGODB_ADMIN_USER root
ENV MONGODB_ADMIN_PASS YrwfHnyvQTP3uwXT6Zqq

# ENV MONGODB_APPLICATION_DATABASE your_db
# ENV MONGODB_APPLICATION_USER user
# ENV MONGODB_APPLICATION_PASS password

EXPOSE 27017 27017

ADD run.sh /run.sh
ADD set_mongodb_password.sh /set_mongodb_password.sh

RUN chmod +x /run.sh
RUN chmod +x /set_mongodb_password.sh

CMD ["/run.sh"]