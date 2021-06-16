import math
import paho.mqtt.client as mqtt
import time
import json 
import numpy as np

<<<<<<< HEAD
#angle = ""

ser=serial.Serial('/dev/ttyACM0',9600)
=======
>>>>>>> e3703dffe59d326b24200bdac0186624a3600403
mqtt_username = "sumobot"
mqtt_password = "sumobot"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print("Connected")

def on_message(client, userdata, message):
    angle = str(message.payload.decode("utf-8"))
    #print(angle)

client.on_connect = on_connect
<<<<<<< HEAD
client.connect("raspberrypi", 1883, 60)
client.on_message = on_message
client.subscribe("raspberry/imu")
while True:
    #client.loop()
    readedText = ser.readline()
    decode = readedText.decode('UTF-8')
    decode = decode.replace("\r\n", "")
    temp_list = decode.split(',')
    if (len(temp_list) < 6):
        decode_list = [0, 0, 0, 0, 0, 0]
    else:
        decode_list = [int(i) for i in temp_list]
    
    #decode_list.append(angle)
    # X = np.reshape(decode_list, (1, 4))
    # pred = model(X)
    #print(decode_list)
    # move = np.argmax(pred[0])
    # print(movement[move])
    #for i in range(0, 5):
     #   time.sleep(2)
      #  print(movement[i])
       # payload_dict = {"cw": True, "move": i}
    payload_json = json.dumps(decode_list)
    client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)
        #time.sleep(0.5)
        #payload_dict = {"cw": True, "move": 0}
        #payload_json = json.dumps(payload_dict)
        #client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)
    
   
=======
client.connect("192.168.1.13", 1883, 60)

payload_dict = {"cw": True, "move": 1}
payload_json = json.dumps(payload_dict)
client.publish('raspberry/bot', payload=payload_json, qos = 0, retain=False)
time.sleep(2)
payload_dict = {"cw": True, "move": 0}
payload_json = json.dumps(payload_dict)
client.publish('raspberry/bot', payload=payload_json, qos = 0, retain=False)

       

>>>>>>> e3703dffe59d326b24200bdac0186624a3600403

