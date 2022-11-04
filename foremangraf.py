from datetime import datetime
from foreman_data import *
import time
import logging

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "_v-lv3tBs3LEoxNlD8p1pYYhEfx8IVJqO4-s_R3Ti7-1j9FFFW2NN6owDH4hb6_BytJ0huQY2SQ6b4TTOqzxgA=="
org = "myown"
bucket = "satellite"
sync_time = 600

client = InfluxDBClient(url="http://192.168.213.48:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

def write_to_influxdb():
 while True:
    logging.basicConfig(level=logging.INFO, filename="main.log", format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Starting new sync sequence")
    res = main_erratum()
    security    = str(res[0][0])
    bugfix      = str(res[0][1])
    enhancement = str(res[0][2])
    total       = str(res[0][3])

    data = f"patchs,type=security totalmachines={security}"
    write_api.write(bucket, org, data) 

    data = f"patchs,type=bugfix totalmachines={bugfix}"
    write_api.write(bucket, org, data)
    
    data = f"patchs,type=enhancement totalmachines={enhancement}"
    write_api.write(bucket, org, data)
    
    data = f"patchs,type=total totalmachines={total}"
    write_api.write(bucket, org, data)
    

    for key in res[1]:
                
        hostname     = res[1][key]["host"]
        errata_type  = res[1][key]["errata_type"]
        errata_count = res[1][key]["errata_count"]              
        data = f"patchs,host={hostname} {errata_type}={errata_count}"
        write_api.write(bucket, org, data)
    timeinminute = sync_time//60    
    logging.info(f"Next sync in: {timeinminute} minutes")
    time.sleep(sync_time)
        
write_to_influxdb()
