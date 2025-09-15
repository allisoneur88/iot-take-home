import json
import logging
import paho.mqtt.client as mqtt

class MqttHandler:
    def __init__(self, broker="localhost", port=1883):
        self.client = mqtt.Client(client_id="pyqt-app")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(broker, port, 60)

        self.received_callback = None
        self.sensor_callback = None

    def _on_connect(self, client, userdata, flags, rc):
        logging.info("Connected to MQTT broker, rc=%s", rc)
        client.subscribe("m/MES/UnitsProduced")
        client.subscribe("m/plc/sensor")

    def _on_message(self, client, userdata, msg):
        try:
            if msg.topic == "m/MES/UnitsProduced":
                if self.received_callback:
                    self.received_callback(msg.payload.decode())
            elif msg.topic == "m/plc/sensor":
                if self.sensor_callback:
                    data = json.loads(msg.payload.decode())
                    self.sensor_callback(data)
        except Exception as e:
            logging.error("Error in MQTT message: %s", e)

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()

    def publish_sensor_data(self, data_dict):
        payload = json.dumps(data_dict)
        logging.info("Publishing: %s", payload)
        self.client.publish("m/plc/sensor", payload)

