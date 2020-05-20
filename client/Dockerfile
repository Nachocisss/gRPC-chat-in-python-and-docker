FROM python:latest

ADD cliente.py /client/
ADD helloworld_pb2.py /client/
ADD helloworld_pb2_grpc.py /client/

RUN pip install grpcio
RUN pip install grpcio-tools

WORKDIR /client/