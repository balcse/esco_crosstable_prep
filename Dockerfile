FROM python:3.11

RUN apt-get update

WORKDIR /usr/src/app
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY prep_data.py .

CMD [ "python","prep_data.py" ]