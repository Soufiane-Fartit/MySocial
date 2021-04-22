# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install ufw nginx python3-dev default-libmysqlclient-dev build-essential -y

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./nginx.conf /etc/nginx/nginx.conf
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled
# RUN ufw delete allow 5000
# RUN ufw allow 'Nginx Full'

RUN mkdir /etc/ssl/private
RUN chmod 700 /etc/ssl/private
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj "/emailAddress=soufiane.fartit@gmail.com/C=FR/ST=GrandEst/L=Strasbourg/O=mySocial Inc/OU=DSI" -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

# copy project
COPY . /usr/src/app/