FROM python:rc-alpine3.11
RUN apk add -U postgresql-dev musl-dev gcc
ADD api /app/api
ADD requirements.txt /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "api/api.py" ]
