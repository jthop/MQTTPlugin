import logging
from nx584 import model

LOG = logging.getLogger('pynx584')


class MQTTBridge(model.NX584Extension):
  def __init__(self, config=None):
    self.logger = LOG
    self.logger.info("MQTTBridge loaded")

  def zone_status(self, zone):
    self.logger.info(f"Zone status change for {zone.number}")
    self.logger.info(f"{zone}")

  def partition_status(self, part):
    self.logger.info(f"Partition status change for {part.number}")
    self.logger.info(f"{part}")
