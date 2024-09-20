FROM python:3.11-slim

WORKDIR /app

COPY app.py requirements.txt extensions.py /app/
COPY models /app/models
COPY routes /app/routes
COPY static /app/static
COPY templates /app/templates

RUN apt-get update && apt-get install -y python3-pip

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Izpostavi vrata
EXPOSE 5000

# Poženi aplikacijo
CMD ["flask", "run"]
