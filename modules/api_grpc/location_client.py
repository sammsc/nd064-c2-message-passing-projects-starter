import grpc
import location_pb2
import location_pb2_grpc
import time

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
for i in range(2):
    order = location_pb2.LocationMessage(
        person_id = 2 + i,
        longitude = 2.4 + i,
        latitude = 3.6 + i,
        creation_time='2021-06-07 10:37:06.000000'
    )


    response = stub.Create(order)