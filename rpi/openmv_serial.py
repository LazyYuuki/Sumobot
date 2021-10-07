import serial
import math
import paho.mqtt.client as mqtt
import time
import json 

ser=serial.Serial('/dev/ttyACM0',115200)
distance = 0
mqtt_username = "sumobot"
mqtt_password = "sumobot"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print(1)
client.on_connect = on_connect
client.connect("raspberrypi", 1883, 60)

while True:
    readedText = ser.readline()
    decode = readedText.decode('UTF-8')
    
#    print(decode)
    
    ours = [0,0,0,0]# x1,y1,x2,y2
    enemy = [0,0,0,0]# same as above
    arena = [0,0]#x,y
    temp_list = decode.split(',')
    if (len(temp_list) == 10):
        decode_list = temp_list
    else:
        decode_list = ["0","0","0","0","0","0","0","0","0","0"]
    
    print(decode_list)
    if (len(decode_list) == 10):
        for i in range(10):
            if i<4:
                try:
                    ours[i] = int(decode_list[i])
                    break
                except ValueError:
                    ours[i] = 0
            elif i<8:
                try:
                    enemy[i-4] = int(decode_list[i])
                    break
                except ValueError:
                    enemy[i-4] = 0
                
            else:
                
                try:
                    arena[i-8] = int(decode_list[i].replace("\r\n",""))
                    break
                except ValueError:
                    arena[i-8] = 0
#     print(ours)
    ours_arena = [ours[0]-arena[0],arena[1] - ours[1]] # coordinate of our bot wrt the arena's origin
    enemy_arena = [enemy[0]-arena[0], arena[1]-enemy[1]] #coordinate of enemy wrt arena's center
    prev_distance = distance
    distance = math.sqrt((ours_arena[0]-enemy_arena[0])**2 + (ours_arena[1]-enemy_arena[1])**2)
    distance = int(distance)
    max_distance = 100
    if(decode_list[4] != '1000'):
    #if not (distance < 95):
        print("ok move")
        payload_dict = {"cw": True, "move": True}
        payload_json = json.dumps(payload_dict)
        client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)
    else:
        print("dont move")
        payload_dict = {"cw": True, "move": False}
        payload_json = json.dumps(payload_dict)
        client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)

#     CW = True
#     
#     if(distance < max_distance):
#         if distance < prev_distance:
#             print("Change!")
#             CW = not CW
#             payload_dict = {"cw": CW, "move": True}
#             payload_json = json.dumps(payload_dict)
#             client.publish('rasberry/topic', payload=payload_json, qos = 0, retain=False)
#         else:
#             print("No change!")
#             payload_dict = {"cw": CW, "move": True} 
#             payload_json = json.dumps(payload_dict)
#             client.publish('rasberry/topic', payload=payload_json, qos = 0, retain=False)            
#     else:
#         print("No move")
#         payload_dict = {"cw": CW, "move": False}
#         payload_json = json.dumps(payload_dict)
#         client.publish('rasberry/topic', payload=payload_json, qos = 0, retain=False)        
#     time.sleep(0.1)

#print(ours)
#     print(enemy)
#     print(arena)
#     print(ours_arena)
#     print(enemy_arena)                                                                     v   
#     print(distance)
    
   
