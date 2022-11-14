from datetime import datetime
from foreman_data import *
import time
import logging
import os

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


token = os.environ.get('INFLUX_TOKEN')
org = os.environ.get('INFLUX_ORG')
bucket = os.environ.get('INFLUX_BUCKET')
sync_time = os.environ.get('SYNC_TIME')
influx_url = os.environ.get('INFLUX_URL')
client = InfluxDBClient(url=f"{influx_url}", token=token)

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
        lifecycle    = res[1][key]["lifecycle"]       
        osname       = str(res[1][key]["osname"])
        osname       = osname.replace(' ', '\ ')
        
        data = f"patchs,host={hostname},lifecycle={lifecycle},osname={osname} {errata_type}={errata_count}"
        write_api.write(bucket, org, data)
    
        data = f"patchs,host={hostname},lifecycle={lifecycle},osname={osname} {errata_type}={errata_count}"
        write_api.write(bucket, org, data)
        
        data = f"patchs,host={hostname},lifecycle={lifecycle},osname={osname} {errata_type}={errata_count}"
        write_api.write(bucket, org, data)
       
    logging.info(f"Next sync in: {sync_time} minutes")
    time.sleep(int(sync_time) * 60)
        
write_to_influxdb()