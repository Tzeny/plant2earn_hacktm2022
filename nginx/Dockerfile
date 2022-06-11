#GET the base default nginx image from docker hub
FROM nginx

COPY ssl_keys/domain_srv.crt /nginx/domain_srv.crt
COPY ssl_keys/domain_srv.key /nginx/domain_srv.key

#Delete the Existing default.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /nginx/
RUN ls -l /nginx/
#Copy the custom default.conf to the nginx configuration