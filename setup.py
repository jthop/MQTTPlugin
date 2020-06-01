from setuptools import setup

setup(name='MQTTPlugin',
  version='0.1',
  py_modules=['MQTTPlugin'],
  install_requires=['setuptools', 'paho-mqtt'],
  entry_points={'pynx584': ['mqtt_plugin=src.MQTTPlugin:MQTTBridge']},
)
