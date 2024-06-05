FROM python:3.11

ENV DJANGO_SETTINGS_MODULE=slack-ai.settings
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get upgrade -y

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]