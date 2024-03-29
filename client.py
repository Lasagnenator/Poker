import config
import socket
import threading
import time

client_socket = socket.socket()
connected = False

chat_log = ""
player_info = []
cards = []
number = 0
player_number = 0
raise_by = 1
pot = 0
turn = 0
table = []

hands = []

winners = []
win_type = ""
win_amount = 0

started = False
anything_changed = False
finished = False

lock = threading.Lock()

def connect(addr):
    client_socket.connect((addr, config.port))
    #send init protocol
    head = "INIT\n"
    payload = head+config.username+"\n"+config.password
    client_socket.sendall(payload.encode())

    #start the thread to receive stuff
    handle_recv()
    connected = True

def chat(message):
    #must be connected already!
    head = "CHAT\n"
    payload = head+config.username+"\n"+message
    client_socket.sendall(payload.encode())

def _handle_recv():
    global chat_log, number, raise_by, pot, turn, player_number, started, anything_changed
    global finished, winners, win_type, win_amount
    while True:
        recv = client_socket.recv(4096)
        recv = recv.decode()
        if recv=="":
            break
        head, data = recv.split("\n")[0], recv.split("\n")[1:]
        lock.acquire()
        print("Client received text")
        print("\t",head, data)

        

        if head=="INIT":
            #print("Initilisation")
            for info in data:
                #name, money, status
                if not "\x00" in info:
                    break
                player_info.append([*info.split("\x00"), "-", ""])
                #if info.split("\x00")[0]==config.username:
                    #number = data.index(info)
            started = True
            anything_changed = True
        if head=="INITCARD":
            #print("Card initilisation")
            player_number = int(data[0])
            card1 = data[1]
            card2 = data[2]
            
            cards.append(card1)
            cards.append(card2)
            #print("Cards:",cards)
        if head=="CHAT":
            #print("Chat message")
            #chat message
            message = data[0]
            chat_log = message+"\n"
            #chat_log += message+"\n"

        if head=="GAME":
            #print("Gameplay action")
            #something happened in-game
            number = int(data[0])
            if data[1]=="FOLD":
                #set status as folded
                player_info[number][2] = "Folded"
            elif data[1]=="RAISE":
                #display the raise
                player_info[number][2] = "Raised by {}".format(data[2])
                raise_by = int(data[2])
                player_info[number][1] = str(int(player_info[number][1])-raise_by)
                pot += raise_by
            elif data[1]=="MATCH":
                #display matched current raise
                player_info[number][2] = "Matched"
                player_info[number][1] = str(int(player_info[number][1])-raise_by)
                pot += raise_by
            elif data[1]=="ALLIN":
                player_info[number][2] = "All in"
                pot += int(player_info[number][1])
                raise_by = max(raise_by, int(player_info[number][1]))
                player_info[number][1] = "0"
                #print(pot)
            anything_changed = True

        if head=="TURN":
            #whose turn it is
            turn = int(data[0])
            for i in range(len(player_info)):
                player_info[i][3] = ""
            player_info[turn][3] = "Turn"
            anything_changed = True

        if head=="TABLE":
            if data[0]=="FIRST3": #first 3 cards
                table.extend(data[1:])
                
            elif data[0]=="FOURTH": #fourth card
                table.append(data[1])
                
            elif data[0]=="FIFTH": #fifth card
                table.append(data[1])

        if head=="REVEAL":
            for item in data:
                hands.append(item.split("\x00"))
            anything_changed = True
            finished = True

        if head=="WINNER":
            for winner in data[0].split("\x00"):
                winners.append(int(winner))
            win_type = data[1]
            win_amount = data[2]
            anything_changed = True

        lock.release()

def handle_recv():
    t = threading.Thread(target=_handle_recv)
    t.start()

def send_fold():
    head = "GAME\n"
    payload = head+"FOLD"
    client_socket.sendall(payload.encode())
    
def send_match():
    head = "GAME\n"
    payload = head+"MATCH"
    client_socket.sendall(payload.encode())

def send_raise(amount):
    head = "GAME\n"
    payload = head+"RAISE\n"+str(amount)
    client_socket.sendall(payload.encode())

def send_all_in():
    head = "GAME\n"
    payload = head+"ALLIN"
    client_socket.sendall(payload.encode())
