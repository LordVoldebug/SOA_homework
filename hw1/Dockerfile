FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /serealization_bench

WORKDIR /serealization_bench

COPY . /serealization_bench/

RUN pip install --no-cache-dir avro-python3 protobuf msgpack pyyaml xmltodict dicttoxml
