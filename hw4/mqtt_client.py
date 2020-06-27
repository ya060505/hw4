import paho.mqtt.client as paho

import time

import matplotlib.pyplot as plt

import numpy as np


s = -5

print("t1")
t = np.arange(0, 20, 0.5)
x = np.arange(0, 20, 0.5)
y = np.arange(0, 20, 0.5)
z = np.arange(0, 20, 0.5)
tilt = np.arange(0, 20, 0.5)
print("t2")

x[0] = 9.1
x[4] = 9911.9911

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client


# MQTT broker hosted on local machine

mqttc = paho.Client()


# Settings for connection

# TODO: revise host to your ip

host = "localhost"

topic = "Mbed"


# Callbacks

def on_connect(self, mosq, obj, rc):

      print("Connected rc: " + str(rc))


def on_message(mosq, obj, msg):
      global s, x, y, z, tilt

      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");


      if s >= 0:
            if s % 4 == 0:
                  x[int(s/4)] = float(msg.payload)
            elif s % 4 == 1:
                  y[int(s/4)] = float(msg.payload)
            elif s % 4 == 2:
                  z[int(s/4)] = float(msg.payload)
            else:
                  tilt[int(s/4)] = float(msg.payload)

      s+=1
      print("s=",s)

      if s == 160:
            fig, ax = plt.subplots(2, 1)

            ax[0].plot(t, x, color="red", linewidth=2.5, linestyle="-", label="x")

            ax[0].plot(t, y, color="blue", linewidth=2.5, linestyle="-", label="y")

            ax[0].plot(t, z, color="green", linewidth=2.5, linestyle="-", label="z")

            ax[0].legend(loc='lower left', frameon=True)

            ax[0].set_xlabel('Time')

            ax[0].set_ylabel('Acc Vector')

            ax[1].stem(t, tilt)

            ax[1].set_xlabel('Time')

            ax[1].set_ylabel('Tilt')

            plt.show()


def on_subscribe(mosq, obj, mid, granted_qos):

      print("Subscribed OK")


def on_unsubscribe(mosq, obj, mid, granted_qos):

      print("Unsubscribed OK")


# Set callbacks

mqttc.on_message = on_message

mqttc.on_connect = on_connect

mqttc.on_subscribe = on_subscribe

mqttc.on_unsubscribe = on_unsubscribe


# Connect and subscribe

print("Connecting to " + host + "/" + topic)

mqttc.connect(host, port=1883, keepalive=60)

mqttc.subscribe(topic, 0)


# Publish messages from Python

num = 0

while num != 5:

      #ret = mqttc.publish(topic, "Message from Python!\n", qos=0)
      ret = mqttc.publish(topic, "ready", qos=0)

      if (ret[0] != 0):

            print("Publish failed")

      mqttc.loop()

      time.sleep(0.5)

      num += 1



# Loop forever, receiving messages

mqttc.loop_forever()