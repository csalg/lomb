FROM python:3.8.3

RUN mkdir /app
COPY requirements.txt /tmp
COPY ./install.sh /tmp

WORKDIR /app

RUN cd /tmp; sh install.sh

CMD /app/run.sh