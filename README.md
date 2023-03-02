## These scripts get info from foreman/satellite and populate the influxdb, that is used as datasource to grafana where you can build the painels.
## It gets the following info from foreman/satellite to influxdb.
- number of registered servers on foreman/satellite
- number of servers with security,bugfix and enhancement with pending updates
- number of pending update per server according with the type security,bugfix and enhancement

## Requirements
- influxdb2
- grafana v9+

## 1. Start influxdb 2.0 container, see https://hub.docker.com/_/influxdb

## 2. start the container that contains this scripts, it will get info from foreman/satellite and populate the influxdb, you need to run  the docker command with the following variables:

- INFLUX_TOKEN=influxdb user token  
- INFLUX_ORG=org name
- INFLUX_BUCKET=bucket name
- SYNC_TIME=30 time in minutes between the script executions (get info from foreman/satellite every 30 minutes)
- INFLUX_URL=http://192.168.1.1:8086
- FOREMAN_HOST=foreman.example.com
- FOREMAN_USER= foreman user
- FOREMAN_TOKEN=user token
- FOREMAN_ORGID=1 (you can get it by running the command: hammer organization list)

you can create a file with these variables and run the following docker command:

- docker run  -d  --env-file ./env.list --restart=always --name foreman_influx barros003/foreman_to_influx:latest

## 3 . import the dashboard to grafana and configure the datasource pointing to influxdb2 (choose flux in query language option), also you will need to adjust the bucket name on the panels.

<a href="https://ibb.co/Wcfjf3V"><img src="https://i.ibb.co/JzHgHd3/grafana-painel.jpg" alt="grafana-painel" border="0" /></a>
