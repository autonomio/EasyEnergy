

# syntax=docker/dockerfile:1


FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3.9 -m pip install --upgrade pip

RUN  python3.9 -m pip install tensorflow

RUN python3.9 -m pip install -r requirements.txt

COPY . .

RUN python3.9 setup.py install
