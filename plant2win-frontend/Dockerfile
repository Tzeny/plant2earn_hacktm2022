FROM node:8

RUN apt-get update && apt-get install gettext-base

COPY ./dist/ /frontend/dist/
COPY ./nginx/ /frontend/nginx/

COPY ./index.js /frontend/index.js

COPY ./package-deploy.json /frontend/package.json
WORKDIR /frontend
RUN npm install

EXPOSE 4200

ENV PORT 4200

CMD npm run start
