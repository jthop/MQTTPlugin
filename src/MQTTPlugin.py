import logging
from nx584 import model

LOG = logging.getLogger('pynx584')


class MQTTBridge(model.NX584Extension):
  def __init__(self, config=None):
    self.logger = LOG
    self.logger.info("MQTTBridge loaded")

  def zone_status(self, zone):
    self.logger.info('Zone status change for {0}'.format(zone.number))

  def partition_status(self, part):
    self.logger.info('Partition status change for {0}'.format(part.number))
