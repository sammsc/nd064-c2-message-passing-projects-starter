from concurrent import futures
import logging
import grpc
import location_pb2
import location_pb2_grpc
from kafka import KafkaProducer, KafkaConsumer
# from kafka import KafkaAdminClient
from kafka.admin import KafkaAdminClient, NewTopic
import pickle

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def __init__(self):
        kafka_server = 'localhost:9092'
        self.kafka_topic = 'locations'
        self.producer = KafkaProducer(bootstrap_servers=kafka_server)
        kafka_client = KafkaConsumer(bootstrap_servers=kafka_server)
        if self.kafka_topic not in kafka_client.topics():
            kafka_admin = KafkaAdminClient(bootstrap_servers=kafka_server)
            kafka_admin.create_topics([NewTopic(name=self.kafka_topic, num_partitions=1, replication_factor=1)])
            kafka_admin.close()
        kafka_client.close()

    def Create(self, request, context):
        print("Received a message!")

        request_value = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time
        }
        print(request_value)

        self.producer.send(self.kafka_topic, value=pickle.dumps(request))
        self.producer.flush()

        return location_pb2.Empty()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    location_pb2_grpc.add_LocationServiceServicer_to_server(
        LocationServicer(), server)
    server.add_insecure_port('[::]:5005')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()