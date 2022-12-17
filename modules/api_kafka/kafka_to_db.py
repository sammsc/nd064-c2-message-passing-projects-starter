from kafka import KafkaConsumer
# import grpc
# import location_pb2
# import location_pb2_grpc
import pickle
# import time
import psycopg2
# import sqlalchemy
from geoalchemy2.functions import ST_Point
# from models import Location
# from typing import Dict
import logging

def connect_db():
    # DB_USERNAME = os.environ["DB_USERNAME"]
    # DB_PASSWORD = os.environ["DB_PASSWORD"]
    # DB_HOST = os.environ["DB_HOST"]
    # DB_PORT = os.environ["DB_PORT"]
    # DB_NAME = os.environ["DB_NAME"]
    DB_USERNAME = 'ct_admin'
    DB_PASSWORD = 'd293aW1zb3NlY3VyZQ=='
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'geoconnections'

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD)    
    cur = conn.cursor()

    return cur

def create(cur, location_table_insert, request, logger):
        coordinate = ST_Point(request.longitude, request.latitude)
        val = (request.person_id, coordinate, request.creation_time)

        try:
            cur.execute(location_table_insert, val)
        except:
            logger.warning(f"Error insert into location table: {val}")


def main():
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger("location-api")

    cur = connect_db()

    location_table_insert = ("""INSERT INTO location (person_id, coordinate, creation_time) 
                                VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
                            """)
    kafka_topic = 'locations'

    consumer = KafkaConsumer(kafka_topic, bootstrap_servers='localhost:9092')
    for msg in consumer:
        print("Received a message!")
        request = pickle.loads(msg.value)

        request_value = {
                "person_id": request.person_id,
                "longitude": request.longitude,
                "latitude": request.latitude,
                "creation_time": request.creation_time
            }
        print(request_value)
     
        create(cur, location_table_insert, request, logger)



if __name__ == "__main__":
    main()