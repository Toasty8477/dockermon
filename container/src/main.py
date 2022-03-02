import docker
from paho.mqtt import client as mqtt
import random
from time import sleep
import json

broker = '192.168.0.18'
port = 1883
topic = 'dockermon'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'mqtt'
password = 'password'
docker = docker.from_env()

def connect():
    global client
    client = mqtt.Client(client_id)
    client.on_connect = print('Connected!')
    client.connect(broker, port)
    return client

try:
    connect()
except:
    print('Something Went Wrong')
while True:
    messages = 0
    status = {}
    for container in docker.containers.list(all):
        messages = messages + 1
        status.update({container.name: container.status })
    status.update({"containers": messages})
    message = json.dumps(status)
    client.publish(topic, payload = message , qos = 0, retain = False)
    print(message)
    print("Status Sent!")
    sleep(900)