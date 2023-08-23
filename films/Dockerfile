FROM python:3.10.6-alpine

WORKDIR /films

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

COPY . .

CMD python manage.py runserver 0.0.0.0:8000

ENTRYPOINT ["/films/entrypoint.sh"]