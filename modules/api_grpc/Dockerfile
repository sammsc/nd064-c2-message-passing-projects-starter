FROM python:3.10-slim-bullseye

RUN mkdir /app
COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt
# RUN python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ location.proto
EXPOSE 5005

CMD ["python", "location_server.py"]