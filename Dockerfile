from python:3.10.6-slim-bullseye

env PIP_DISABLE_PIP_VERSION_CHECK 1
env PYTHONDONTWRITEBYTECODE 1
env PYTHONUNBUFFERED 1

workdir /app

copy ./requirements.txt .
run pip install -r requirements.txt

copy . .
