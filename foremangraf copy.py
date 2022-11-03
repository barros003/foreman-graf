from datetime import datetime
from foreman_data import *
import random

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "_v-lv3tBs3LEoxNlD8p1pYYhEfx8IVJqO4-s_R3Ti7-1j9FFFW2NN6owDH4hb6_BytJ0huQY2SQ6b4TTOqzxgA=="
org = "myown"
bucket = "satellite"

client = InfluxDBClient(url="http://192.168.213.48:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

for i in range(4, 427):
    num1 = random.randint(10, 150)
    num2 = random.randint(10, 150)
    num3 = random.randint(10, 150)
    data = f"patch,host=oracle7-{i} security={num1}"
    write_api.write(bucket, org, data)
    data = f"patch,host=oracle7-{i} bugfix={num2}"
    write_api.write(bucket, org, data)
    data = f"patch,host=oracle7-{i} enhancement={num3}"
    write_api.write(bucket, org, data)


    

#data = f"patch,host=oracle7 security=0"
#write_api.write(bucket, org, data)

#data = f"patch,host=oracle7 bugfix=0"
#write_api.write(bucket, org, data)

#data = f"patch,host=oracle7 enhancement=0"
#write_api.write(bucket, org, data)