FROM python:3
ENV PYTHONUNBUFFERED 1
EXPOSE 8000/tcp
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
CMD gunicorn sptest.wsgi:application --bind 0.0.0.0:8000 --workers 3
