FROM python:3.8

RUN mkdir app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scraper.py .
COPY /phone_extractor ./phone_extractor

WORKDIR /app

RUN ls -la

# command to run on container start
CMD  python -m scraper