FROM python:3.9.2

ENV PYTHONUNBUFFERED 1

RUN mkdir /streetEvent
WORKDIR /streetEvent
ADD requirements.txt /streetEvent/

RUN apt update && apt install -y gdal-bin libgdal-dev python3-gdal && pip install --upgrade pip && pip install -r requirements.txt

COPY ./streetEvent streetEvent