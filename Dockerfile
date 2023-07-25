FROM python:alpine3.17

RUN adduser -D appuser

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

USER appuser

EXPOSE 5000

CMD gunicorn --workers 1 --bind 0.0.0.0:5000 wsgi:app







