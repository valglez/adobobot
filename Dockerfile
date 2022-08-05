FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install python-telegram-bot mysql-connector-python

COPY adobobot.py .

CMD [ "python3", "adobobot.py"]