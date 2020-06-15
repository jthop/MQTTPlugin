import logging
import json
import paho.mqtt.client as mqtt

from nx584 import model

MQTT_HOST = "192.168.29.15"
PART_TOPIC = "alarm/part"
ZONE_TOPIC = "alarm/zone"
SYSTEM_TOPIC = "alarm/system"
LOG_TOPIC = "alarm/log"
QOS = 1

LOG = logging.getLogger('pynx584')


class MQTTBridge(model.NX584Extension):
  def __init__(self, config=None):
    self.logger = LOG
    self.connected = False
    self.logger.info("MQTTBridge loaded")
    
    self.mqtt = mqtt.Client()
    self._start_mqtt()

  def _start_mqtt(self):
    try:
      self.mqtt.on_connect = self._on_connect
      self.mqtt.on_disconnect = self._on_disconnect
      self.mqtt.connect(MQTT_HOST, 1883, 60)
      self.mqtt.loop_start()
    except Exception as e:
      self.logger.info("mqtt connect failed")
      self.connected = False

  def _restart(self):
    self.mqtt.reinitialise()
    self._start_mqtt()
      
  def _on_connect(self, client, userdata, flags, rc):
    self.logger.info("MQTT client connected")
    self.connected = True
  
  def _on_disconnect(self, client, userdata, rc):
    self.connected = False
    self._restart()
    
  def log_event(self, event):
    if not self.connected:
      self._restart()
      return
    
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

  def system_status(self, system):
    if not self.connected:
      self._restart()
      return
    
    sys_dict = {
      "panel": system.panel_id,
      "flags": system.status_flags
    }
    js = json.dumps(sys_dict)
    self.mqtt.publish(SYSTEM_TOPIC, payload=js, qos=QOS)
    self.logger.info(f"{js}")
    
  def zone_status(self, zone):
    if not self.connected:
      self._restart()
      return
    
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
    if not self.connected:
      self._restart()
      return
    
    part_dict = {
      "number": part.number,
      "condition_flags": part.condition_flags,
      "armed": part.armed
    }
    js = json.dumps(part_dict)
    self.mqtt.publish(PART_TOPIC, payload=js, qos=QOS)
    self.logger.info(f"{js}")
 
