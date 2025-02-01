FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN chmod +x docker-entrypoint.sh

RUN apt-get update && apt-get install -y postgresql-client

ENTRYPOINT ["./docker-entrypoint.sh"]
