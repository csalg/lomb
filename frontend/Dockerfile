FROM node:14
ARG API_URL
ARG HOSTNAME

RUN apt install make -y
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN make build
CMD /bin/bash
