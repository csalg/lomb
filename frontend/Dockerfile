FROM node:14

RUN apt install make -y
RUN mkdir /app
COPY ./package.json ./package.lock* /app
WORKDIR /app
RUN npm install
#CMD /bin/bash
CMD make run
