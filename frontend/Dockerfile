FROM node:14

RUN apt install make
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN make build
#CMD /bin/bash
CMD make run
