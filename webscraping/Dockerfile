FROM python:3.9-slim-bullseye

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    unzip \
    xvfb \
    firefox-esr \
    libx11-xcb1 \
    libdbus-glib-1-2 \
	firefox \
    && rm -rf /var/lib/apt/lists/*

ENV GECKODRIVER_VERSION=0.33.0

RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz \
    && tar -xzf geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir psycopg2-binary SQLAlchemy

ENV MOZ_HEADLESS=1
ENV PYTHONUNBUFFERED=1

COPY . .

CMD ["python", "src/main.py"]
