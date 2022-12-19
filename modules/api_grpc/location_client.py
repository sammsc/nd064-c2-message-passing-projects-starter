import grpc
import location_pb2
import location_pb2_grpc
from datetime import datetime, timezone

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

# channel = grpc.insecure_channel("localhost:5005")
channel = grpc.insecure_channel("localhost:30005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
for i in range(2):
    cur_position = location_pb2.LocationMessage(
        person_id = 2 + i,
        longitude = 2.4 + i,
        latitude = 3.6 + i,
        creation_time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.000000")
    )

    response = stub.Create(cur_position)