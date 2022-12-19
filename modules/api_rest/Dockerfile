FROM python:3.7-alpine

RUN mkdir /app
COPY . /app/
WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]