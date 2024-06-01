FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .


EXPOSE 5000


CMD ["gunicorn","--timeout" ,"800", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
