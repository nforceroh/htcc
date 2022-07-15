import os
import time
import logging
import sys
import random
import json
from pyhtcc import PyHTCC
import paho.mqtt.client as mqtt

HTCC_USER = os.getenv("HTCC_USER", "")
HTCC_PASS = os.getenv("HTCC_PASS", "")
HTCC_SNOOZE = os.getenv("HTCC_SNOOZE", "300")
MQTT_PUB_ROOT = os.getenv("MQTT_PUB_ROOT", "HTCC")
MQTT_CLIENTID = os.getenv("MQTT_CLIENTID", f'metar-{random.randint(0, 1000)}')
MQTT_HOST = os.getenv("MQTT_HOST", "")
MQTT_PORT = os.getenv("MQTT_PORT", "1883")
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASS = os.getenv("MQTT_PASS", "")
MQTT_KEEPALIVE = os.getenv("MQTT_KEEPALIVE", "60")

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(
    stream=sys.stdout, filemode="w", format=Log_Format, level=logging.ERROR
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def mqtt_publish(data):

    logger.debug("Write points: {0}".format(data))

    client = mqtt.Client(client_id="metar", clean_session=None, userdata=None,
                         transport="tcp", reconnect_on_failure=True)  # create new instance
    client.connect(host=MQTT_HOST, port=int(MQTT_PORT))  # connect to broker
    client.publish(MQTT_PUB_ROOT, payload=json.dumps(data))  # publish


def query_htcc():
    logger.debug("Connecting to HTCC")
    p = PyHTCC(HTCC_USER, HTCC_PASS)
    zone = p.get_zone_by_name("HOME")

    data = {
        "tags": {"DeviceID": zone.zone_info["DeviceID"]},
        "fields": {
            "IsFanRunning":  zone.zone_info['IsFanRunning'],
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

    mqtt_publish(data)


if __name__ == "__main__":
    while True:
        query_htcc()
        logger.debug("Sleeping till next go around")
        time.sleep(int(HTCC_SNOOZE))
