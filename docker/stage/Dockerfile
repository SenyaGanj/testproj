FROM python:3.9-alpine

ENV LIBRARY_PATH=/lib:/usr/lib
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /opt/testproj/

RUN apk add pkgconfig gcc libc-dev postgresql-dev libpq-dev

COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN python3.9 -m pip install pip --upgrade \
    && python3.9 -m pip install pipenv \
    && pipenv install

COPY . .

RUN chmod +x ./wait-for-it.sh ./entrypoint.sh
CMD ["./migrations.sh"]
EXPOSE 8000
