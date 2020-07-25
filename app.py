import json
import paho.mqtt.client as mqtt
import requests
import logging
import sys

global cfg

if len(sys.argv) != 1:
  loglevel = sys.argv[1]
  numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
  logging.basicConfig(level=numeric_level)

with open("config.json") as cfg_file:
  cfg_content = cfg_file.read()
  cfg = json.loads(cfg_content)

def on_connect(client, userdata, flags, rc):
  logging.info("Connected with result code "+str(rc))
  client.subscribe(cfg['mqtt_topic'])

def on_message(client, userdata, msg):
  logging.debug("Received: {}".format(msg.payload.decode()))
  r = requests.post(cfg['http_endpoint'], data = msg.payload.decode())
  logging.debug("Response from endpoint: {}".format(r.text))
    
client = mqtt.Client()
client.connect(cfg['mqtt_server'],1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
