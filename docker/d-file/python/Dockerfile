FROM python:3.8-slim-buster
RUN apt update
RUN apt upgrade
RUN mkdir /app

COPY requirements.txt /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ../../../ .

CMD [ "python3", "manage.py" , "runserver"]
