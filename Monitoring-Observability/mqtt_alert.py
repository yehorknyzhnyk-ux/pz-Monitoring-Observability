#!/usr/bin/env python3
"""
Zabbix Media Type Script — публікує alert у MQTT topic alerts/service-status
Розмістити в: /usr/lib/zabbix/alertscripts/mqtt_alert.py
"""

import sys
import paho.mqtt.client as mqtt
import json
from datetime import datetime

MQTT_BROKER = "web3"
MQTT_PORT   = 1883
MQTT_TOPIC  = "alerts/service-status"

def send_alert(to, subject, message):
    payload = json.dumps({
        "to":        to,
        "subject":   subject,
        "message":   message,
        "timestamp": datetime.utcnow().isoformat()
    })

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "zabbix_alert")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 10)
        result = client.publish(MQTT_TOPIC, payload, qos=1, retain=False)
        result.wait_for_publish()
        print(f"[OK] Alert published to {MQTT_TOPIC}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        client.disconnect()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: mqtt_alert.py <to> <subject> <message>", file=sys.stderr)
        sys.exit(1)
    send_alert(sys.argv[1], sys.argv[2], sys.argv[3])
