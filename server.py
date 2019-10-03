import socket
import config
import threading
import cards
import time
import money
import winner

Server = socket.socket()
alive = True
server_running = False
connected = []
info = []
hands = []
table = []
turn = 0
raise_by = 1
pot = 0
cards_visible = 0
last_raise = 0

round_num = 0
match_count = 0

user_pass = []

money.load_table()

lock = threading.Lock()

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
    Server.bind((config.addr, config.port))
    #Server.bind(socket.INADDR_ANY)
    Server.listen()
    t = threading.Thread(target=update_connections)
    t.start()

def end_listen():
    global alive
    send_init()
    time.sleep(0.1)
    alive = False
    
    print("connected")
    deal_cards()

def send_to_all(payload):
    try:
        payload = payload.encode()
    except:
        pass #already encoded
    for c_s in connected:
        try:
            c_s.sendall(payload)
        except ConnectionResetError:
            pass

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
    global raise_by, info, pot, last_raise
    number = connected.index(c_s)
    while server_running:
        try:
            recv = c_s.recv(4096)
        except ConnectionResetError:
            send_game(number, "FOLD")
            info[number][2] = "FOLD"
            print("Player",number,"disconnected.")
            if turn==number:
                send_turn()
            return
        recv = recv.decode()
        head, data = recv.split("\n")[0], recv.split("\n")[1:]
        
        lock.acquire()
        
        print("Server received text")
        print("\t", head, data)
        
        if head=="INIT":
            username = data[0]
            password = data[1]
            value = money.retrieve(username, password)
            if value<=0: #no money
                print("Player",number,"had no money. Kicking them.")
                connected.remove(c_s)
                return
            info.append([username, str(value), ""])
            user_pass.append([username, password])
            #print(info)
            
        elif head=="CHAT":
            name = data[0]
            message = data[1]
            send_chat(name, message)
        
        elif head=="GAME":
            if data[0]=="FOLD":
                send_game(number, "FOLD")
                info[number][2] = "FOLD"
            elif data[0]=="RAISE":
                send_game(number, "RAISE", data[1])
                value -= int(data[1])
                raise_by = int(data[1])
                money.set_val(username, password, value)
                pot += raise_by
                info[number][2] = "RAISE"
                last_raise = number
            elif data[0]=="MATCH":
                send_game(number, "MATCH")
                value -= raise_by
                money.set_val(username, password, value)
                pot += raise_by
                info[number][2] = "MATCH"
            elif data[0]=="ALLIN":
                send_game(number, "ALLIN")
                raise_by = max(value, raise_by) #because an all in can match higher raise
                pot += raise_by
                if value>raise_by:
                    last_raise = number #higher so this is the latest raise
                value = 0
                money.set_val(username, password, value)
                info[number][2] = "ALLIN"

            #need this otherwise client doesn't have enough time to react
            time.sleep(0.1)
            info[number][1] = str(value)
            send_turn()
        lock.release()
    c_s.shutdown(0)
    c_s.close()
        
def send_chat(name, message):
    head = "CHAT\n"
    payload = head + name + ": " + message
    send_to_all(payload.encode())
    #print(len(connected))

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
    elif action=="ALLIN":
        payload = head + str(number)+"\n" + "ALLIN"

    send_to_all(payload.encode())

def send_turn():
    global turn
    head = "TURN\n"
    #payload = head+str(turn)
    old = turn
    turn += 1
    if turn>=len(connected):
        turn = 0

    payload = head+str(turn)
    try:
        while info[turn][2]=="ALLIN" or info[turn][2]=="FOLD":
            turn += 1 #skip a person if they folded or went all-in
            if turn>=len(connected):
                turn = 0
            payload = head+str(turn)
            if turn==old: #break if we looped around
                break
            
            check_round()
    except BaseException as e:
        print(e.args)
        pass
    
    #print("here")
    send_to_all(payload.encode())

    time.sleep(0.5)

    check_round()

def check_round():
    #this is run at the end of a send_turn call
    global round_num, info, cards_visible, match_count, last_raise

    #print("last_raise =", last_raise)
    #print("info =", info)
    #print("turn =", turn)

    if turn != last_raise: #only start checking once we are back to last raise
        return

    auto_skip_count = 0

    for player in info:
        if player[2]=="MATCH":
            match_count += 1
        if player[2]=="ALLIN":
            match_count += 1
            auto_skip_count += 1
        if player[2]=="FOLD":
            match_count += 1
            auto_skip_count += 1

    #print("match_count =", match_count)

    if match_count==len(info)-1: # everyone else matched
        #print("cards_visible =", cards_visible)
        match_count = 0
        if cards_visible==0:
            send_table("FIRST3")
            if auto_skip_count==len(info)-1:
                #auto complete
                time.sleep(0.1)
                send_table("FOURTH")
                time.sleep(0.1)
                send_table("FIFTH")
                time.sleep(0.1)
                reveal_cards()
                find_winner()
                
        elif cards_visible==3:
            send_table("FOURTH")
            if auto_skip_count==len(info)-1:
                time.sleep(0.1)
                send_table("FIFTH")
                time.sleep(0.1)
                reveal_cards()
                find_winner()
                
        elif cards_visible==4:
            send_table("FIFTH")
            if auto_skip_count==len(info)-1:
                time.sleep(0.1)
                reveal_cards()
                find_winner()
        elif cards_visible==5:
            reveal_cards()
            find_winner()

    match_count = 0

def send_table(which):
    global table, cards_visible
    head = "TABLE\n"
    if which=="FIRST3":
        cards_visible = 3
        payload = head + "FIRST3\n" + table[0]+"\n" + table[1]+"\n" + table[2]
    elif which=="FOURTH":
        cards_visible = 4
        payload = head + "FOURTH\n" + table[3]
    elif which=="FIFTH":
        cards_visible = 5
        payload = head + "FIFTH\n" + table[4]
    send_to_all(payload.encode())

def reveal_cards():
    head = "REVEAL\n"
    payload = head
    for i, hand in enumerate(hands):
        temp = winner.fname_to_cards(hand)
        payload += temp[0]+"\x00"+temp[1]+"\n"
    payload = payload[:-1] #remove the trailing newline
    send_to_all(payload.encode())

def find_winner():
    global server_running
    allowed = []
    for i, hand in enumerate(hands):
        if info[i][2]!="FOLD":
            allowed.append(hand)

    best_hands, win_type = winner.determine_winner(allowed, table)
    win_nums = []
    for hand in best_hands:
        win_nums.append(str(hands.index(hand)))

    #distribute pot
    winner_count = len(win_nums)
    amount = (pot//winner_count)+ (pot%winner_count>0) #rounds up

    for num in win_nums:
        username, password = user_pass[int(num)]
        value = money.retrieve(username, password)
        value += amount
        money.set_val(username, password, value)
        info[int(num)][1] = str(value)
    money.save_table()

    head = "WINNER\n"
    payload = head+"\x00".join(win_nums)+"\n"+win_type+"\n"+str(amount)
    send_to_all(payload.encode())
    server_running = False
    
    pass
