FROM python:3.9-alpine

ENV LIBRARY_PATH=/lib:/usr/lib
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk add pkgconfig gcc libc-dev postgresql-dev libpq-dev

COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN python3.9 -m pip install pip --upgrade \
    && python3.9 -m pip install pipenv \
    && pipenv install

COPY . .

EXPOSE 8000

CMD ["pipenv", "run", "gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "main.wsgi:application"]