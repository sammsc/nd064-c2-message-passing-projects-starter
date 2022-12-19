from kafka import KafkaConsumer
import pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Point
from models import Location
import logging
import location_pb2
import os


def connect_db():
    DB_USERNAME = os.environ["DB_USERNAME"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_NAME = os.environ["DB_NAME"]

    engine = create_engine(f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    cur = Session(engine)

    return cur


def create(cur, request, logger):
        new_location = Location()
        new_location.person_id = request.person_id
        new_location.creation_time = request.creation_time
        new_location.coordinate = ST_Point(request.latitude, request.longitude)

        try:
            cur.add(new_location)
            cur.commit()
        except:
            logger.warning(f"Error insert into location table: {new_location}")


def main():
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger("location-api")

    cur = connect_db()

    kafka_topic = 'locations'
    kafka_server = 'kafka-service:9092'
    # kafka_server = 'localhost:9092'

    consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_server)
    for msg in consumer:
        # print("Received a message!")
        request = pickle.loads(msg.value)

        # request_value = {
        #         "person_id": request.person_id,
        #         "longitude": request.longitude,
        #         "latitude": request.latitude,
        #         "creation_time": request.creation_time
        #     }
        # print(request_value)
     
        create(cur, request, logger)


if __name__ == "__main__":
    main()