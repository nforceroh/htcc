import os
import time
import logging
import sys
from pyhtcc import PyHTCC
from influxdb import InfluxDBClient

HTCC_USER = os.getenv("HTCC_USER")
HTCC_PASS = os.getenv("HTCC_PASS")
INFLUX_HOST = os.getenv("INFLUX_HOST", "influxdb-svc.databases.svc.cluster.local")
INFLUX_DB = os.getenv("INFLUX_DB", "htcc")
INFLUX_PORT = os.getenv("INFLUX_PORT", "8086")
QUERYTIME = os.getenv("QUERYTIME", "300")

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(
    stream=sys.stdout, filemode="w", format=Log_Format, level=logging.ERROR
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def write_to_db(data):
    dbClient = InfluxDBClient(
        INFLUX_HOST, int(INFLUX_PORT), "datainsert", "adddata", INFLUX_DB
    )
    logger.info("Write points: {0}".format(data))
    dbClient.write_points(data)


def query_htcc():
    logger.info("Connecting to HTCC")
    p = PyHTCC(HTCC_USER, HTCC_PASS)
    zone = p.get_zone_by_name("HOME")

    data = [
        {
            "measurement": "measurement",
            "tags": {"DeviceID": zone.zone_info["DeviceID"]},
            "fields": {
                "IsFanRunning": zone.zone_info["IsFanRunning"],
                "DispTemp": zone.zone_info["DispTemp"],
                "HeatSetpoint": zone.zone_info["latestData"]["uiData"]["HeatSetpoint"],
                "CoolSetpoint": zone.zone_info["latestData"]["uiData"]["CoolSetpoint"],
                "IndoorHumi": zone.zone_info["IndoorHumi"],
                "StatusCool": zone.zone_info["latestData"]["uiData"]["StatusCool"],
                "StatusHeat": zone.zone_info["latestData"]["uiData"]["StatusHeat"],
                "OutdoorTemperature": zone.zone_info["OutdoorTemperature"],
                "OutdoorHumidity": zone.zone_info["OutdoorHumidity"],
                "SystemSwitchPosition": zone.zone_info["latestData"]["uiData"][
                    "SystemSwitchPosition"
                ],
                "OutdoorTemperature": zone.zone_info["OutdoorTemperature"],
                "EquipmentOutputStatus": zone.zone_info["latestData"]["uiData"][
                    "EquipmentOutputStatus"
                ],
                "SystemSwitchPosition": zone.zone_info["latestData"]["uiData"][
                    "SystemSwitchPosition"
                ],
            },
        }
    ]
    # pprint(data)
    write_to_db(data)


if __name__ == "__main__":
    while True:
        query_htcc
        logger.info("Sleeping till next go around")
        time.sleep(int(QUERYTIME))
