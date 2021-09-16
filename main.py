from pyhtcc import PyHTCC
#from pprint import pprint
from influxdb import InfluxDBClient


p = PyHTCC("andisyl@martintwingles.com", "Kaykay2634")
zone = p.get_zone_by_name('HOME')

dbClient = InfluxDBClient('influxdb.ocp.nf.lab',
                          8086, 'datainsert', 'adddata', 'htcc')
data = [
    {
        "measurement": "measurement",
        "tags": {
            "DeviceID": zone.zone_info['DeviceID']
        },
        "fields": {
            "IsFanRunning": zone.zone_info['IsFanRunning'],
            "DispTemp": zone.zone_info['DispTemp'],
            "HeatSetpoint": zone.zone_info['latestData']['uiData']['HeatSetpoint'],
            "CoolSetpoint": zone.zone_info['latestData']['uiData']['CoolSetpoint'],
            "IndoorHumi": zone.zone_info['IndoorHumi'],
            "StatusCool": zone.zone_info['latestData']['uiData']['StatusCool'],
            "StatusHeat": zone.zone_info['latestData']['uiData']['StatusHeat'],
            "OutdoorTemperature": zone.zone_info['OutdoorTemperature'],
            "OutdoorHumidity": zone.zone_info['OutdoorHumidity'],
            "SystemSwitchPosition": zone.zone_info['latestData']['uiData']['SystemSwitchPosition'],
            "OutdoorTemperature": zone.zone_info['OutdoorTemperature'],
            "EquipmentOutputStatus": zone.zone_info['latestData']['uiData']['EquipmentOutputStatus'],
            "SystemSwitchPosition": zone.zone_info['latestData']['uiData']['SystemSwitchPosition'],
        }
    }
]
# pprint(data)
dbClient.write_points(data)

""" 
zone.zone_info['DeviceID'] # DeviceID
zone.zone_info['IsFanRunning'] # fan running
zone.zone_info['DispTemp'] # fan running
zone.zone_info['IndoorHumi'] # fan running
zone.zone_info['OutdoorTemperature'] # fan running
zone.zone_info['OutdoorHumidity'] # fan running
zone.zone_info['latestData']['uiData']['EquipmentOutputStatus'] # 1 running 0 off
zone.zone_info['latestData']['uiData']['SystemSwitchPosition'] # 1 heat 2 off
statusCool/statusHeat=0 when set to follow schedule
statusCool/statusHeat=1 when set on temporary hold
statusCool/statusHeat=2 when set on permanent hold
SystemSwitchPosition=1 when set to heat mode
SystemSwitchPosition=2 when set to off mode
SystemSwitchPosition=3 when set to cool mode
SystemSwitchPosition=4 when set to auto mode 
"""
