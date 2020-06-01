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
    
    self.zone = None
    self.part = None
    
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
    self.zone = zone_dict
    self._publish()

  def partition_status(self, part):
    self.logger.info(f"Partition status change for {part.number}")

    if "Siren on" in part.condition_flags:
      self.triggered = True
      self.logger.warning("ALARM TRIGGERED!")
      js = json.dumps({"triggered": True})
      self.mqtt.publish('alarm/trigger', payload=js, qos=1)
    elif self.triggered == True:
      self.triggered = False
      self.logger.warning("ALARM NO LONGER TRIGGERED")
      js = json.dumps({"triggered": False})
      self.mqtt.publish('alarm/trigger', payload=js, qos=0)
    
    part_dict = {
      "number": part.number,
      "condition_flags": part.condition_flags,
      "armed": part.armed
    }
    self.part = part_dict
    self._publish()

  def _publish(self):
    system = {}
    if self.zone is not None:
      system["zone"] = self.zone
    if self.part is not None:
      system["part"] = self.part
    js = json.dumps(system)
    self.mqtt.publish('alarm/update', payload=js, qos=0)
      
