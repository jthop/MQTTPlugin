import logging
import json
import paho.mqtt.client as mqtt

from nx584 import model

PART_TOPIC = "alarm/part"
ZONE_TOPIC = "alarm/zone"
SYSTEM_TOPIC = "alarm/system"
LOG_TOPIC = "alarm/log"
TRIGGER_TOPIC = "alarm/trigger"
QOS = 1

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
    
  def system_status(self, system):
    sys_dict = {
      "panel": system.panel_id,
      "flags": system.status_flags
    }
    js = json.dumps(sys_dict)
    self.mqtt.publish(SYSTEM_TOPIC, payload=js, qos=QOS)
    self.logger.info(f"{js}")
      
  def log_event(self, event):
    event_dict = {
      "str": event.event_string,
      "number": event.number,
      "log_size": event.log_size,
      "event_type": event.event_type,
      "reportable": event.reportable,
      "zone_user_device": event.zone_user_device,
      "partition_number": event.partition_number
    }
    js = json.dumps(event_dict)
    self.mqtt.publish(LOG_TOPIC, payload=js, qos=QOS)
    self.logger.info(f"{js}")
    
  def zone_status(self, zone):
    zone_dict = {
      "number": zone.number,
      "name": zone.name,
      "state": zone.state,
      "condition_flags": zone.condition_flags,
      "type_flags": zone.type_flags,
      "bypassed": zone.bypassed
    }
    js = json.dumps(zone_dict)
    self.mqtt.publish(ZONE_TOPIC, payload=js, qos=QOS)
    self.logger.info(f"{js}")

  def partition_status(self, part):
    if "Siren on" in part.condition_flags:
      self.triggered = True
      self.logger.warning("ALARM TRIGGERED!")
      js = json.dumps({"triggered": True})
      self.mqtt.publish(TRIGGER_TOPIC, payload=js, qos=QOS)
    elif self.triggered == True:
      self.triggered = False
      self.logger.warning("ALARM NO LONGER TRIGGERED")
      js = json.dumps({"triggered": False})
      self.mqtt.publish(TRIGGER_TOPIC, payload=js, qos=QOS)
    
    part_dict = {
      "number": part.number,
      "condition_flags": part.condition_flags,
      "armed": part.armed
    }
    js = json.dumps(part_dict)
    self.mqtt.publish(PART_TOPIC, payload=js, qos=QOS)
    self.logger.info(f"{js}")
 
