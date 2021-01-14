FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV APP_PATH /usr/src/app

WORKDIR ${APP_PATH}

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD . /code/

COPY . .