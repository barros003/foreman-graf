from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "_v-lv3tBs3LEoxNlD8p1pYYhEfx8IVJqO4-s_R3Ti7-1j9FFFW2NN6owDH4hb6_BytJ0huQY2SQ6b4TTOqzxgA=="
org = "myown"
bucket = "satellite"

client = InfluxDBClient(url="http://192.168.213.48:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

data = "patchs,type=security totalmachines=100"
write_api.write(bucket, org, data)

data = "patchs,type=bugfix totalmachines=150"
write_api.write(bucket, org, data)

data = "patchs,type=enhancement totalmachines=30"
write_api.write(bucket, org, data)