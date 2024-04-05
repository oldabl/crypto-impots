FROM python:3.9-alpine3.19

ENV TZ="Europe/Paris"
RUN date

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./statements ./statements

CMD [ "python", "./src/main.py" ]
