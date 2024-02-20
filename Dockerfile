FROM python:3.13-rc-slim

WORKDIR /app

RUN mkdir /app/data

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]