from setuptools import setup

setup(name='MQTTPlugin',
  version='0.1',
  py_modules=['MQTTPlugin'],
  install_requires=[
    'setuptools>=40.5.0',
    'paho-mqtt>=1.5.0'
    ],
  entry_points={'pynx584': ['test=src.MQTTPlugin:MQTTBridge']},
)
