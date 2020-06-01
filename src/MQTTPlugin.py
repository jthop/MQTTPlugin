import logging
import json
import paho.mqtt.client as mqtt

from nx584 import model

LOG = logging.getLogger('pynx584')


class MQTTBridge(model.NX584Extension):
  def __init__(self, config=None):
    self.logger = LOG
    self.logger.info("MQTTBridge loaded")
    self.triggered = False
    
    self.mqtt = mqtt.Client()
    self._start_mqtt()

  def _start_mqtt(self):
    self.mqtt.on_connect = self._on_connect
    self.mqtt.connect('192.168.29.13', 1883, 60)
    self.mqtt.loop_start()
    
  def _on_connect(self, client, userdata, flags, rc):
    self.logger.info("MQTT client connected")
    
  def zone_status(self, zone):
    self.logger.info(f"Zone status change for {zone.number}")
    zone_dict = {
      "number": zone.number,
      "name": zone.name,
      "state": zone.state,
      "condition_flags": zone.condition_flags,
      "type_flags": zone.type_flags,
      "bypassed": zone.bypassed
    }
    js = json.dumps(zone_dict)
    self.mqtt.publish('alarm/zone', payload=js, qos=0)    

  def partition_status(self, part):
    self.logger.info(f"Partition status change for {part.number}")
    if "Siren on" in part.condition_flags:
      self.triggered = True
      self.logger.warning("ALARM TRIGGERED!")
    elif self.triggered == True:
      self.triggered = False
      self.logger.warning("ALARM NO LONGER TRIGGERED")
      
    part_dict = {
      "number": part.number,
      "condition_flags": part.condition_flags,
      "armed": part.armed
    }
    js = json.dumps(part_dict)
    self.mqtt.publish('alarm/part', payload=js, qos=0)    

