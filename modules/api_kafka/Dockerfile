FROM python:3.10-slim-bullseye

RUN mkdir /app
COPY . /app/
WORKDIR /app
RUN apt update && apt install -y libgeos-dev libpq-dev python3-dev build-essential
RUN pip install -r requirements.txt

CMD ["python", "-u", "kafka_to_db.py"]