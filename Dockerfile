# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY main.py data_grabber.py ./
COPY data/ ./data/

CMD [ "python3", "./main.py"]