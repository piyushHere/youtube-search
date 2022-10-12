# syntax=docker/dockerfile:1

FROM python:3.10.2

WORKDIR /youtube-fetch

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "app", "run", "--host=0.0.0.0"]