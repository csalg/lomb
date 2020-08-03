FROM node:14

RUN apt install make -y
RUN mkdir /app
COPY ./package.json ./package.lock* /app
WORKDIR /app
RUN npm install
RUN npm install -g serve
RUN npm run build
#CMD /bin/bash
CMD make run

