import pyembedded
from pyembedded.raspberry_pi_tools.raspberrypi import PI
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt # mosquitto.py is deprecated
import time
import json
import os
hostname = os.environ["NODE_NAME"]


#hostname=socket.gethostname()


pi = PI()


def get_data():
    # get parameters via piembedded
    ram_raw = pi.get_ram_info()
    disk_raw = pi.get_disk_space()
    cpu_raw = pi.get_cpu_usage()

    temperatur_raw=pi.get_cpu_temp()

    # pi.get_connected_ip_addr(network='wlan0')
    # pi.get_wifi_status()

    # create dicts/json objects
    temperature = {
        "name": "temperature",
        "value": temperatur_raw,
        "unit": "°C",
        "node": hostname
    }
    ram = {
        "name": "ram",
        "value": {
            "total": round(int(ram_raw[0])/1000000,1),
            "used": round(int(ram_raw[1])/1000000,1),
            "free": round(int(ram_raw[2])/1000000,1),
            },
        "unit": "GB",
        "node": hostname
        }


    disk = {
        "name": "disk",
        "value": {
            "total": disk_raw[0],
            "used": disk_raw[1],
            "free": disk_raw[2],
            },
        "unit": "GB",
        "node": hostname
        }


    cpu = {
        "name": "cpu",
        "value": cpu_raw,
        "unit": "Percent",
        "node": hostname
        }

    print("#############################################################")
    print("#############################################################")
    print("Node: ", hostname)
    print("#############################################################")
    print("temperature: ",temperature)
    print("#############################################################")
    print("ram: ",ram)
    print("#############################################################")
    print("disk: ",disk)
    print("#############################################################")
    print("cpu: ",cpu)

    return temperature, ram, disk, cpu


mqttc = mqtt.Client("k3s")
# mqttc.connect("kmaster.local", 31349, 60)
mqttc.connect("mosquitto.default.svc.cluster.local", 1883, 60)
mqttc.loop_start()
while True:
    mqttc.publish("test","Hello")

    temperature, ram, disk, cpu = get_data()
    mqttc.publish("temperature",str(temperature))
    mqttc.publish("ram",json.dumps(ram))
    mqttc.publish("disk",json.dumps(disk))
    mqttc.publish("cpu",json.dumps(cpu))

    time.sleep(2)# sleep for 10 seconds before next call