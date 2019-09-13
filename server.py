import socket
import config
import threading
import cards
import time
import money

Server = socket.socket()
Server.bind((config.addr, config.port))
alive = True
connected = []
info = []
hands = []
table = []
turn = 0
raise_by = 1

money.load_table()

def update_connections():
    global connected, alive
    c_s = Server.accept()[0]
    connected.append(c_s)
    #create thread for each connection
    while alive:
        print("Got connection")
        t = threading.Thread(target=handle_recv, args=[c_s])
        t.start()
        c_s = Server.accept()[0]
        connected.append(c_s)
    connected.pop()

def begin_listen():
    global alive, Server
    alive = True
    Server.listen()
    t = threading.Thread(target=update_connections)
    t.start()

def end_listen():
    global alive
    alive = False
    send_init()
    print("connected")
    deal_cards()

def send_to_all(payload):
    try:
        payload = payload.encode()
    except:
        pass #already encoded
    for c_s in connected:
        c_s.sendall(payload)

def send_init():
    head = "INIT\n"
    message = ""
    for player in info:
        #name and money
        message += player[0]+"\x00"+player[1]+"\n"
    payload = (head+message).encode()
    #now send it to each socket individually
    send_to_all(payload)

def handle_recv(c_s):
    global raise_by
    number = connected.index(c_s)
    while True:
        recv = c_s.recv(4096)
        recv = recv.decode()
        head, data = recv.split("\n")[0], recv.split("\n")[1:]
        
        print("Server received text")
        print("\t", head, data)
        
        if head=="INIT":
            username = data[0]
            password = data[1]
            value = money.retrieve(username, password)
            info.append([username, str(value)])
            #print(info)
            
        elif head=="CHAT":
            name = data[0]
            message = data[1]
            send_chat(name, message)
        
        elif head=="GAME":
            if data[0]=="FOLD":
                send_game(number, "FOLD")
            elif data[0]=="RAISE":
                send_game(number, "RAISE", data[1])
                value -= int(data[1])
                raise_by = int(data[1])
                money.set_val(username, password, value)
            elif data[0]=="MATCH":
                send_game(number, "MATCH")
                value -= raise_by
                money.set_val(username, password, value)
                pass

            #need this otherwise client doesn't have enough time to react
            time.sleep(0.1)
            send_turn()
        
def send_chat(name, message):
    head = "CHAT\n"
    payload = head + name + ": " + message
    send_to_all(payload.encode())

def deal_cards():
    global connected
    head = "INITCARD\n"
    
    player_num = len(connected)
    #1 deck for every 10 players
    decks = 1+(player_num//10)
    deck = cards.create_deck(decks)
    time.sleep(1)
    for i in range(player_num):
        c1 = deck[i*2]
        c2 = deck[i*2+1]
        c_s = connected[i]
        hands.append([c1,c2])
        #head, number, card 1, card 2
        payload = head+str(i)+"\n"+c1+"\n"+c2
        
        c_s.sendall(payload.encode())
        #print(payload)

    deck = deck[player_num*2:]
    #add the community cards
    table.extend([deck[0], deck[1], deck[2], deck[3], deck[4]])

def send_game(number, action, val=None):
    head = "GAME\n"
    if action=="FOLD":
        payload = head + str(number)+"\n" + "FOLD"
    elif action=="MATCH":
        payload = head + str(number)+"\n" + "MATCH"
    elif action=="RAISE":
        payload = head + str(number)+"\n" + "RAISE\n" + val

    send_to_all(payload.encode())

def send_turn():
    global turn
    head = "TURN\n"
    payload = head+str(turn)
    send_to_all(payload.encode())
    turn += 1
    if turn>=len(connected):
        turn = 0
