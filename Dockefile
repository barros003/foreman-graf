FROM python:3.9.15-alpine
RUN pip install influxdb-client requests
WORKDIR /app
COPY . .
CMD ["python", "src/foremangraf.py"]