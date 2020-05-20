FROM python:latest

ADD servidor.py /server/
ADD helloworld_pb2.py /server/
ADD helloworld_pb2_grpc.py /server/

RUN pip install grpcio
RUN pip install grpcio-tools

WORKDIR /server/