FROM python:3.9.6
RUN pip install influxdb-client requests
WORKDIR /app
COPY . .
CMD ["python", "src/foremangraf.py"]