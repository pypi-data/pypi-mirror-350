import ssl
import paho.mqtt.client as mqtt
from importlib.resources import files

from os import environ as env

class MQTTClient:
  def __init__(self):  
    self.__mqtt_client = mqtt.Client()
    cert_path = files("rmind_yandex_smart_home") / "rootCA.crt"

    self.__mqtt_client.username_pw_set(username=env['MQTT_USER'], password=env['MQTT_PASS'])
    self.__mqtt_client.tls_set(str(cert_path), tls_version=ssl.PROTOCOL_TLSv1_2)
    self.__mqtt_client.tls_insecure_set(True)

  def connect(self): 
    self.__mqtt_client.connect(env.get('MQTT_URL', 'mqtt.cloud.yandex.net'), int(env.get('MQTT_PORT', '8883')), 60)

  def publish(self, topic, message):
    if message is None:
      return False

    tries = 5
    while True:
      response = self.__mqtt_client.publish(topic, message, 1)
      if response.rc == mqtt.MQTT_ERR_SUCCESS:
        break

      tries -= 1
      if tries == 0:
        return False
            
    return True