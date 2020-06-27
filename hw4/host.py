import paho.mqtt.client as paho

import serial

import time

mqttc = paho.Client()


# Settings for connection

host = "localhost"

topic= "Mbed"

port = 1883


# Callbacks

def on_connect(self, mosq, obj, rc):

    print("Connected rc: " + str(rc))


def on_message(mosq, obj, msg):

    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");


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

####################################################
# XBee setting

serdev = '/dev/ttyUSB0'

s = serial.Serial(serdev, 9600)


s.write("+++".encode())

char = s.read(2)

print("Enter AT mode.")

print(char.decode())


s.write("ATMY 0x140\r\n".encode())

char = s.read(3)

print("Set MY 0x140.")

print(char.decode())


s.write("ATDL 0x240\r\n".encode())

char = s.read(3)

print("Set DL 0x240.")

print(char.decode())


s.write("ATID 0x1\r\n".encode())

char = s.read(3)

print("Set PAN ID 0x1.")

print(char.decode())


s.write("ATWR\r\n".encode())

char = s.read(3)

print("Write config.")

print(char.decode())


s.write("ATMY\r\n".encode())

char = s.read(4)

print("MY :")

print(char.decode())


s.write("ATDL\r\n".encode())

char = s.read(4)

print("DL : ")

print(char.decode())


s.write("ATCN\r\n".encode())

char = s.read(3)

print("Exit AT mode.")

print(char.decode())


print("start sending RPC")
####################################################


def readchar():
    acc = ""
    read = 1
    while read:

        while(s.readable()):

            char=s.read(1)

            acc += char.decode()
            
            if (acc == "\r"):
                print("rrr")
            if char.decode() == "\n" or char.decode() == "\r":
                read = 0
                break
    print("acc: "+acc)
    return acc

    
import matplotlib.pyplot as plt

import numpy as np

tn = np.arange(0, 20, 1)
t = np.arange(0, 20, 0.5)
n = np.arange(0, 20, 1)
x = np.arange(0, 20, 0.5)
y = np.arange(0, 20, 0.5)
z = np.arange(0, 20, 0.5)
tilt = np.arange(0, 20, 0.5)

for i in range(0, 20):

    if i == 0:
        print("i=0")
        s.write("/query/run\r".encode())
        readchar()
        time.sleep(0.2)
        print("i=0")

    s.write("/query/run\r".encode())

    print(">>>>>j=")
    j = int(readchar())
    n[i] = int(readchar())
    x[2*i] = float(readchar())
    y[2*i] = float(readchar())
    z[2*i] = float(readchar())
    x[2*i+1] = float(readchar())
    y[2*i+1] = float(readchar())
    z[2*i+1] = float(readchar())
    print("<<<<<j=")
    j = int(readchar())

    print("nnnnn")

    time.sleep(0.3)

s.close()


for i in range(0, 40):
    if z[i]<0 or z[i]*z[i]<0.5:
        tilt[i] = 1
    else:
        tilt[i] = 0
    
    
    
    mesg = str(x[i])

    mqttc.publish(topic, mesg)

    print(mesg)

    mesg = str(y[i])

    mqttc.publish(topic, mesg)

    print(mesg)

    mesg = str(z[i])

    mqttc.publish(topic, mesg)

    print(mesg)

    mesg = str(tilt[i])

    mqttc.publish(topic, mesg)

    print(mesg)



plt.plot(tn,n)

plt.xlabel('timestamp')

plt.ylabel('number')

plt.show()