from card import *
import platform, zmq, os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def self_hash():
    return str(hash(platform.node()))

def send(mes: str):
    pub.send_string(mes)

def listen():
    data = str(sub.recv())
    #print (data)
    return data[2:len(data)-1]

def listen_untill(prefix):
    listening = True
    while listening:
        data = listen().split(" ")
        if data[0] == prefix:
            listening = False
            #data = " ".join(data)
            #print (data)
            return " ".join(data)

PORT = 65432
HOST = input("Host: ")
client=zmq.Context()
sub=client.socket(zmq.SUB)
sub.setsockopt_string(zmq.SUBSCRIBE,'')
sub.connect('tcp://'+HOST+':'+str(PORT))
pub=client.socket(zmq.PUSH)
pub.connect('tcp://'+HOST+':'+str(PORT+1))

name = input("Name: ")
client_id = self_hash()#name
clear()
send(f"id {client_id} {name}")

data = listen_untill(client_id).split(" ")
player_number = data[1]

def correctify(s):
    while len(s) != 3:
        s = "0" + s
    return s

def do(com):
    if com[0] == "cc":
        clear()
        print (f"Current card: {com[1].replace(',', ' ')}")
    elif com[0] == "cl":
        print (f"Cards left: {com[1]}")
    elif com[0] == "ca":
        print ()
        print ("Your cards:")
        l = com[1:len(com)]
        l = list(map(correctify, l))
        for i in range(len(l)):
            #i = str(i)
            color = COLOR_TRANSLATOR[int(l[i][0:1])]
            card_type = TYPE_TRANSLATOR[int(l[i][1:3])]
            print (str(i+1)+".", color, card_type)
            #print (f"{str(i)}. {l[i].replace(',', ' ')}")
        print ()
    elif com[0] == "rc":
        c = input("Number of card(s) to play:\n")
        send(c)
    elif com[0] == "np":
        print ("\nNot a playable card")
    elif com[0] == "cr":
        c = input("\nNew color:\n")
        send(c)

on = True
while on:
    message = listen().split(" ")
    #print (message)
    if message[0] == str(player_number):
        do(message[1:len(message)])
    elif message[0] == "wait":
        clear()
        print (f"########### Waiting for {message[1]} ###########")
    elif message[0] == "win":
        clear()
        print (f"########### {message[1]} wins! ###########")
        on = False
        break