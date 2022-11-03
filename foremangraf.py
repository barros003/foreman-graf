from datetime import datetime
from foreman_data import *

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "_v-lv3tBs3LEoxNlD8p1pYYhEfx8IVJqO4-s_R3Ti7-1j9FFFW2NN6owDH4hb6_BytJ0huQY2SQ6b4TTOqzxgA=="
org = "myown"
bucket = "satellite"

client = InfluxDBClient(url="http://192.168.213.48:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

res = get_errata_count_all()
security    = str(res[0])
bugfix      = str(res[1])
enhancement = str(res[2])
total       = str(res[3])

data = f"patchs,type=security totalmachines={security}"
write_api.write(bucket, org, data)

data = f"patchs,type=bugfix totalmachines={bugfix}"
write_api.write(bucket, org, data)

data = f"patchs,type=enhancement totalmachines={enhancement}"
write_api.write(bucket, org, data)

data = f"patchs,type=total totalmachines={total}"
write_api.write(bucket, org, data)