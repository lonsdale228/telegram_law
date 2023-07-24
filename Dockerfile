FROM ubuntu:latest

FROM python:3.10.12-slim

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .


CMD ["python3", "main.py"]