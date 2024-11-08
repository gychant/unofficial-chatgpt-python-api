# syntax=docker/dockerfile:1

FROM python:3.11

RUN apt-get update \
    && apt-get install -y \
    poppler-utils \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080 9222

ENV CHROME_BIN=/usr/bin/google-chrome
ENV DISPLAY=:99

CMD ["bash", "-c", "uvicorn app:app --host 0.0.0.0 --port 8080"]