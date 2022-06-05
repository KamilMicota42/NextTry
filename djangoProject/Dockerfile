# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install Pillow
<<<<<<< HEAD
COPY . /code/
=======
COPY . /code/
>>>>>>> 9c8328b1e52c206ac46a43aebfc89c9062745086
