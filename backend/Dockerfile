FROM python:3.8.3

RUN mkdir /app
COPY ./src/requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

WORKDIR /app
CMD /app/run.sh
