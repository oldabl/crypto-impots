FROM python:3.9-alpine3.19

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY main-code.py ./
COPY statements .

CMD [ "python", "./main-code.py" ]
