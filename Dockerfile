FROM python:3.9
WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#COPY ./compose/local/celery/worker/start /start-celeryworker
#RUN sed -i 's/\r//' /start-celeryworker
#RUN chmod +x /start-celeryworker
#
#COPY ./compose/local/start /start-app
#RUN sed -i 's/\r//' /start-app
#RUN chmod +x /start-app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . .
